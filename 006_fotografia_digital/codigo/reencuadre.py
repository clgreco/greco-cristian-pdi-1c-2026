"""
TP006 — Parte 2 — Punto 5: Reencuadre y reinterpretación

Objetivo
--------
Demostrar que cambiar el encuadre modifica el significado de la imagen.
Sobre las dos tomas amplias del mismo sujeto (sansevieria en balcón) se
producen dos reencuadres con narrativas distintas:

    Reencuadre A — narrativa "AMANECER"
        Partiendo de IMG 47 se conserva el tercio superior:
        protagonismo del cielo y del horizonte urbano al amanecer;
        la planta se vuelve elemento secundario.

    Reencuadre B — narrativa "PLANTA"
        Partiendo de IMG 43 se conserva la mitad inferior derecha:
        la sansevieria ocupa toda la lectura; el contexto urbano
        desaparece.
"""

from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt


# =========================
# 1. RUTAS
# =========================

ruta_originales = Path("C:/Users/Cristian/Desktop/greco-cristian-pdi-1c-2026/006_fotografia_digital/imagenes/originales")
ruta_procesadas = Path("C:/Users/Cristian/Desktop/greco-cristian-pdi-1c-2026/006_fotografia_digital/imagenes/procesadas")
ruta_procesadas.mkdir(parents=True, exist_ok=True)

nombre_imagen_amanecer = "IMG 47.jpeg"
nombre_imagen_planta = "IMG 43.jpeg"


# =========================
# 2. CARGA DE IMAGENES
# =========================

def cargar_rgb(ruta):
    """Carga una imagen y la convierte de BGR a RGB."""
    imagen_bgr = cv2.imread(str(ruta), cv2.IMREAD_COLOR)
    if imagen_bgr is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")
    return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)


img_amanecer_rgb = cargar_rgb(ruta_originales / nombre_imagen_amanecer)
img_planta_rgb = cargar_rgb(ruta_originales / nombre_imagen_planta)

H_am, W_am = img_amanecer_rgb.shape[:2]
H_pl, W_pl = img_planta_rgb.shape[:2]


# =========================
# 3. RECORTE A — NARRATIVA AMANECER (IMG 47)
# =========================

y1_a, y2_a = 0, int(H_am * 0.55)
x1_a, x2_a = 0, W_am

recorte_amanecer = img_amanecer_rgb[y1_a:y2_a, x1_a:x2_a]


# =========================
# 4. RECORTE B — NARRATIVA PLANTA (IMG 43)
# =========================

y1_b, y2_b = int(H_pl * 0.35), H_pl
x1_b, x2_b = int(W_pl * 0.25), W_pl

recorte_planta = img_planta_rgb[y1_b:y2_b, x1_b:x2_b]


# =========================
# 5. MARCAS SOBRE LAS ORIGINALES
# =========================

img_amanecer_marcas = img_amanecer_rgb.copy()
cv2.rectangle(
    img_amanecer_marcas,
    (x1_a, y1_a),
    (x2_a - 1, y2_a),
    (255, 100, 0),
    8,
)
cv2.putText(
    img_amanecer_marcas,
    "Recorte A - Amanecer",
    (x1_a + 20, y1_a + 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.3,
    (255, 100, 0),
    4,
)

img_planta_marcas = img_planta_rgb.copy()
cv2.rectangle(
    img_planta_marcas,
    (x1_b, y1_b),
    (x2_b - 1, y2_b - 1),
    (0, 200, 80),
    8,
)
cv2.putText(
    img_planta_marcas,
    "Recorte B - Planta",
    (x1_b + 20, y1_b + 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.3,
    (0, 200, 80),
    4,
)


# =========================
# 6. VISUALIZACION
# =========================

plt.figure(figsize=(16, 10))

plt.subplot(2, 2, 1)
plt.imshow(img_amanecer_marcas)
plt.title("Original IMG 47 + Recorte A (amanecer)", fontweight="bold")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(img_planta_marcas)
plt.title("Original IMG 43 + Recorte B (planta)", fontweight="bold")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(recorte_amanecer)
plt.title("Recorte A - narrativa AMANECER", fontweight="bold")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(recorte_planta)
plt.title("Recorte B - narrativa PLANTA", fontweight="bold")
plt.axis("off")

plt.tight_layout()
plt.savefig(ruta_procesadas / "punto05_comparacion.png",
            bbox_inches="tight", dpi=150)
plt.close()


# =========================
# 7. EXPORTACION FINAL
# =========================

cv2.imwrite(
    str(ruta_procesadas / "punto05_original_amanecer_IMG47.jpg"),
    cv2.cvtColor(img_amanecer_rgb, cv2.COLOR_RGB2BGR),
)
cv2.imwrite(
    str(ruta_procesadas / "punto05_original_planta_IMG43.jpg"),
    cv2.cvtColor(img_planta_rgb, cv2.COLOR_RGB2BGR),
)
cv2.imwrite(
    str(ruta_procesadas / "punto05_recorte_A_amanecer.jpg"),
    cv2.cvtColor(recorte_amanecer, cv2.COLOR_RGB2BGR),
)
cv2.imwrite(
    str(ruta_procesadas / "punto05_recorte_B_planta.jpg"),
    cv2.cvtColor(recorte_planta, cv2.COLOR_RGB2BGR),
)
cv2.imwrite(
    str(ruta_procesadas / "punto05_marcas_amanecer.jpg"),
    cv2.cvtColor(img_amanecer_marcas, cv2.COLOR_RGB2BGR),
)
cv2.imwrite(
    str(ruta_procesadas / "punto05_marcas_planta.jpg"),
    cv2.cvtColor(img_planta_marcas, cv2.COLOR_RGB2BGR),
)

print("Punto 5 - Reencuadre: archivos generados en", ruta_procesadas)
