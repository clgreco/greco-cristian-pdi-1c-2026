"""
TP006 — Parte 2 — Punto 4: Fotografía de simplicidad visual

Objetivo
--------
Construir una imagen donde el sujeto principal sea claramente identificable.
Sobre la imagen original IMG 11 (sansevieria en balcón / atardecer) se aplican
DOS estrategias de simplificación visual:

    Estrategia A — conversión a escala de grises (cv2.COLOR_RGB2GRAY)
                   elimina la información cromática para que la atención
                   se concentre en forma, textura y contraste.

    Estrategia B — acercamiento (crop)
                   recorta el encuadre original para aislar el sujeto
                   (la planta) eliminando el contexto urbano.

Salida
------
- punto04_simplicidad_original.jpg
- punto04_simplicidad_grises.jpg
- punto04_simplicidad_acercamiento.jpg
- punto04_simplicidad_marcas.jpg       (region del acercamiento marcada)
- punto04_comparacion.png              (original | grises | acercamiento)
- punto04_histogramas.png              (histograma RGB y de grises)
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

nombre_imagen = "IMG 11.jpeg"


# =========================
# 2. CARGA DE IMAGEN
# =========================

def cargar_rgb(ruta):
    """
    Carga una imagen con OpenCV y la convierte de BGR a RGB
    para visualizarla correctamente con Matplotlib.
    """
    imagen_bgr = cv2.imread(str(ruta), cv2.IMREAD_COLOR)
    if imagen_bgr is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")
    return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)


imagen_rgb = cargar_rgb(ruta_originales / nombre_imagen)
alto, ancho = imagen_rgb.shape[:2]


# =========================
# 3. ESTRATEGIA A — ESCALA DE GRISES
# =========================

# Eliminamos la información cromática para que el ojo se concentre
# en la textura y el contraste.
imagen_gris = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2GRAY)


# =========================
# 4. ESTRATEGIA B — ACERCAMIENTO
# =========================

# Recortamos el encuadre original aislando la sansevieria principal.
# Se eliminan los elementos contextuales (reja, edificios, suelo).
y1, y2 = int(alto * 0.25), int(alto * 0.80)
x1, x2 = int(ancho * 0.30), int(ancho * 0.98)

imagen_acercamiento = imagen_rgb[y1:y2, x1:x2]


# =========================
# 5. MARCAS SOBRE LA ORIGINAL
# =========================

imagen_marcada = imagen_rgb.copy()
cv2.rectangle(imagen_marcada, (x1, y1), (x2, y2), (255, 200, 0), 8)
cv2.putText(
    imagen_marcada,
    "Acercamiento",
    (x1 + 10, y1 + 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.3,
    (255, 200, 0),
    4,
)


# =========================
# 6. VISUALIZACION
# =========================

plt.figure(figsize=(16, 8))

plt.subplot(1, 3, 1)
plt.imshow(imagen_rgb)
plt.title("Original — IMG 11", fontweight="bold")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(imagen_gris, cmap="gray")
plt.title("Estrategia A — escala de grises", fontweight="bold")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(imagen_acercamiento)
plt.title("Estrategia B — acercamiento", fontweight="bold")
plt.axis("off")

plt.tight_layout()
plt.savefig(ruta_procesadas / "punto04_comparacion.png",
            bbox_inches="tight", dpi=150)
plt.close()


# =========================
# 7. HISTOGRAMAS
# =========================

plt.figure(figsize=(14, 4))

# Histograma RGB original
plt.subplot(1, 2, 1)
colores = ("red", "green", "blue")
for i, color in enumerate(colores):
    histograma = cv2.calcHist(
        [imagen_rgb], [i], None, [256], [0, 256]
    )
    plt.plot(histograma, color=color)
plt.title("Histograma RGB — original", fontweight="bold")
plt.xlabel("Intensidad")
plt.ylabel("Cantidad de píxeles")

# Histograma escala de grises
plt.subplot(1, 2, 2)
plt.hist(imagen_gris.ravel(), bins=256, range=(0, 256), color="black")
plt.title("Histograma escala de grises", fontweight="bold")
plt.xlabel("Intensidad")
plt.ylabel("Cantidad de píxeles")

plt.tight_layout()
plt.savefig(ruta_procesadas / "punto04_histogramas.png",
            bbox_inches="tight", dpi=150)
plt.close()


# =========================
# 8. EXPORTACION FINAL
# =========================

cv2.imwrite(
    str(ruta_procesadas / "punto04_simplicidad_original.jpg"),
    cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2BGR),
)

cv2.imwrite(
    str(ruta_procesadas / "punto04_simplicidad_grises.jpg"),
    imagen_gris,
)

cv2.imwrite(
    str(ruta_procesadas / "punto04_simplicidad_acercamiento.jpg"),
    cv2.cvtColor(imagen_acercamiento, cv2.COLOR_RGB2BGR),
)

cv2.imwrite(
    str(ruta_procesadas / "punto04_simplicidad_marcas.jpg"),
    cv2.cvtColor(imagen_marcada, cv2.COLOR_RGB2BGR),
)

print("Punto 4 — Simplicidad visual: archivos generados en", ruta_procesadas)
