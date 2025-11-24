import threading
import os
import time
import webbrowser

try:
    import PySimpleGUI as sg
except Exception:
    sg = None

from downloader import MusicDownloader


def start_gui():
    if sg is None:
        print("PySimpleGUI no está instalado. Instala dependencias con: python -m pip install -r requirements.txt")
        return

    # Theme colors (black & gold)
    BG = "#0b0b0b"
    FG = "#D4AF37"
    BUTTON_BG = "#1e1e1e"

    # Set a base theme and rely on element-level colors
    try:
        sg.theme('Dark')
    except Exception:
        pass

    layout = [
        [sg.Text('Music Downloader', font=('Any', 20), justification='center', expand_x=True, pad=(10, 10))],
        [
            sg.Text('Modo:', pad=(5, 5)),
            sg.Radio('YouTube URL', 'mode', key='-YT-', default=True, enable_events=True, background_color=BG, text_color=FG),
            sg.Radio('Búsqueda', 'mode', key='-QUERY-', enable_events=True, background_color=BG, text_color=FG),
            sg.Radio('Spotify URL', 'mode', key='-SPOT-', enable_events=True, background_color=BG, text_color=FG),
        ],
        [sg.Text('Entrada:', size=(8, 1), pad=(5, 5)), sg.Input(key='-INPUT-', expand_x=True), sg.Button('Abrir doc', key='-HELP-', button_color=(FG, BUTTON_BG))],
        [sg.Text('Carpeta destino:', size=(12, 1)), sg.Input(default_text='downloads', key='-OUT-', expand_x=True), sg.FolderBrowse(button_text='Elegir', target='-OUT-')],
        [sg.Button('Descargar', key='-DL-', size=(10, 1), button_color=(BG, FG)), sg.Button('Salir', key='-EXIT-', button_color=(BG, FG))],
        [sg.HorizontalSeparator(color=FG)],
        [sg.Multiline('', size=(80, 12), key='-LOG-', autoscroll=True, background_color=BG, text_color=FG, disabled=True)],
    ]

    window = sg.Window('Music Downloader', layout, finalize=True, element_justification='left', background_color=BG)

    dl = MusicDownloader()

    def log(msg: str):
        window['-LOG-'].update(value=msg + '\n', append=True)

    download_thread = None

    def do_download(mode: str, text: str, outdir: str):
        nonlocal dl
        dl = MusicDownloader(output_dir=outdir)
        if not dl.check_ffmpeg():
            log('Advertencia: ffmpeg no encontrado. La conversión a MP3 puede fallar.')

        log(f'Iniciando descarga (modo={mode})...')
        result = None
        try:
            if mode == 'yt':
                result = dl.download_youtube(text)
            elif mode == 'query':
                result = dl.download_query(text)
            elif mode == 'spotify':
                result = dl.download_spotify(text)
        except Exception as e:
            log(f'Error durante descarga: {e}')

        if result:
            log(f'Descarga completada: {result}')
            # Open folder containing result if possible
            try:
                if os.path.isdir(result):
                    webbrowser.open(result)
                else:
                    webbrowser.open(os.path.dirname(result))
            except Exception:
                pass
        else:
            log('No se pudo completar la descarga.')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-EXIT-'):
            break
        if event == '-HELP-':
            sg.popup('Introduce una URL de YouTube o Spotify, o un texto de búsqueda. Ejemplos:\n- https://www.youtube.com/watch?v=...\n- https://open.spotify.com/track/...\n- Bohemian Rhapsody Queen', title='Ayuda', background_color=BG, text_color=FG)
        if event == '-DL-':
            inp = values['-INPUT-'].strip()
            out = values['-OUT-'].strip() or 'downloads'
            if not inp:
                sg.popup('Ingresa una URL o consulta.', title='Error', background_color=BG, text_color=FG)
                continue

            if values['-YT-']:
                mode = 'yt'
            elif values['-QUERY-']:
                mode = 'query'
            else:
                mode = 'spotify'

            # start thread
            window['-DL-'].update(disabled=True)
            download_thread = threading.Thread(target=lambda: [do_download(mode, inp, out), window.refresh(), window['-DL-'].update(disabled=False)])
            download_thread.start()

    window.close()


if __name__ == '__main__':
    start_gui()
