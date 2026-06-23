"""
gesture_detector.py
-------------------

Modulo reutilizable de deteccion de gestos con MediaPipe Tasks API
(la API nueva, que funciona con Python 3.13).

Reconoce dos gestos sobre una mano:

    OPEN_HAND  ->  los 4 dedos largos + el pulgar estan extendidos
    FIST       ->  los 4 dedos largos estan flexionados

Se basa en una regla geometrica simple: para cada dedo se compara la
posicion 'y' del TIP (punta) contra el PIP (segunda articulacion). Si el
TIP esta mas arriba que el PIP, ese dedo esta extendido. Para el pulgar
usamos la coordenada 'x' porque crece hacia el costado.

Para evitar parpadeos en la deteccion, la clase GestureDetector mantiene
un buffer: un gesto solo se reporta como "estable" cuando aparece N
frames consecutivos.

La primera vez que se ejecuta, descarga automaticamente el modelo
hand_landmarker.task (~7 MB) desde Google Storage. Las siguientes
ejecuciones lo levantan de disco.
"""

import time
import urllib.request
from collections import deque
from dataclasses import dataclass
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision


# Indices oficiales de MediaPipe para los landmarks de la mano
# https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
WRIST = 0
THUMB_TIP, THUMB_IP = 4, 3
INDEX_TIP, INDEX_PIP = 8, 6
MIDDLE_TIP, MIDDLE_PIP = 12, 10
RING_TIP, RING_PIP = 16, 14
PINKY_TIP, PINKY_PIP = 20, 18

# Conexiones para dibujar el esqueleto de la mano (21 keypoints)
HAND_CONNECTIONS = [
    # Pulgar
    (0, 1), (1, 2), (2, 3), (3, 4),
    # Indice
    (0, 5), (5, 6), (6, 7), (7, 8),
    # Medio
    (5, 9), (9, 10), (10, 11), (11, 12),
    # Anular
    (9, 13), (13, 14), (14, 15), (15, 16),
    # Menique
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20),
]

# Modelo oficial de MediaPipe (~7 MB)
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
)
MODEL_PATH = Path(__file__).parent / "hand_landmarker.task"


def _asegurar_modelo():
    """Descarga el .task la primera vez que se necesita."""
    if MODEL_PATH.exists():
        return MODEL_PATH
    print(f"Descargando modelo de MediaPipe a {MODEL_PATH.name} ...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"Modelo descargado ({MODEL_PATH.stat().st_size / 1024:.0f} KB)")
    return MODEL_PATH


@dataclass
class GestureResult:
    """Resultado de un frame procesado."""
    raw: str          # gesto crudo de este frame: OPEN_HAND, FIST, NONE
    stable: str       # gesto estable (paso el filtro del buffer)
    fingers_up: int   # cantidad de dedos extendidos (debug)


class GestureDetector:
    """
    Detector de gestos para una sola mano (API Tasks).

    Parametros
    ----------
    stable_frames : int
        Cantidad de frames consecutivos con el mismo gesto que se
        requieren para considerarlo "estable". Default 6 (a 30 fps,
        ~200 ms).
    detection_confidence : float
        Umbral de MediaPipe para detectar la mano.
    tracking_confidence : float
        Umbral de MediaPipe para seguir la mano entre frames.
    """

    def __init__(
        self,
        stable_frames: int = 6,
        detection_confidence: float = 0.5,
        tracking_confidence: float = 0.5,
    ):
        modelo = _asegurar_modelo()

        base_options = mp_python.BaseOptions(
            model_asset_path=str(modelo)
        )
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

        self.buffer = deque(maxlen=stable_frames)
        self.last_stable = "NONE"
        self._t0 = time.time()

    # ------------------------------------------------------------------
    # API publica
    # ------------------------------------------------------------------
    def process(self, frame_bgr):
        """
        Procesa un frame BGR y devuelve (GestureResult, frame_anotado).
        """
        h, w = frame_bgr.shape[:2]

        # MediaPipe Tasks trabaja con su tipo mp.Image en RGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # Timestamp en milisegundos desde que se creo el detector
        ts_ms = int((time.time() - self._t0) * 1000)

        result = self.detector.detect_for_video(mp_image, ts_ms)

        annotated = frame_bgr.copy()
        raw = "NONE"
        fingers_up = 0

        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]
            # handedness: Right / Left
            handedness = result.handedness[0][0].category_name

            self._dibujar_esqueleto(annotated, landmarks, w, h)
            raw, fingers_up = self._classify(landmarks, handedness)

        # Buffer de estabilidad
        self.buffer.append(raw)
        if len(self.buffer) == self.buffer.maxlen and len(set(self.buffer)) == 1:
            self.last_stable = self.buffer[0]

        # Overlay con info de debug
        cv2.putText(
            annotated,
            f"Gesto: {raw}  (dedos={fingers_up})",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0) if raw != "NONE" else (0, 0, 255),
            2,
        )
        cv2.putText(
            annotated,
            f"Estable: {self.last_stable}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2,
        )

        return GestureResult(raw=raw, stable=self.last_stable,
                             fingers_up=fingers_up), annotated

    def close(self):
        if self.detector is not None:
            self.detector.close()
            self.detector = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _dibujar_esqueleto(img, landmarks, w, h):
        """Dibuja las conexiones y los keypoints sobre la imagen."""
        # Convertir a pixeles
        pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
        # Conexiones
        for a, b in HAND_CONNECTIONS:
            cv2.line(img, pts[a], pts[b], (255, 255, 255), 2)
        # Puntos
        for x, y in pts:
            cv2.circle(img, (x, y), 4, (0, 200, 255), -1)
            cv2.circle(img, (x, y), 4, (0, 0, 0), 1)

    @staticmethod
    def _classify(landmarks, handedness: str):
        """
        Devuelve (gesto, cantidad_de_dedos_extendidos_largos).

        Regla simplificada: solo contamos los 4 dedos largos (indice,
        medio, anular, menique). Ignoramos el pulgar porque su
        clasificacion depende de handedness y a veces MediaPipe se
        equivoca con eso.

        Un dedo esta "extendido" si su TIP esta mas arriba (y mas chico)
        que su PIP en coordenadas normalizadas.

        OPEN_HAND  -> 4 dedos largos extendidos
        FIST       -> 0 dedos largos extendidos
        NONE       -> entre 1 y 3 extendidos (transicion / ambiguo)
        """
        lm = landmarks

        index_up = lm[INDEX_TIP].y < lm[INDEX_PIP].y
        middle_up = lm[MIDDLE_TIP].y < lm[MIDDLE_PIP].y
        ring_up = lm[RING_TIP].y < lm[RING_PIP].y
        pinky_up = lm[PINKY_TIP].y < lm[PINKY_PIP].y

        fingers_up = sum([index_up, middle_up, ring_up, pinky_up])

        if fingers_up == 4:
            return "OPEN_HAND", fingers_up
        if fingers_up == 0:
            return "FIST", fingers_up
        return "NONE", fingers_up
