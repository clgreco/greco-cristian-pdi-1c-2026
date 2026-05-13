"""
TP006 - Parte 2 - Fotografia de simplicidad visual (Anexo tecnico)
Conversion a escala de grises (cv2.COLOR_BGR2GRAY)
Elimina informacion cromatica - el ojo se concentra en textura,
forma y contraste.

Script minimo obligatorio. La version completa con histogramas
y acercamiento se encuentra en simplicidad_visual.py
"""
import cv2

img = cv2.imread("C:/Users/Cristian/Desktop/greco-cristian-pdi-1c-2026/006_fotografia_digital/imagenes/originales/IMG 11.jpeg")
gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("C:/Users/Cristian/Desktop/greco-cristian-pdi-1c-2026/006_fotografia_digital/imagenes/procesadas/punto04_simplicidad_grises.jpg", gris)
print("Imagen en escala de grises guardada.")
