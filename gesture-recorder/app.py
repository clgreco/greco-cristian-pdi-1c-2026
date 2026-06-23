"""
app.py
------

Version Gradio de gesture-recorder. Disenada para Gradio 5.

Patron de streaming
-------------------
- gr.Image(sources=["webcam"], streaming=True) como entrada.
- Una sola funcion `procesar_frame` que recibe el frame RGB y devuelve
  (frame_anotado_rgb, mensaje_estado).
- El video grabado se obtiene apretando un boton "Mostrar ultimo clip",
  porque actualizar un gr.Video cada frame causa problemas en Gradio 5.

Estado de la grabacion
----------------------
Usamos variables a nivel de modulo (no gr.State) porque en un Space de
Hugging Face cada usuario corre normalmente en su propio container y
porque gr.State + streaming dio problemas en Gradio 5.x. Si dos personas
se conectaran al mismo proceso, compartirian estado -- aceptable para
un demo de la cursada.

Flujo
-----
1. Mano abierta sostenida -> abre VideoWriter y empieza a grabar
2. Puno sostenido -> cierra VideoWriter y libera el archivo
3. Boton "Mostrar ultimo clip" -> trae el .mp4 al reproductor

Para correr local:
    python app.py
y abrir http://127.0.0.1:7860
"""

import time
from pathlib import Path

import cv2
import gradio as gr
import numpy as np

from gesture_detector import GestureDetector


# ----------------------------------------------------------------------
# Configuracion y estado de modulo
# ----------------------------------------------------------------------

FPS = 5.0

# Codec compatible con HTML5 video. Intentamos H264 (mejor metadata
# para el browser); si OpenCV no lo tiene en este sistema, fallback a
# mp4v (que graba pero el browser muestra NaN como duracion).
def _seleccionar_codec():
    for fourcc_name in ("avc1", "H264", "mp4v"):
        fourcc = cv2.VideoWriter_fourcc(*fourcc_name)
        # Probar creando un writer dummy en memoria temporal
        test_path = DIR_VIDEOS / "_test_codec.mp4"
        w = cv2.VideoWriter(str(test_path), fourcc, 5.0, (320, 240))
        ok = w.isOpened()
        w.release()
        if test_path.exists():
            test_path.unlink()
        if ok:
            print(f"[init] Codec seleccionado: {fourcc_name}")
            return fourcc
    raise RuntimeError("Ningun codec de video disponible")


# Lo evaluamos lazy para no tocar archivos al importar el modulo
_CODEC = None
def get_codec():
    global _CODEC
    if _CODEC is None:
        _CODEC = _seleccionar_codec()
    return _CODEC

# Carpeta dentro del proyecto para que Gradio pueda servir los videos
DIR_VIDEOS = Path(__file__).parent / "grabaciones"
DIR_VIDEOS.mkdir(exist_ok=True)

# Lazy init -- evita crear el detector si nadie usa la app
_detector = None

# Estado de la grabacion
_estado = "IDLE"            # IDLE | RECORDING
_writer = None
_archivo_actual = None
_inicio_grabacion = None
_ultimo_video = None
_tamano = None              # (w, h) del primer frame
_contador = 0               # para los prints de debug


def get_detector():
    global _detector
    if _detector is None:
        print("[init] Creando GestureDetector ...")
        _detector = GestureDetector(stable_frames=4)
        print("[init] Detector listo.")
    return _detector


# Maximo lado largo del frame para inferencia (mas chico = mas rapido)
TARGET_LARGO = 640


def _redimensionar(frame_rgb):
    """Reescala manteniendo aspect ratio si el lado largo supera TARGET_LARGO."""
    h, w = frame_rgb.shape[:2]
    if max(h, w) <= TARGET_LARGO:
        return frame_rgb
    if w >= h:
        nw = TARGET_LARGO
        nh = int(h * TARGET_LARGO / w)
    else:
        nh = TARGET_LARGO
        nw = int(w * TARGET_LARGO / h)
    return cv2.resize(frame_rgb, (nw, nh), interpolation=cv2.INTER_AREA)


# ----------------------------------------------------------------------
# Callback principal
# ----------------------------------------------------------------------

