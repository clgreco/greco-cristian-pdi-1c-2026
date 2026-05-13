"""
TP006 — Parte 2 — Punto 6: Punto de vista y construcción narrativa

Objetivo
--------
Explorar cómo la posición de la cámara modifica la escala, el contexto
y la información visual de la escena.

    Vista A — IMG 10 (vista desde arriba / ligeramente elevada)
        Contexto: ciudad. Se observa el conjunto de techos y edificios
        del barrio detrás de la reja. La planta se integra al paisaje
        urbano.
        Edición: se recorta el 15% izquierdo de la imagen para eliminar
        un pie que aparecía en la zona inferior izquierda y distraía
        del sujeto.

    Vista B — IMG 9 (vista frontal)
        Contexto: amanecer. La cámara baja a la altura del sujeto y
        deja ver la línea del horizonte iluminada por la luz cálida
        del amanecer. La planta dialoga con el cielo.

Salida
------
- punto06_IMG10_original.jpg
- punto06_IMG10_marcas.jpg
- punto06_vista_A_cenital.jpg
- punto06_vista_B_frontal_amanecer.jpg
- punto06_comparacion.png
- punto06_esquema_camara.png
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

nombre_vista_a = "IMG 10.jpeg"   # vista desde arriba / contexto ciudad
nombre_vista_b = "IMG 9.jpeg"    # vista frontal / contexto amanecer


# =========================
# 2. CARGA DE IMAGENES
# =========================

def cargar_rgb(ruta):
    """Carga una imagen y la convierte de BGR a RGB."""
    imagen_bgr = cv2.imread(str(ruta), cv2.IMREAD_COLOR)
    if imagen_bgr is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")
    return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)


vista_a_full = cargar_rgb(ruta_originales / nombre_vista_a)
vista_b_rgb = cargar_rgb(ruta_originales / nombre_vista_b)

H_a, W_a = vista_a_full.shape[:2]


# =========================
# 3. VISTA A — RECORTE 15% IZQUIERDO (sacar pie visible)
# =========================

x_descartado = int(W_a * 0.15)
vista_a_rgb = vista_a_full[:, x_descartado:]


# =========================
# 4. MARCAS SOBRE IMG 10 (zona descartada + encuadre final)
# =========================

vista_a_marcas = vista_a_full.copy()

# Rectángulo rojo: zona descartada (15% izquierdo, contiene el pie)
cv2.rectangle(
    vista_a_marcas,
    (0, 0),
    (x_descartado, H_a - 1),
    (220, 30, 30),
    8,
)
cv2.putText(
    vista_a_marcas,
    "Descartado (15%)",
    (20, 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.1,
    (220, 30, 30),
    4,
)

# Rectángulo verde: encuadre final
cv2.rectangle(
    vista_a_marcas,
    (x_descartado, 0),
    (W_a - 1, H_a - 1),
    (0, 200, 0),
    6,
)
cv2.putText(
    vista_a_marcas,
    "Encuadre final",
    (x_descartado + 20, 100),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.1,
    (0, 200, 0),
    4,
)


# =========================
# 5. ESQUEMA — DIRECCION DE LAS DOS CAMARAS
# =========================

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.set_title(
    "Esquema — Dos puntos de vista del mismo sujeto",
    fontweight="bold",
)

# Sujeto (planta)
ax.add_patch(plt.Circle((5, 2.5), 0.4, color="green"))
ax.text(5, 1.8, "Planta\n(sujeto)", ha="center")

# Cámara A — vista cenital
ax.add_patch(plt.Rectangle((4.7, 5.0), 0.6, 0.4, color="red"))
ax.annotate(
    "",
    xy=(5, 3),
    xytext=(5, 4.9),
    arrowprops=dict(arrowstyle="->", color="red", lw=2),
)
ax.text(
    5.5, 5.2,
    "Camara A - vista desde arriba\n(contexto = ciudad)",
    color="red",
)

# Cámara B — vista frontal
ax.add_patch(plt.Rectangle((1.5, 2.3), 0.6, 0.4, color="blue"))
ax.annotate(
    "",
    xy=(4.5, 2.5),
    xytext=(2.2, 2.5),
    arrowprops=dict(arrowstyle="->", color="blue", lw=2),
)
ax.text(
    0.5, 1.5,
    "Camara B - vista frontal\n(contexto = amanecer)",
    color="blue",
)

plt.tight_layout()
plt.savefig(
    ruta_procesadas / "punto06_esquema_camara.png",
    bbox_inches="tight",
    dpi=150,
)
plt.close()


# =========================
# 6. COMPARACION
# =========================

plt.figure(figsize=(14, 8))

plt.subplot(1, 2, 1)
plt.imshow(vista_a_rgb)
plt.title("Vista A — desde arriba (contexto: ciudad)", fontweight="bold")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(vista_b_rgb)
plt.title("Vista B — frontal (contexto: amanecer)", fontweight="bold")
plt.axis("off")

plt.tight_layout()
plt.savefig(
    ruta_procesadas / "punto06_comparacion.png",
    bbox_inches="tight",
    dpi=150,
)
plt.close()


# =========================
# 7. EXPORTACION FINAL
# =========================

cv2.imwrite(
    str(ruta_procesadas / "punto06_IMG10_original.jpg"),
    cv2.cvtColor(vista_a_full, cv2.COLOR_RGB2BGR),
)
cv2.imwrite(
    str(ruta_procesadas / "punto06_IMG10_marcas.jpg"),
    cv2.cvtColor(vista_a_marcas, cv2.COLOR_RGB2BGR),
)
cv2.imwrite(
    str(ruta_procesadas / "punto06_vista_A_cenital.jpg"),
    cv2.cvtColor(vista_a_rgb, cv2.COLOR_RGB2BGR),
)
cv2.imwrite(
    str(ruta_procesadas / "punto06_vista_B_frontal_amanecer.jpg"),
    cv2.cvtColor(vista_b_rgb, cv2.COLOR_RGB2BGR),
)

print("Punto 6 — Punto de vista: archivos generados en", ruta_procesadas)
