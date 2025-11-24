import argparse
import sys
from downloader import MusicDownloader


def parse_args():
    p = argparse.ArgumentParser(description="Descarga canciones en MP3 desde YouTube o resolviendo URLs de Spotify (usa YouTube).")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--youtube", "-y", help="URL de YouTube o texto de búsqueda prefijado con 'ytsearch1:'")
    group.add_argument("--query", "-q", help="Consulta de búsqueda (p.ej. 'Bohemian Rhapsody Queen')")
    group.add_argument("--spotify", "-s", help="URL de Spotify (se resolverá a una búsqueda en YouTube)")
    p.add_argument("--output", "-o", default="downloads", help="Carpeta de salida para MP3")
    return p.parse_args()


def main():
    args = parse_args()
    dl = MusicDownloader(output_dir=args.output)
    if not dl.check_ffmpeg():
        print("Advertencia: No se encontró FFmpeg en el sistema. yt-dlp necesita FFmpeg para convertir a MP3. Instala FFmpeg y vuelve a intentarlo.")

    result = None
    if args.youtube:
        # If user passed a raw URL, download directly; if they passed a search string, we call download_youtube (yt-dlp accepts ytsearch1:)
        result = dl.download_youtube(args.youtube)
    elif args.query:
        result = dl.download_query(args.query)
    elif args.spotify:
        result = dl.download_spotify(args.spotify)

    if result:
        print("Descarga completada. Resultado:", result)
    else:
        print("No se pudo completar la descarga.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrumpido por el usuario')
        sys.exit(1)
