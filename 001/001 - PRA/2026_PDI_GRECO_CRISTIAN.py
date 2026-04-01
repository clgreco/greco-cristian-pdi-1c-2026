import py5

# varibales iniciales
color_actual = py5.color(0)
grosor = 3
modo = "lapicera"

def setup():
    py5.size(900, 600)
    py5.background(255)

def draw():
    

    global modo
    
    if py5.is_mouse_pressed:
        py5.stroke_weight(grosor)
        
        if modo == "lapicera":
            py5.stroke(color_actual)
            py5.line(py5.pmouse_x, py5.pmouse_y, py5.mouse_x, py5.mouse_y)
        
        elif modo == "borrador":
            py5.stroke(255)
            py5.stroke_weight(grosor*3)
            py5.line(py5.pmouse_x, py5.pmouse_y, py5.mouse_x, py5.mouse_y)


# Defino las teclas para cambiar color, el modo, y el grosor y borrar todo
def key_pressed():
    global color_actual, grosor, modo
    # r = rojo
    if py5.key == 'r':
        color_actual = py5.color(255, 0, 0)
    # v = verde
    elif py5.key == 'v':
        color_actual = py5.color(0, 255, 0)
    # a = azul
    elif py5.key == 'a':
        color_actual = py5.color(0, 0, 255)
    # n = negro
    elif py5.key == 'n':
        color_actual = py5.color(0)
    # 1 = lapicera
    elif py5.key == '1':
        modo = "lapicera"
    # 2 = borrador
    elif py5.key == '2':
        modo = "borrador"
 
    # con el + hago mas grande el grosor
    elif py5.key == '+':
        grosor += 1
    # Con el - hago mas chico el grosor (no peude ser menor a 1)
    elif py5.key == '-':    
        grosor = max(1, grosor - 1)
    # con la C borro el dibujo (la pantalla en blanco)
    elif py5.key == 'c':
        py5.background(255)
    # con la S guardo la imaen
    elif py5.key == 's':
        py5.save("C:/Users/Cristian/Desktop/py5/mi_dibujo.png")
        print("Imagen guardada")

py5.run_sketch()