---
title: Gesture Recorder
emoji: ✊
colorFrom: red
colorTo: blue
sdk: gradio
sdk_version: 5.30.0
app_file: app.py
pinned: false
license: mit
---

# gesture-recorder

Aplicación que **graba video controlada por gestos de la mano**, usando
MediaPipe Hands. La grabación se inicia mostrando la palma abierta a la
cámara y se detiene cerrando el puño. El video resultante queda
disponible para descargar.

> **Materia:** Procesamiento de Imagenes
> **Tecnicatura:** Desarrollo de Inteligencia Artificial
> **Entrega:** Laboratorio Integrador — 23 / junio / 2026
> **Línea elegida:** Línea 1 — MediaPipe para detección de pose (manos)
> **Integrante:** Cristian Greco

---

## Cómo usar la aplicación

1. Apretá **Record** sobre el feed de la cámara (paso obligatorio del
   navegador para activar el acceso al stream).
2. Mostrá la **palma abierta** durante ~1 segundo → arranca la grabación.
3. Cerrá el **puño** durante ~1 segundo → corta la grabación y aparece
   el clip listo para reproducir y descargar.
4. Click derecho sobre el video → "Guardar video como…" para bajarlo.

---

## Cómo funciona

1. **Captura:** Gradio recibe frames de la webcam a ~5 fps.
2. **Detección de gestos:** MediaPipe Hands (`mediapipe.tasks.python.vision`)
   extrae los 21 landmarks de la mano. Un clasificador geométrico cuenta
   cuántos de los 4 dedos largos están extendidos: 4 → `OPEN_HAND`,
   0 → `FIST`, intermedio → `NONE`.
3. **Filtro de estabilidad:** un buffer circular exige que el mismo
   gesto aparezca durante 4 frames consecutivos antes de aceptarlo.
4. **Máquina de estados:**

```
IDLE ──── OPEN_HAND estable ───►  RECORDING
 ▲                                     │
 └────────── FIST estable ─────────────┘
```

5. **Grabación:** `cv2.VideoWriter` con codec H264 (`avc1`), fallback a
   `mp4v` si H264 no está disponible.
6. **Refresco del clip:** un `gr.Timer` tickea cada segundo y actualiza
   el reproductor con el último clip — workaround para una limitación
   de Gradio 5.

---

## Estructura del repositorio

```
gesture-recorder/
├── app.py                  ← Aplicación Gradio (la que se despliega)
├── prototipo_local.py      ← Versión OpenCV para probar con webcam
├── gesture_detector.py     ← Módulo reusable de detección de gestos
├── requirements.txt        ← Dependencias pineadas
├── README.md               ← Este archivo
├── .gitignore
└── assets/                 ← GIF y screenshots de demo
```

`hand_landmarker.task` se descarga automáticamente al primer uso (~7 MB).

---

## Cómo correrlo localmente

```bash
git clone https://github.com/<tu-usuario>/gesture-recorder.git
cd gesture-recorder
py -3.12 -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py
# Abrí http://127.0.0.1:7860
```

---

## Decisiones técnicas

| Decisión | Por qué |
|----------|---------|
| MediaPipe Hands (no Pose) | El sujeto es la mano; Hands tiene 21 keypoints específicos. |
| API `mediapipe.tasks` (no la legacy `solutions`) | La legacy se eliminó de los wheels de Python 3.13. |
| Clasificador geométrico | No hace falta ML: comparar `tip.y < pip.y` por dedo alcanza. |
| Ignoramos el pulgar | Su clasificación depende de handedness, que MediaPipe a veces equivoca. |
| Codec H264 con fallback a mp4v | H264 produce mp4 con duración legible por HTML5 video. |
| `gr.Timer` para actualizar `gr.Video` | Workaround a una limitación de Gradio 5. |
| Variables a nivel de módulo (no `gr.State`) | `gr.State` + streaming es inestable en Gradio 5. |

---

## Limitaciones conocidas
- Limitaciones del navegador, se debe oprimir el boton record para iniciar la grabación.
- En Hugging Face Spaces gratis (CPU), el frame rate efectivo es ~5 fps.
- No graba audio, solo video.
- Una sola mano por vez.
- Si dos personas comparten el mismo container del Space, comparten estado.

---

## Despliegue

🤗 **Hugging Face Space:** https://huggingface.co/spaces/clgreco/gesture-recorder
📦 **Repositorio:** https://github.com/clgreco/greco-cristian-pdi-1c-2026/tree/main/gesture-recorder

