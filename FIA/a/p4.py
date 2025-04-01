#A) GUI

import tkinter as tk
from tkinter import messagebox
import subprocess

# Configuración del tablero
FILAS = 6 #r
COLUMNAS = 7 #c
EMPTY = 0
PLAYER = 1 #Jugador 1 es PLAYER/Verde/Humano
AI = 2     #Jugador 2 es IA/Beige/C
jugador = PLAYER  # Jugador PLAYER comienza

#[Lista]de[Listas]
tablero = [[EMPTY for _ in range(COLUMNAS)] for _ in range(FILAS)] 


#  A) Funciones de la GUI 
def dibujar_tablero():
    """
    * @brief Dibuja el estado actual del tablero en la interfaz gráfica.
    * Crea círculos en cada celda con el color correspondiente al jugador que ocupa esa posición.
    """
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            color = "white"  # Color por defecto para el fondo
            if tablero[fila][columna] == 1:
                color = "DarkOliveGreen3"  # Jugador 1 verde
            elif tablero[fila][columna] == 2:
                color = "LightGoldenrod2"  # Jugador 2 beige
            # tamaño circulos
            lienzo.create_oval(columna * 100 + 10, fila * 100 + 10, (columna + 1) * 100 - 10, (fila + 1) * 100 - 10, fill=color)

def soltar_pieza(columna_seleccionada): # larga
    """
    *@brief Maneja la colocación de una pieza en el tablero por parte del jugador PLAYER.
    *@param columna_seleccionada: int - Índice de la columna donde se intenta colocar la pieza.
    """
    global jugador
    # Solo permite mover si es el turno del jugador PLAYER
    if jugador != PLAYER:
        print("No es tu turno.")
        return
    
    # Encontrar la primera fila vacía en la columna seleccionada
    fila_real = -1
    for fila in range(FILAS - 1, -1, -1):
        if tablero[fila][columna_seleccionada] == EMPTY:
            tablero[fila][columna_seleccionada] = PLAYER
            fila_real = fila
            break
    
    # Si no hay filas vacías en la columna
    if fila_real == -1:
        messagebox.showwarning("Movimiento inválido", "La columna seleccionada está llena.")
        return # Columna llena

    dibujar_tablero() # Dibuja el movimiento PLAYER

    # Verificar condiciones de fin de juego
    if verificar_ganador(PLAYER):
        dibujar_tablero()  # Asegúrate de que la última pieza ganadora se dibuje
        messagebox.showinfo("¡Ganador!", f"¡Jugador {PLAYER} (PLAYER) gana!")
        reiniciar_juego()
        return
    elif verificar_empate():
        dibujar_tablero() # Asegúrate de que el tablero lleno se dibuje
        messagebox.showinfo("¡Fin del Juego!", "¡Es un empate!")
        reiniciar_juego()
        return
    else:
         # Si PLAYER no ganó ni empata, cambia al turno a IA (para poda(alterna MAX-MIN))
         jugador = AI
         print("Turno del Jugador", jugador, "(IA)")
         ventana_principal.after(50, ejecutar_c) # 50ms de retraso

#  B) Funciones de la Mecánica del juego
def verificar_ganador(jugador):
    """
    *@brief Verifica si el jugador especificado ha formado una línea de 4 piezas.
    *@param jugador_actual: int - Identificador del jugador a verificar (PLAYER o AI).
    *@return: bool - True si el jugador ha ganado, False en caso contrario.
    """
    # Verificar filas, columnas y diagonales
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            #Izq->Dere y ademas ve que no se salga del tablero
            if columna + 3 < COLUMNAS and all(tablero[fila][columna + indice] == jugador for indice in range(4)):
                return True
            #Dere->Izq
            if fila + 3 < FILAS and all(tablero[fila + indice][columna] == jugador for indice in range(4)):
                return True
            # Diaginal  \
            if fila + 3 < FILAS and columna + 3 < COLUMNAS and all(tablero[fila + indice][columna + indice] == jugador for indice in range(4)):
                return True
            # Diagonal /
            if fila - 3 >= 0 and columna + 3 < COLUMNAS and all(tablero[fila - indice][columna + indice] == jugador for indice in range(4)):
                return True
    return False

# Función para reiniciar el juego
def reiniciar_juego():
    """
    *@brief Reinicia el estado del juego al inicial.
    *Limpia el tablero y restablece el turno al PLAYER.
    """
    global jugador, tablero
    jugador = 1  # Jugador 1 PLAYER comienza
    tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
    dibujar_tablero()

# C) Conexión con el C
def leer_tablero():
    """
    *@brief Lee el estado del tablero desde un archivo .txt
    *@return: list[list[int]] - Matriz que representa el estado del tablero.
    """
    with open('tablero.txt', 'r') as file:
        tablero = [list(map(int, line.split())) for line in file]
    return tablero

def guardar_tablero():
    """
    *@brief Guarda el estado actual del tablero en un archivo de texto.
    *El formato es una matriz de números separados por espacios.
    """
    with open('tablero.txt', 'w') as file:
        for fila in tablero:
            file.write(" ".join(map(str, fila)) + "\n")

