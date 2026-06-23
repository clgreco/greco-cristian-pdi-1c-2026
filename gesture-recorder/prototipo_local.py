"""
prototipo_local.py
------------------

Prototipo local con OpenCV. Abre la webcam, detecta gestos en tiempo
real y graba un video cuando se detecta OPEN_HAND. Detiene la grabacion
cuando se detecta FIST.

Esto NO usa Gradio. Es para que pruebes la logica del proyecto en tu
maquina antes de empaquetar la version web.

Como correrlo
-------------
1. Crea un entorno virtual e instala dependencias:

    python -m venv .venv
    .venv\\Scripts\\activate         # Windows
    source .venv/bin/activate       # Mac / Linux
    pip install -r requirements.txt

2. Ejecutalo:

    python prototipo_local.py

3. Mostra la mano abierta a la camara para empezar a grabar.
   Mostra el puno cerrado para parar.
   Apreta 'q' para salir.

4. Los videos quedan en la carpeta ./grabaciones/
"""

import time
from pathlib import Path

import cv2

from gesture_detector import GestureDetector


# ----------------------------------------------------------------------
# Configuracion
# ----------------------------------------------------------------------
CARPETA_SALIDA = Path("grabaciones")
CARPETA_SALIDA.mkdir(exist_ok=True)

FPS_GRABACION = 20.0
CODEC = cv2.VideoWriter_fourcc(*"mp4v")  # mp4 portable


# ----------------------------------------------------------------------
# Maquina de estados
# ----------------------------------------------------------------------
# IDLE       -> esperando OPEN_HAND para empezar
# RECORDING  -> grabando frames, esperando FIST para terminar
# ----------------------------------------------------------------------

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la camara")

    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camara abierta: {ancho}x{alto}")

    detector = GestureDetector(stable_frames=8)
    estado = "IDLE"
    writer = None
    archivo_actual = None
    inicio_grabacion = None

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            # MediaPipe usa imagen "espejada" para que sea mas natural
            frame = cv2.flip(frame, 1)

            resultado, anotado = detector.process(frame)

            # Logica de transicion
            if estado == "IDLE" and resultado.stable == "OPEN_HAND":
                estado = "RECORDING"
                ts = time.strftime("%Y%m%d_%H%M%S")
                archivo_actual = CARPETA_SALIDA / f"gesto_{ts}.mp4"
                writer = cv2.VideoWriter(
                    str(archivo_actual), CODEC, FPS_GRABACION, (ancho, alto)
                )
                inicio_grabacion = time.time()
                print(f"[REC] Iniciado: {archivo_actual.name}")

            elif estado == "RECORDING" and resultado.stable == "FIST":
                estado = "IDLE"
                if writer is not None:
                    writer.release()
                    writer = None
                duracion = time.time() - inicio_grabacion
                print(f"[STOP] {archivo_actual.name}  ({duracion:.1f}s)")
                archivo_actual = None
                inicio_grabacion = None

            # Si estamos grabando, escribimos el frame en disco
            if estado == "RECORDING" and writer is not None:
                writer.write(anotado)

            # Overlay de estado
            if estado == "RECORDING":
                # Punto rojo + tiempo grabado
                cv2.circle(anotado, (ancho - 40, 40), 12, (0, 0, 255), -1)
                t = time.time() - inicio_grabacion
                cv2.putText(
                    anotado,
                    f"REC {t:5.1f}s",
                    (ancho - 180, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )
            else:
                cv2.putText(
                    anotado,
                    "Mano abierta para grabar",
                    (10, alto - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (200, 200, 200),
                    2,
                )

            cv2.imshow("gesture-recorder (prototipo local)", anotado)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        if writer is not None:
            writer.release()
        cap.release()
        detector.close()
        cv2.destroyAllWindows()
        print("Listo. Videos en:", CARPETA_SALIDA.resolve())


if __name__ == "__main__":
    main()
