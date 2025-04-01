/*
INSTRUCCIONES: 
0) son 6 archivos: 
    * mainp4.c (Ejecutar funciones)
    * functionsp4.c (declaracipon explisita funciones)
    * functionsp4.h (prototipado funciones)
    * p4.py (GUI del coecta4)
    * ejecutable que se genera despues de compilar
    * el .txt que sirve de peente entre C y python
1) COMPILAR el mainp4.c con gcc mainp4.c functionsp4.c -o conecta4 -lm
2) Ejecutar p4.py con "python p4.py"
3) Se habre una ventana con el juego 
4) Movimiento es del HUMANO
5) Despues la IA buscara el mejor movimiento con el mainp4.c
    5.1) Regresara la fila donde debe tirar a traves de un .txt
    5.2) El p4.py leera el .txt
6) Se actualiza la GUI con base en el C.
7) Repetir 4 a 6



gcc mainp4.c functionsp4.c -o conecta4 -lm
*/

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>
typedef int element;
#include "functionsp4.h"

/*
 * Programa principal para ser llamado desde Python via subprocess.
 * Lee el tablero de 'tablero.txt', calcula y realiza el movimiento de la IA,
 * y guarda el tablero actualizado de nuevo en 'tablero.txt'.
 * Fecha: 31 de marzo de 2025  
 */

 int main() {
     int tablero[ROWS][COLS];
     const char* nombreArchivo = "tablero.txt"; 

     // 1. Leer y pasar el tablero desde el .txt con función
     if (!leerTableroDesdeArchivo(tablero, nombreArchivo)) {
         fprintf(stderr, "Error C (main): No se pudo leer el tablero desde %s\n", nombreArchivo);
         return 1;
     }

     // 2--- Lógica para hacer el movimiento de la IA ---

     // 2.1 Pasar el tablero [lista]de[listas] a un array simple
     int tableroAplanado[ROWS * COLS];
     for (int r = 0; r < ROWS; ++r) {
         for (int c = 0; c < COLS; ++c) {
             tableroAplanado[r * COLS + c] = tablero[r][c];
         }
     }

     // 2.2. Obtener la mejor columna/jugada para la IA
     printf("Info C (main): Calculando movimiento para Jugador %d con profundidad %d...\n", JUGADOR_ESTE_PROGRAMA, PROFUNDIDAD_IA);
     int mejorColumna = obtenerMejorMovimientoParaJugador(
         tableroAplanado, // Pasa el tablero aplanado
         ROWS,
         COLS,
         JUGADOR_ESTE_PROGRAMA,
         PROFUNDIDAD_IA
     );

     // 4. Realizar el movimiento si es válido
     // Verificar que sea valido el movimiento
     if (mejorColumna >= 0 && mejorColumna < COLS) {
         printf("Info C (main): IA (Jugador %d) elige la columna %d.\n", JUGADOR_ESTE_PROGRAMA, mejorColumna);
         // Modificar el tablero de [lista]de[lista] :/ tablero
         int filaMovimiento = hacerMovimiento(tablero, mejorColumna, JUGADOR_ESTE_PROGRAMA);
         // Si no es valido el movimiento
         if (filaMovimiento == -1) {
              fprintf(stderr, "Error C (main): La columna %d elegida por la IA resultó inválida al hacer el movimiento.\n", mejorColumna);
         }
     } else {
        // No  hace ningún movimiento, pero se guarda el tablero tal cual se leyó.
         fprintf(stderr, "Advertencia C (main): La IA no pudo encontrar un movimiento válido (Columna %d). ¿Tablero lleno o error?\n", mejorColumna);
     }

     // 5. Guardar el tablero (si se modificó) de vuelta al archivo .txt
     if (!guardarTableroEnArchivo(tablero, nombreArchivo)) {
         fprintf(stderr, "Error C (main): No se pudo guardar el tablero en %s\n", nombreArchivo);
         return 1; 
     }

     printf("Info C (main): Tablero actualizado guardado en %s.\n", nombreArchivo);
     return 0;
 }

// By Said C. Cruz Trejo Aaron U. Téllez--MEX-IPN-ESCOM-IA 2025/2 spring 2025