def ejecutar_c():
    """
    *@brief Ejecuta el programa en C que contiene la lógica de la IA.
    *Guarda el tablero actual, ejecuta la IA y actualiza el tablero con su movimiento.
    """
    global jugador #quién es el siguiente jugador?
    if jugador != AI: # Solo ejecuta C cuando le toca a la la IA
         print("Error lógico: ejecutar_c llamado cuando no es turno de la IA")
         return

    print("Guardando tablero para C...")
    guardar_tablero()  # Guardar el estado antes de llamar a C(por sin hay "execpts")

    print("Ejecutando C ('./conecta4')...")
    try:
        subprocess.run(["./conecta4"], check=True)  # Ejecutar el programa en C
        print("Ejecución de C completada.")
    except FileNotFoundError:
         messagebox.showerror("Error", "No se encontró el ejecutable './conecta4'. Asegúrate de que está compilado y en el mismo directorio.")
         reiniciar_juego() 
         return
    except subprocess.CalledProcessError as e:
         messagebox.showerror("Error", f"El programa C './conecta4' falló.\nError: {e}")
         reiniciar_juego() 
         return
    except Exception as e:
         messagebox.showerror("Error", f"Ocurrió un error inesperado al ejecutar C.\nError: {e}")
         reiniciar_juego()
         return

    print("Actualizando tablero desde archivo...")
    actualizar_tablero_desde_archivo()  # Leer la actualización de C

    if verificar_ganador(AI):
        messagebox.showinfo("¡Fin del Juego!", f"¡Jugador {AI} (IA) gana!")
        reiniciar_juego()
    elif verificar_empate():
         messagebox.showinfo("¡Fin del Juego!", "¡Es un empate!")
         reiniciar_juego()
    else:
        # Si el juego no ha terminado, cambia el turno de vuelta al PLAYER
        jugador = PLAYER
        print("Turno del Jugador", jugador)

def verificar_empate():
    """
    *@brief Verifica si el juego ha terminado en empate (tablero lleno).
    *@return: bool - True si todas las columnas están llenas, False en caso contrario.
    """
    # El tablero está lleno si la fila superior no tiene casillas vacías
    for col in range(COLUMNAS):
        if tablero[0][col] == EMPTY:
            return False # Encontró un espacio vacío, no es empate
    return True # No hay espacios vacíos en la fila superior

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Conecta Cuatro con búsqueda α-β")

titulo = tk.Label(ventana_principal, text="Conecta Cuatro con búsqueda α-β", font=("Arial", 25, "bold"))
titulo.pack(pady=10)

# Crear el lienzo para dibujar el tablero
lienzo = tk.Canvas(ventana_principal, width=COLUMNAS * 100, height=FILAS * 100)
lienzo.pack()

# Botones para elegir la columna, solo clicleable en sonas grises
for columna in range(COLUMNAS):
    lienzo.create_rectangle(columna * 100 + 10, 0, (columna + 1) * 100 - 10, 40, fill="gray", outline="black")
    # No se me ocurre como dejar los espacios en blanco tambien como boton
    lienzo.tag_bind(lienzo.create_rectangle(columna * 100 + 10, 0, (columna + 1) * 100 - 10, 800, fill="gray", outline="black"), '<Button-1>', lambda e, col=columna: soltar_pieza(col))

# Botón para reiniciar el juego
boton_reiniciar = tk.Button(ventana_principal, text="Reiniciar Juego", command=reiniciar_juego)
boton_reiniciar.pack()

# Función para mostrar el menú desplegable para seleccionar el número de jugador (futuras implementaciones)
def mostrar_opciones_jugador(numero_jugador):
    ventana_opciones = tk.Toplevel(ventana_principal)
    ventana_opciones.title(f"Seleccionar Jugador {numero_jugador}")

    # Crear una lista desplegable
    variable_jugador = tk.IntVar()
    variable_jugador.set(1)  # Valor predeterminado
    for indice in range(1, 11):
        tk.Radiobutton(ventana_opciones, text=str(indice), variable=variable_jugador, value=indice).pack(anchor='w')

    def aplicar_opcion():
        if numero_jugador == 1:
            eleccion_jugador_uno.set(variable_jugador.get())
        else:
            eleccion_jugador_dos.set(variable_jugador.get())
        ventana_opciones.destroy()

    tk.Button(ventana_opciones, text="Aceptar", command=aplicar_opcion).pack()


def actualizar_tablero_desde_archivo():
    """
    *@brief usa el C con el mejor movimiento(int-columna en donde tirar) para redibujar interfaz
    """
    global tablero
    try:
        with open('tablero.txt', 'r') as file:
            tablero = [list(map(int, line.split())) for line in file]
        dibujar_tablero()  # Redibujar la interfaz con el nuevo tablero
    except FileNotFoundError:
        print("Error: No se encontró el archivo tablero.txt")


# Variables para los jugadores
eleccion_jugador_uno = tk.IntVar(value=1)
eleccion_jugador_dos = tk.IntVar(value=1)

# Botón para Player One
boton_jugador_uno = tk.Button(ventana_principal, text="Seleccionar Jugador 1", command=lambda: mostrar_opciones_jugador(1))
boton_jugador_uno.pack(side=tk.LEFT, padx=5)

# Botón para Player Two
boton_jugador_dos = tk.Button(ventana_principal, text="Seleccionar Jugador 2", command=lambda: mostrar_opciones_jugador(2))
boton_jugador_dos.pack(side=tk.LEFT, padx=5)

# Dibujar el tablero inicial
dibujar_tablero()

# Iniciar la interfaz de Tkinter
ventana_principal.mainloop()

#By Said C. Cruz Trejo Aaron U. Téllez--MEX-IPN-ESCOM-IA 2025/2 spring 2025