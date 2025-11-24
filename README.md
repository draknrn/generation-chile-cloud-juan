# Music Downloader

Pequeña herramienta que descarga audio en MP3 usando `yt-dlp` como backend. Para resolver canciones desde Spotify se usa una búsqueda en YouTube basada en la metadata pública de la página de Spotify.

Requisitos
- Python 3.8+
- `ffmpeg` instalado y disponible en PATH (necesario para la conversión a MP3)

Instalación

```bash
python -m pip install -r requirements.txt
# asegúrate de tener ffmpeg instalado en tu sistema
```

Uso

- Descargar desde YouTube (URL o consulta `ytsearch1:`):

```bash
python main.py --youtube "https://www.youtube.com/watch?v=..."
# o búsqueda
python main.py --youtube "ytsearch1:Bohemian Rhapsody Queen"
```

- Descargar por consulta:

```bash
python main.py --query "Bohemian Rhapsody Queen"
```

- Descargar resolviendo una URL de Spotify:

```bash
python main.py --spotify "https://open.spotify.com/track/...."
```

Notas
- Descargar directamente de Spotify no está implementado (DRM y legalidad). Este proyecto resuelve la URL de Spotify a una consulta y descarga la coincidencia en YouTube.
- Si `yt-dlp` no está instalado como módulo, el script intentará llamar a la herramienta `yt-dlp` en PATH.

Interfaz gráfica (GUI)

Este proyecto incluye una GUI basada en `PySimpleGUI` con tema negro y detalles dorados. Para ejecutarla, instala las dependencias y lanza:

```bash
python gui.py
```

La GUI permite elegir modo (YouTube URL, Búsqueda o Spotify URL), especificar la carpeta de salida y ver el log de progreso. Asegúrate de tener un servidor X o entorno gráfico disponible si ejecutas esto en una máquina remota.

Uso en Windows (GUI)

1. Instalar FFmpeg:
	- Descarga una versión estática de FFmpeg desde https://ffmpeg.org/download.html#build-windows (por ejemplo, builds de gyan o BtbN).
	- Extrae el contenido y añade la carpeta `bin` de FFmpeg a la variable de entorno `PATH` (Sistema → Configuración avanzada del sistema → Variables de entorno).

2. Instalar dependencias Python:

```powershell
python -m pip install -r requirements.txt
```

3. Ejecutar la interfaz gráfica (desde PowerShell o CMD):

```powershell
python gui.py
```

4. Uso rápido:
	- Elige `YouTube URL`, `Búsqueda` o `Spotify URL`.
	- Ingresa la URL o la consulta y selecciona la carpeta de salida.
	- Pulsa `Descargar` y revisa el log en la ventana.

Nota: en Windows la GUI se ejecuta en el entorno gráfico local; no requiere servidor X. Si haces doble clic en `gui.py`, es recomendable ejecutarlo desde una terminal para ver mensajes y logs.