def procesar_frame(frame_rgb):
    """
    Entrada: ndarray RGB del webcam de Gradio (o None).
    Salida:  (frame_anotado_rgb, mensaje_estado)

    Nota: el video del clip ya NO se devuelve desde aca. En Gradio 5
    el gr.Video no se actualiza bien desde dentro del streaming.
    Por eso usamos un gr.Timer separado que tickea cada segundo y
    refresca el reproductor con la funcion mostrar_clip().
    """
    global _estado, _writer, _archivo_actual, _inicio_grabacion
    global _ultimo_video, _tamano, _contador

    if frame_rgb is None:
        return None, "### 🎥 Esperando camara..."

    _contador += 1

    try:
        frame_rgb_small = _redimensionar(frame_rgb)

        det = get_detector()
        frame_bgr = cv2.cvtColor(frame_rgb_small, cv2.COLOR_RGB2BGR)
        h, w = frame_bgr.shape[:2]
        if _tamano is None:
            _tamano = (w, h)

        resultado, anotado = det.process(frame_bgr)

        # Transiciones
        if _estado == "IDLE" and resultado.stable == "OPEN_HAND":
            _estado = "RECORDING"
            ts = time.strftime("%Y%m%d_%H%M%S")
            _archivo_actual = str(DIR_VIDEOS / f"clip_{ts}.mp4")
            _writer = cv2.VideoWriter(_archivo_actual, get_codec(), FPS, _tamano)
            _inicio_grabacion = time.time()
            print(f"[REC] Iniciado: {Path(_archivo_actual).name}")

        elif _estado == "RECORDING" and resultado.stable == "FIST":
            if _writer is not None:
                _writer.release()
                _writer = None
                _ultimo_video = _archivo_actual
                dur = time.time() - _inicio_grabacion
                print(
                    f"[STOP] {Path(_archivo_actual).name} ({dur:.1f}s) "
                    f"-> {_ultimo_video}"
                )
            _estado = "IDLE"

        # Grabar si corresponde
        if _estado == "RECORDING" and _writer is not None:
            _writer.write(anotado)
            t = time.time() - _inicio_grabacion
            cv2.circle(anotado, (w - 40, 40), 12, (0, 0, 255), -1)
            cv2.putText(
                anotado, f"REC {t:4.1f}s",
                (w - 180, 50), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 255), 2,
            )
            mensaje = f"### 🔴 Grabando ({t:.1f} s)"
        else:
            cv2.putText(
                anotado, "Mano abierta=REC  Puno=STOP",
                (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (240, 240, 240), 2,
            )
            if _ultimo_video:
                mensaje = "### ✅ Clip listo. Mostrá la mano abierta para grabar de nuevo."
            else:
                mensaje = "### 🖐️ Mostrá la palma abierta para empezar a grabar."

        anotado_rgb = cv2.cvtColor(anotado, cv2.COLOR_BGR2RGB)
        return anotado_rgb, mensaje

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return frame_rgb, f"### ❌ Error: {e}"


# Funcion que el timer dispara cada segundo para refrescar el reproductor.
# Devuelve el path del ultimo clip cerrado (o None si no hay).
def mostrar_clip():
    return _ultimo_video


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------

DESCRIPCION = """
# 🖐️✊ gesture-recorder

Graba video con la webcam **usando solo tu mano**:

1. Apretá **Record** sobre la cámara para activar el feed (paso obligatorio del navegador)
2. **Mano abierta** sostenida → empieza a grabar 🔴
3. **Puño cerrado** sostenido → detiene la grabación y muestra el clip ✅

MediaPipe Hands + OpenCV + Gradio · Laboratorio Integrador 2026
"""


def construir_app():
    with gr.Blocks(title="gesture-recorder") as demo:
        gr.Markdown(DESCRIPCION)

        with gr.Row():
            with gr.Column(scale=1):
                webcam = gr.Image(
                    sources=["webcam"],
                    streaming=True,
                    label="Cámara (entrada)",
                    type="numpy",
                )
            with gr.Column(scale=1):
                vista = gr.Image(
                    label="Vista anotada con gestos",
                    type="numpy",
                )

        estado_txt = gr.Markdown(
            "### 🖐️ Apretá Record en la cámara, luego mostrá la palma abierta."
        )

        clip = gr.Video(label="Último clip grabado", autoplay=True)

        # Stream: maneja camara -> vista anotada + estado
        webcam.stream(
            fn=procesar_frame,
            inputs=[webcam],
            outputs=[vista, estado_txt],
            time_limit=600,
            stream_every=0.2,
        )

        # Timer: cada 1 segundo refresca el reproductor de video.
        # Esto sortea la limitacion de Gradio 5 con gr.Video dentro del stream.
        timer = gr.Timer(value=1.0)
        timer.tick(fn=mostrar_clip, outputs=[clip])

    return demo


if __name__ == "__main__":
    print("Iniciando gesture-recorder ...")
    construir_app().launch(
        allowed_paths=[str(DIR_VIDEOS)],
    )
