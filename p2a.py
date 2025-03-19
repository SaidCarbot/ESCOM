# se ve todo bein hasta Antes de GUI y ya con BFS, no verificado

import tkinter as tk
from PIL import Image, ImageTk  # Importar Pillow
import queue

# Crear la ventana principal de Tkinter
raiz = tk.Tk()
raiz.title("15 Puzzle")

# Obtener las dimensiones de la pantalla
ancho_pantalla = raiz.winfo_screenwidth()
alto_pantalla = raiz.winfo_screenheight()

# Ajustar el tamaño de la ventana a las dimensiones de la pantalla
raiz.geometry(f"{ancho_pantalla}x{alto_pantalla}")

# Crear un marco para controles y posicionarlo arriba
marco_controles = tk.Frame(raiz, bg="gray")
marco_controles.pack(side="top", fill="x")  # Lo pone arriba y lo expande horizontalmente

# Definir canvas que ocupará toda la pantalla menos el espacio de los botones
lienzo = tk.Canvas(raiz, width=ancho_pantalla, height=alto_pantalla - 100, bg="linen")
lienzo.pack()

# Funciones de botones
def bfsPrime():
    try:
        bfs(orden5)
    except:
        print("No se pudo ejecutar BFS")

def dfsPrime():
    try:
        print("DFS")
    except:
        print("No se pudo ejecutar DFS")

def salir():
    try:
        raiz.quit()
    except:
        print("No se pudo salir")

# Crear botones dentro del marco de controles
BotonBFS = tk.Button(marco_controles, text="BFS", command=bfsPrime, font=("Arial", 12), width=10, bg="lightblue")
BotonDSF = tk.Button(marco_controles, text="DFS", command=dfsPrime, font=("Arial", 12), width=10, bg="lightgreen")
BotonExit = tk.Button(marco_controles, text="Exit", command=salir, font=("Arial", 12), width=10, bg="lightgreen")

# Posicionar los botones dentro del marco_controles
BotonBFS.grid(row=0, column=0, padx=5, pady=10)
BotonDSF.grid(row=0, column=1, padx=5, pady=10)
BotonExit.grid(row=0, column=3, padx=5, pady=10)

# Crear barra deslizable
barra_velocidad = tk.Scale(marco_controles, from_=1, to=100, orient="horizontal", label="Velocidad", length=200)
barra_velocidad.grid(row=0, column=2, padx=10, pady=10)


def cargar_imagen(lienzo, img_path, orden=None, filas=4, columnas=4):
    img = Image.open(img_path)
    w, h = img.size
    w_corte, h_corte = w // columnas, h // filas

    # Crear lista indexada para guardar imágenes en su índice correcto
    imagenes = [None] * (filas * columnas)

    # Recortar y almacenar cada pieza en su índice correcto
    for i in range(filas):
        for j in range(columnas):
            idx = i * columnas + j
            left = j * w_corte
            upper = i * h_corte
            right = left + w_corte
            lower = upper + h_corte
            sub_img = img.crop((left, upper, right, lower))
            sub_img_tk = ImageTk.PhotoImage(sub_img)
            imagenes[idx] = sub_img_tk  # Guardamos en su posición real

    # Si orden no se define, usamos el orden natural
    if orden is None:
        orden = list(range(filas * columnas))  # [0,1,2,...15]

    # Colocar imágenes en el lienzo usando el orden definido
    #print("\nÍndices de las imágenes en el lienzo:")
    for pos_actual, idx in enumerate(orden):  
        fila = pos_actual // columnas
        columna = pos_actual % columnas
        #print(f"Posición en lienzo ({fila}, {columna}) ← Imagen con índice {idx}")
        lienzo.create_image(columna * w_corte, fila * h_corte, anchor="nw", image=imagenes[idx])

    return imagenes, orden  # Devolver imágenes y orden para modificaciones futuras

# Llamar a la función para cargar la imagen en el lienzo con el orden especificado
ordenBase = [0, 1, 2, 3,
             4, 5, 6, 7,
             8, 9, 10, 11,
             12, 13, 14]  # salen bien todos

orden5 = [0, 1, 2, 3,
          4, 5, 6, 7,
          8, 10, 11, 14,
          12, 9, 13]

orden10 = [0, 1, 2, 3,
         8, 4, 6, 7,
         5, 9, 10, 11,
         12, 13, 14]

orden20 = [1, 2, 6, 3,
         0, 10, 7, 11,
         8, 9, 4, 5,
         12, 13, 14]
# funciones chidas
from collections import deque

def generar_vecinos(estado):
    """Genera todos los estados vecinos moviendo el espacio vacío (0)"""
    vecinos = []#lista
    idx_0 = estado.index(0)  # Encuentra la posición del 0
    filas, columnas = 4, 4  # Tamaño del tablero

    # Posiciones de movimiento (arriba, abajo, izquierda, derecha)
    movimientos = {
        "arriba": -columnas,
        "izquierda": -1
    }

    for mov, offset in movimientos.items():
        nuevo_idx = idx_0 + offset

        # Verifica si el movimiento es válido dentro de los límites
        if 0 <= nuevo_idx < filas * columnas:
            # Evitar movimientos ilegales entre filas
            if mov == "izquierda" and idx_0 % columnas == 0:
                continue

            # Generar el nuevo estado intercambiando 0 con su vecino
            nuevo_estado = list(estado)  # Copia la lista
            nuevo_estado[idx_0], nuevo_estado[nuevo_idx] = nuevo_estado[nuevo_idx], nuevo_estado[idx_0]
            
            # Solo agregamos el nuevo estado si el 0 regresa a la posición 15
            if nuevo_estado.index(0) == 15:
                vecinos.append(tuple(nuevo_estado))  # Convertimos de nuevo a tupla
    
    return vecinos

def bfs(estado_inicial):
    """Ejecuta BFS para resolver el rompecabezas deslizante"""
    estado_inicial = tuple(estado_inicial)  # Convertimos la lista en tupla
    objetivo = tuple(range(16))  # (0,1,2,3,...,15)
    
    queue = deque([estado_inicial])  # Cola para BFS
    visited = set()  # Estados visitados
    parent = {}  # Para reconstruir el camino

    visited.add(estado_inicial)
    
    while queue:
        estado_actual = queue.popleft()
        print(f"Visitando: {estado_actual}")  # Para depuración

        if estado_actual == objetivo:
            print("¡Solución encontrada!")
            return reconstruir_camino(parent, estado_inicial, estado_actual)

        # Expandir vecinos
        for vecino in generar_vecinos(estado_actual):
            if vecino not in visited:
                queue.append(vecino)
                visited.add(vecino)
                parent[vecino] = estado_actual  # Registrar el padre
    
    print("No se encontró solución.")
    return None

def reconstruir_camino(parent, inicio, fin):
    """Reconstruye el camino desde la meta hasta el inicio"""
    camino = []
    actual = fin
    while actual != inicio:
        camino.append(actual)
        actual = parent[actual]
    camino.append(inicio)
    return camino[::-1]  # Devolver en orden correcto


imagenes = cargar_imagen(lienzo, "img2.png", orden5)

# Mantener la ventana en ejecución
raiz.mainloop()
