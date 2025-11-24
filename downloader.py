import os
import shutil
import subprocess
from typing import Optional

try:
    import yt_dlp as ytdl
except Exception:
    ytdl = None

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import glob

try:
    import mutagen
    from mutagen.easyid3 import EasyID3
except Exception:
    mutagen = None
    EasyID3 = None


class MusicDownloader:
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.ffmpeg_path = shutil.which("ffmpeg")

    def check_ffmpeg(self) -> bool:
        return self.ffmpeg_path is not None

    def _yt_dlp_opts(self, outtmpl: Optional[str] = None):
        outtmpl = outtmpl or os.path.join(self.output_dir, "%(title)s.%(ext)s")
        opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "noplaylist": True,
            "quiet": False,
            "no_warnings": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        return opts

    def download_youtube(self, url: str) -> Optional[str]:
        """Download a YouTube URL as MP3. Returns output filepath or None on error."""
        outtmpl = os.path.join(self.output_dir, "%(title)s.%(ext)s")
        if ytdl:
            try:
                opts = self._yt_dlp_opts(outtmpl=outtmpl)
                with ytdl.YoutubeDL(opts) as dl:
                    info = dl.extract_info(url, download=True)
                    title = info.get("title")
                    artist = info.get("artist") or info.get("uploader")
                    # try to find the resulting mp3 file
                    filepath = self._find_newest_mp3()
                    if filepath and mutagen and EasyID3:
                        self._tag_file(filepath, title=title, artist=artist)
                    return filepath
            except Exception as e:
                print("Error con yt_dlp API:", e)
                return None
        else:
            # Fallback to calling system yt-dlp
            cmd = [
                "yt-dlp",
                "-x",
                "--audio-format",
                "mp3",
                "-o",
                outtmpl,
                url,
            ]
            try:
                subprocess.run(cmd, check=True)
                # We cannot easily know final filename without parsing yt-dlp output; try to find newest mp3
                filepath = self._find_newest_mp3()
                return filepath or self.output_dir
            except Exception as e:
                print("Error ejecutando yt-dlp en subprocess:", e)
                return None

    def download_query(self, query: str, title: Optional[str] = None, artist: Optional[str] = None) -> Optional[str]:
        """Search YouTube and download the first result. Optionally provide title/artist for tagging."""
        search = f"ytsearch1:{query}"
        filepath = self.download_youtube(search)
        # If download_youtube couldn't tag (e.g., subprocess path), attempt tagging here using provided metadata
        if filepath and mutagen and EasyID3:
            # ensure we only tag if file exists and tags are missing
            self._tag_file(filepath, title=title or query, artist=artist)
        return filepath

    def resolve_spotify(self, url: str) -> Optional[tuple]:
        """Resolve Spotify track/album/playlist URL to a reasonable search query (title + artist).
        This function scrapes the public Spotify page and tries to extract the track title and artist.
        """
        headers = {"User-Agent": UserAgent().random}
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print("No se pudo obtener la página de Spotify:", e)
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        # Try common meta tags
        title = None
        artist = None
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title["content"]
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            # often "Track — Artist" or similar
            desc = og_desc["content"]
            # try to split by '•' or '–' or '-' or 'by'
            # Keep desc as fallback
            if "•" in desc:
                parts = [p.strip() for p in desc.split("•") if p.strip()]
                if parts:
                    title = title or parts[0]
            else:
                # leave as fallback
                pass

        # Fallback to title tag
        if not title and soup.title:
            title_text = soup.title.string or ""
            title = title_text.replace(" on Spotify", "").strip()

        # Try to parse title into song + artist if it contains separators
        if title:
            text = " ".join(title.split())
            seps = ["•", "·", "—", "–", "-", "|"]
            song = None
            art = None
            for sep in seps:
                if sep in text:
                    parts = [p.strip() for p in text.split(sep) if p.strip()]
                    if len(parts) >= 2:
                        # assume first is song, last is artist
                        song = parts[0]
                        art = parts[-1]
                        break
            if not song:
                # fallback: try to split by ' by '
                if ' by ' in text.lower():
                    parts = text.split(' by ')
                    song = parts[0].strip()
                    art = parts[-1].strip()
                else:
                    # use whole title as query
                    song = text
            query = f"{song} {art or ''}".strip()
            return (query, song, art)
        else:
            print("No se encontró metadata útil en la página de Spotify.")
            return None

    def download_spotify(self, spotify_url: str) -> Optional[str]:
        resolved = self.resolve_spotify(spotify_url)
        if not resolved:
            print("No se pudo resolver la URL de Spotify a una consulta.")
            return None
        query, song, artist = resolved
        print(f"Buscando en YouTube: {query}")
        # pass song/artist to allow tagging
        return self.download_query(query, title=song, artist=artist)

    def _find_newest_mp3(self) -> Optional[str]:
        pattern = os.path.join(self.output_dir, "*.mp3")
        files = glob.glob(pattern)
        if not files:
            return None
        newest = max(files, key=os.path.getmtime)
        return newest

    def _tag_file(self, filepath: str, title: Optional[str] = None, artist: Optional[str] = None) -> None:
        if not mutagen or not EasyID3:
            return
        try:
            try:
                audio = EasyID3(filepath)
            except Exception:
                audio = mutagen.File(filepath, easy=True)
                if audio is None:
                    return
                if not audio.tags:
                    audio.add_tags()
            if title:
                audio['title'] = title
            if artist:
                audio['artist'] = artist
            audio.save()
        except Exception as e:
            print(f"No se pudieron escribir tags en {filepath}: {e}")
