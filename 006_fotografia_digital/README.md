# TP006 — Fotografía Digital
## De la cámara oscura a la imagen intencional
### Óptica, composición y postproceso en fotografía digital

**Materia:** Introducción al Procesamiento Digital de Imágenes · 2026
**Alumno:** Cristian Greco
**Entrega:** Repositorio GitHub

---

## Estructura del repositorio

```
006_fotografia_digital/
│
├── README.md                          ← este archivo
├── presentacion.pdf                   ← entrega principal (Partes 1 + 2 + 3)
│
├── imagenes/
│   ├── originales/                    ← 48 capturas sin procesar
│   ├── procesadas/                    ← figuras generadas por scripts
│   └── descartes/                     ← tomas descartadas con criterio
│
├── codigo/
│   ├── ecualizacion_hsv.py            ← Parte 1 · cámara oscura + HSV
│   ├── escala_grises.py               ← Parte 2 · script mínimo grises
│   ├── simplicidad_visual.py          ← Parte 2 · punto 4 completo
│   ├── reencuadre.py                  ← Parte 2 · punto 5 completo
│   └── punto_de_vista.py              ← Parte 2 · punto 6 completo
│
└── recursos/
    └── (referencias opcionales)
```

Cada script genera sus salidas dentro de `imagenes/procesadas/` y puede
ejecutarse de forma independiente desde la carpeta `codigo/`.

---

## Parte 1 — Cámara oscura y procesamiento digital

### Dispositivo
Caja de cartón con orificio (pinhole). La **propagación rectilínea de la luz**
genera una proyección invertida 180° en la pared opuesta (plano de imagen).

### Pipeline de procesamiento (`ecualizacion_hsv.py`)

| Paso | Operación | Código |
|------|-----------|--------|
| 1 | Invertir imagen | `cv2.flip(img, -1)` |
| 2 | Recortar ROI | `img[220:720, 50:910]` |
| 3 | Convertir a HSV | `cv2.cvtColor(img, cv2.COLOR_BGR2HSV)` |
| 4 | Separar canales | `h, s, v = cv2.split(hsv)` |
| 5 | Ecualizar canal V | `v_eq = cv2.equalizeHist(v)` |
| 6 | Recomponer | `cv2.merge([h, s, v_eq])` |

### ¿Por qué ecualizar V y no RGB?
Ecualizar los canales RGB por separado introduce dominantes de color
artificiales. Operar solo sobre V (brillo) en HSV preserva el matiz (H)
y la saturación (S) originales.

---

## Parte 2 — Composición y lenguaje visual
**Sujeto:** Sansevieria en balcón · Buenos Aires · Amanecer / hora dorada

### 4. Simplicidad visual — `simplicidad_visual.py`
**Imagen base:** `IMG 11.jpeg`

| Estrategia | Operación | Efecto compositivo |
|-----------|-----------|--------------------|
| A · escala de grises | `cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)` | Elimina la información cromática; protagonismo de la textura y el contraste |
| B · acercamiento | `img[0.25H:0.80H, 0.30W:0.98W]` | Aísla la sansevieria; desaparece el contexto urbano |

Salidas:
- `punto04_simplicidad_original.jpg`
- `punto04_simplicidad_grises.jpg`
- `punto04_simplicidad_acercamiento.jpg`
- `punto04_simplicidad_marcas.jpg`
- `punto04_comparacion.png`
- `punto04_histogramas.png`

### 5. Reencuadre y reinterpretación — `reencuadre.py`
**Imágenes base:** `IMG 47.jpeg` (amanecer) · `IMG 43.jpeg` (planta)

| Reencuadre | Origen | Lo que aparece | Lo que desaparece |
|-----------|--------|---------------|-------------------|
| A · narrativa AMANECER | IMG 47, tercio superior | Cielo, horizonte de Buenos Aires, hora dorada | La planta como sujeto |
| B · narrativa PLANTA | IMG 43, mitad inferior derecha | Sansevieria con detalle y textura | El cielo, la ciudad |

Salidas:
- `punto05_original_amanecer_IMG47.jpg`, `punto05_original_planta_IMG43.jpg`
- `punto05_recorte_A_amanecer.jpg`, `punto05_recorte_B_planta.jpg`
- `punto05_marcas_amanecer.jpg`, `punto05_marcas_planta.jpg`
- `punto05_comparacion.png`

### 6. Punto de vista y construcción narrativa — `punto_de_vista.py`
**Imágenes base:** `IMG 10.jpeg` (vista desde arriba) · `IMG 9.jpeg` (frontal)

| Vista | Posición de la cámara | Contexto que aporta |
|------|----------------------|--------------------|
| A · desde arriba | Cámara elevada apuntando a la maceta | El conjunto urbano / techos / ciudad |
| B · frontal | Cámara a la altura del sujeto | El amanecer detrás del horizonte |

**Edición sobre IMG 10:** se recorta el **15% izquierdo** de la imagen para
eliminar un pie que aparecía en la zona inferior izquierda y distraía del
sujeto (`img[:, int(W*0.15):]`).

Salidas:
- `punto06_IMG10_original.jpg`, `punto06_IMG10_marcas.jpg`
- `punto06_vista_A_cenital.jpg`, `punto06_vista_B_frontal_amanecer.jpg`
- `punto06_comparacion.png`, `punto06_esquema_camara.png`

### 7. Luz — Tres momentos del atardecer

| Momento | Temperatura | Efecto |
|---------|-------------|--------|
| Hora azul (inicial) | Fría / difusa | Aplana el volumen; planta como silueta |
| Primeros cálidos | Transición azul→naranja | Expectativa; luz rasante empieza a modelar |
| Hora dorada | Cálida / lateral rasante | Revela textura y volumen; efecto escultórico |

### 8. Selección crítica
**Imagen elegida:** hora dorada con bokeh moderado.
**Criterio:** sujeto nítido, fondo desenfocado que sugiere el atardecer sin
competir, luz que revela textura sin quemar ni oscurecer.

---

## Parte 3 — Reflexión final

**¿Qué aprendiste sobre mirar?**
Mirar fotográficamente implica seleccionar activamente. La diferencia entre
imágenes posibles es la intención: altura, momento, encuadre.

**¿Diferencia entre registrar y construir una imagen?**
Registrar es capturar lo que hay. Construir es decidir cómo presentarlo.
El postproceso es parte de esa construcción.

**¿Relación entre óptica, percepción y composición?**
La óptica determina la profundidad de campo. La percepción decide qué es
figura y fondo. La composición organiza los elementos para guiar esa
percepción. Las tres son inseparables.

**¿Cómo modifica el postproceso la lectura?**
La conversión a grises transforma una imagen colorida en gráfica y
atemporal. El reencuadre modifica el sujeto sin cambiar la escena. El
postproceso no es corrección: es decisión creativa.

---

## Cómo ejecutar el código

```bash
cd codigo
python3 ecualizacion_hsv.py       # Parte 1
python3 simplicidad_visual.py     # Punto 4
python3 reencuadre.py             # Punto 5
python3 punto_de_vista.py         # Punto 6
```

Dependencias: `opencv-python`, `numpy`, `matplotlib`.

---

## Criterios de evaluación

| Criterio | Peso |
|----------|------|
| Comprensión óptica y cámara oscura | 20% |
| Procesamiento HSV y operaciones digitales | 15% |
| Composición y lenguaje visual | 25% |
| Uso consciente de la luz | 15% |
| Calidad reflexiva y argumentativa | 15% |
| Organización y claridad del PDF | 10% |
