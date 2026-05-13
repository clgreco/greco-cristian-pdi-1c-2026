"""
TP006 — Parte 1 — Cámara oscura y procesamiento digital
Código principal requerido por el TP (Anexo técnico).

Proceso:
  1. Cargar imagen de cámara oscura
  2. Invertir (flip -1) — la proyección llega girada 180°
  3. Recortar zona de proyección útil (ROI)
  4. Convertir a HSV
  5. Separar canales H, S, V
  6. Ecualizar ÚNICAMENTE el canal V
  7. Recomponer y guardar
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

img_bgr = cv2.imread("C:/Users/Cristian/Desktop/greco-cristian-pdi-1c-2026/006_fotografia_digital/imagenes/originales/img_camara_oscura1.jpeg")
img_bgr = cv2.flip(img_bgr, -1)
img_bgr = img_bgr[220:720, 50:910]
hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
v_eq = cv2.equalizeHist(v)
hsv_eq = cv2.merge([h, s, v_eq])
img_eq_bgr = cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)
cv2.imwrite("C:/Users/Cristian/Desktop/greco-cristian-pdi-1c-2026/006_fotografia_digital/imagenes/procesadas/camara_oscura_ecualizada_v.jpg", img_eq_bgr)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fig.suptitle("Canal V — Antes vs Después de equalizeHist", fontsize=13)
axes[0].fill_between(range(256), cv2.calcHist([v],[0],None,[256],[0,256]).flatten(), color='darkorange', alpha=0.8)
axes[0].set_title("V original"); axes[0].set_xlabel("Intensidad"); axes[0].set_ylabel("Frecuencia")
axes[1].fill_between(range(256), cv2.calcHist([v_eq],[0],None,[256],[0,256]).flatten(), color='steelblue', alpha=0.8)
axes[1].set_title("V ecualizado"); axes[1].set_xlabel("Intensidad")
axes[2].fill_between(range(256), cv2.calcHist([v],[0],None,[256],[0,256]).flatten(), color='darkorange', alpha=0.5, label='Antes')
axes[2].fill_between(range(256), cv2.calcHist([v_eq],[0],None,[256],[0,256]).flatten(), color='steelblue', alpha=0.5, label='Despues')
axes[2].set_title("Comparacion"); axes[2].legend()
plt.tight_layout()
plt.savefig("C:/Users/Cristian/Desktop/greco-cristian-pdi-1c-2026/006_fotografia_digital/imagenes/procesadas/histogramas_canal_v.jpg", dpi=150, bbox_inches='tight')
print("Pipeline completo ejecutado.")
