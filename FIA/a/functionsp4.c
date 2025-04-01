/*
31 de marzo de 2025
Del archivo con las funciones para poda alpha-beta en un conecta 4
*/
#include <stdio.h> 
#include <stdlib.h> 
#include <stdbool.h>
#include <limits.h> 
#include "functionsp4.h" 
/**
 * Estuve investigando y encontré que por buenas prácticas se hacen comentarios con @"identificador"
 * Asi generadores de documentación de código lo hacen automaticamente, sin usar chat. 
 * @reference R. C. Martin, Clean Code: A Handbook of Agile Software Craftsmanship. Upper Saddle River, NJ: Prentice Hall, 2009, pp.94
 */

 // ---A) Funciones de Validación y Manipulación del Tablero de [Lista]de[Listas] ---
/** 
 * @brief Verifica si una columna es válida y no está llena.
 * @return true si es valido, false sino es valido
 */
bool isValidMove(int board[ROWS][COLS], int col) {
    // Verifica rango de columna(Izq-Der)
    if (col < 0 || col >= COLS) {
        // printf("Columna %d fuera de rango.\n", col); //  Para debugear
        return false;
    }
    // Verifica si la columna está llena (ve la casilla superior)(Abajo-Arriba)
    if (board[0][col] != EMPTY) {
        // printf("Columna %d llena.\n", col); //  Para debugear
        return false;
    }
    return true; // Movimiento válido
}

/**
 * @brief Coloca la ficha del jugador (humano o IA) en la columna especificada, recuerda que lo simula en el "GameArbol"
 * @return La fila donde se colocó la ficha, o -1 si la columna es inválida/llena.
 */
int hacerMovimiento(int board[ROWS][COLS], int col, int jugador) {
    // Re-validación, anque podría quitarse pues usualmente se llama después de isValidMove que ya revisa si es valido
    if (col < 0 || col >= COLS || board[0][col] != EMPTY) {
        return -1;
    }
    // Encuentra la fila vacía más baja
    for (int row = ROWS - 1; row >= 0; row--) {
        if (board[row][col] == EMPTY) {
            board[row][col] = jugador;
            return row; // Retorna la fila donde se colocó
        }
    }
    return -1;
}

/**
 * @brief Quita una ficha de la posición especificada (para deshacer movimientos)
 * Como revisa todos los movimientos por columnas recursivamente la funcion poda
 * Pero sí modifica el tablero original asi que esta sirve para cada posible columan/tiro
 */
void deshacerMovimiento(int board[ROWS][COLS], int row, int col) {
    // Verifica límites (opcional pero seguro)
    if (row >= 0 && row < ROWS && col >= 0 && col < COLS) {
         board[row][col] = EMPTY;
    }
}

// ---B) Funciones de Verificación del Estado del Juego(ganar,perder,empate) ---

/**
 * @brief Verifica si un jugador ha ganado (4 opciones, o sea ve si ya hay 3 en linea).
 * @return  true si hay ganador, false sino hay ganador
 */
bool checkWinner(int board[ROWS][COLS], int jugador) {
    // Horizontal (-)
    for (int row = 0; row < ROWS; row++) {
        for (int col = 0; col < COLS - 3; col++) {
            if (board[row][col] == jugador && board[row][col+1] == jugador &&
                board[row][col+2] == jugador && board[row][col+3] == jugador) {
                return true;
            }
        }
    }
    // Vertical (|)
    for (int row = 0; row < ROWS - 3; row++) {
        for (int col = 0; col < COLS; col++) {
            if (board[row][col] == jugador && board[row+1][col] == jugador &&
                board[row+2][col] == jugador && board[row+3][col] == jugador) {
                return true;
            }
        }
    }
    // (\)
    for (int row = 0; row < ROWS - 3; row++) {
        for (int col = 0; col < COLS - 3; col++) {
            if (board[row][col] == jugador && board[row+1][col+1] == jugador &&
                board[row+2][col+2] == jugador && board[row+3][col+3] == jugador) {
                return true;
            }
        }
    }
    // (/)
    for (int row = 3; row < ROWS; row++) {
        for (int col = 0; col < COLS - 3; col++) {
            if (board[row][col] == jugador && board[row-1][col+1] == jugador &&
                board[row-2][col+2] == jugador && board[row-3][col+3] == jugador) {
                return true;
            }
        }
    }
    return false; // No hay ganador
}

/**
 * @brief Ver si alguien ganó o empataron
 * @return true si ya gano alguien o si board lleno(empate) o false si nadie ha ganado
 */
bool isGameOver(int board[ROWS][COLS]) {
    // Verifica si alguien ganó
    if (checkWinner(board, PLAYER) || checkWinner(board, AI)) {
        return true;
    }
    // Empate por que lleno
    for (int col = 0; col < COLS; col++) {
        if (board[0][col] == EMPTY) {
            return false; //Hay una casilla vacía, el juego no ha terminado
        }
    }
    // Si no hay ganador y no hay casillas vacías en la fila superior, es empate
    return true;
}

// ---C) Funciones de Evaluación (Heurística) ---

/**
 * @brief Evalúa cuántas líneas de 'longitud' potencialmente completables tiene un jugador.
 * @return  int de count de cuantas fichas hay en cada linea
 */
int evaluarLineas(int board[ROWS][COLS], int jugador, int longitud) {
    int count = 0;
    int oponente = (jugador == AI) ? PLAYER : AI;

    // (-) y la repito para todas las direcciones
    for (int row = 0; row < ROWS; row++) {
        for (int col = 0; col <= COLS - longitud; col++) {
            int piezasJugador = 0;
            bool bloqueado = false;
            for (int i = 0; i < longitud; i++) {
                if (board[row][col + i] == jugador) {
                    piezasJugador++;
                } else if (board[row][col + i] == oponente) {
                    bloqueado = true;
                    break;
                }
            }
            // Cuenta si la línea NO está bloqueada y tiene al menos una pieza del jugador
            // no tira en espacios que no esten ya conectado con algo n n+/- 1, o sea en libre
            if (!bloqueado && piezasJugador > 0) {
                count++;
            }
        }
    }

    // (|)
     for (int col = 0; col < COLS; col++) {
        for (int row = 0; row <= ROWS - longitud; row++) {
             int piezasJugador = 0;
             bool bloqueado = false;
             for (int i = 0; i < longitud; i++) {
                 if (board[row + i][col] == jugador) {
                     piezasJugador++;
                 } else if (board[row + i][col] == oponente) {
                     bloqueado = true;
                     break;
                 }
             }
             if (!bloqueado && piezasJugador > 0) {
                 count++;
             }
         }
     }

    // (\)
     for (int row = 0; row <= ROWS - longitud; row++) {
         for (int col = 0; col <= COLS - longitud; col++) {
             int piezasJugador = 0;
             bool bloqueado = false;
             for (int i = 0; i < longitud; i++) {
                 if (board[row + i][col + i] == jugador) {
                     piezasJugador++;
                 } else if (board[row + i][col + i] == oponente) {
                     bloqueado = true;
                     break;
                 }
             }
             if (!bloqueado && piezasJugador > 0) {
                 count++;
             }
         }
     }

    // (/)
     for (int row = longitud - 1; row < ROWS; row++) {
         for (int col = 0; col <= COLS - longitud; col++) {
             int piezasJugador = 0;
             bool bloqueado = false;
             for (int i = 0; i < longitud; i++) {
                 if (board[row - i][col + i] == jugador) {
                     piezasJugador++;
                 } else if (board[row - i][col + i] == oponente) {
                     bloqueado = true;
                     break;
                 }
             }
             if (!bloqueado && piezasJugador > 0) {
                 count++;
             }
         }
     }

    return count;
}

/**
 * @brief Función heurística que asigna una puntuación al tablero.
 * La puntuación es SIEMPRE relativa al jugador 'AI'.
 * Positivo es bueno para AI, Negativo es bueno para PLAYER.
 * @return int puntaje de para quien es bueno (IA o PLAYER)
 */
int evaluarTablero(int board[ROWS][COLS]) {
    int puntaje = 0;

    // Evaluar victoria / derrota inmediata 
    if (checkWinner(board, AI)) return 10000; // Puntuación muy alta para victoria de AI
    if (checkWinner(board, PLAYER)) return -10000; // Puntuación muy baja para victoria de Player

    // Priorizar el centro (columna 3 en un tablero 7x6)
    int colCentral = COLS / 2;
    for (int row = 0; row < ROWS; row++) {
        if (board[row][colCentral] == AI) puntaje += 3;
        else if (board[row][colCentral] == PLAYER) puntaje -= 3;
    }

    // Evalúar líneas de 2 y 3 fichas (potencial)
    puntaje += evaluarLineas(board, AI, 2) * 2;   // 2 en línea AI = +2
    puntaje += evaluarLineas(board, AI, 3) * 10;  // 3 en línea AI = +10

    puntaje -= evaluarLineas(board, PLAYER, 2) * 2; // 2 en línea Player = -2
    puntaje -= evaluarLineas(board, PLAYER, 3) * 10; // 3 en línea Player = -10

    return puntaje;
}

// ---D)  Algoritmo Alpha-Beta ---

/**
 * @brief Implementación del algoritmo Alpha-Beta.
 * @return La evaluación del tablero desde la perspectiva del jugador 'AI'.
 */

int alphaBeta(int board[ROWS][COLS], int depth, int alpha, int beta, bool esMaximizando) {
    // Condición de parada: profundidad alcanzada o juego terminado
    if (depth == 0 || isGameOver(board)) {
        int baseEval = evaluarTablero(board);
        if (baseEval > 5000) baseEval += depth; // Si AI va ganando, prefiere ganar antes
        else if (baseEval < -5000) baseEval -= depth; // Si AI va perdiendo, prefiere perder después
        return baseEval;
    }

    if (esMaximizando) { // Turno del jugador AI (maximizar puntuación relativa a AI)
        int maxEval = INT_MIN;
        for (int col = 0; col < COLS; col++) {
            if (isValidMove(board, col)) {
                int row = hacerMovimiento(board, col, AI);
                /**
                 * Es recursivo porque asi va intercamaoindo entre los MAX-MIN-MAX para IA(raiz) y PLAYER  
                */
                int eval = alphaBeta(board, depth - 1, alpha, beta, false); // El siguiente es minimizador
                deshacerMovimiento(board, row, col);
                maxEval = (eval > maxEval) ? eval : maxEval; // maxEval = max(maxEval, eval);
                alpha = (eval > alpha) ? eval : alpha;     // alpha = max(alpha, eval);
                if (beta <= alpha) {
                    break; // Poda Beta
                }
            }
        }
        // Si no hay movimientos válidos desde este estado
        if (maxEval == INT_MIN) {
             // Podría significar que todos los caminos llevan a la derrota inmediata.
             return evaluarTablero(board); // O return -20000;
        }
        return maxEval;
    } else { // Turno del jugador PLAYER (minimizar puntuación relativa a AI)
        int minEval = INT_MAX;
        for (int col = 0; col < COLS; col++) {
            if (isValidMove(board, col)) {
                int row = hacerMovimiento(board, col, PLAYER);
                int eval = alphaBeta(board, depth - 1, alpha, beta, true); // El siguiente es maximizador
                deshacerMovimiento(board, row, col);
                minEval = (eval < minEval) ? eval : minEval; // minEval = min(minEval, eval);
                beta = (eval < beta) ? eval : beta;       // beta = min(beta, eval);
                if (beta <= alpha) {
                    break; // Poda Alpha
                }
            }
        }
        // Si no hay movimientos válidos
         if (minEval == INT_MAX) {
             return evaluarTablero(board); // O return 20000;
         }
        return minEval;
    }
}


// ---E) Funciones para conectar con la Interfaz en Python ---

/**
 * @brief Calcula la mejor columna para el jugador actual usando Alpha-Beta. *
 * @param flat_board Puntero al tablero representado como un array 1D (fila por fila).
 * @param rows Número de filas del tablero (debe coincidir con ROWS).
 * @param cols Número de columnas del tablero (debe coincidir con COLS).
 * @param jugadorActual El marcador del jugador cuyo movimiento se busca (AI o PLAYER).
 * @param profundidad La profundidad de búsqueda para este turno.
 * @return Basicamente, dondé tirar en el board: int El índice de la mejor columna encontrada (0 a COLS-1), o -1 si no hay movimientos válidos o hay error.
 */
int obtenerMejorMovimientoParaJugador(int *flat_board, int rows, int cols, int jugadorActual, int profundidad) {
    // Validación de dimensiones
    if (rows != ROWS || cols != COLS) {
        fprintf(stderr, "Error C: Dimensiones de tablero incorrectas (recibido %dx%d, esperado %dx%d).\n", rows, cols, ROWS, COLS);
        return -1;
    }
     if (profundidad <= 0) {
        fprintf(stderr, "Error C: Profundidad debe ser positiva (recibido %d).\n", profundidad);
        return -1;
    }
    // Crear una copia local del tablero en 2D
    int board[ROWS][COLS];
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            board[r][c] = flat_board[r * cols + c];
        }
    }

    int mejorCol = -1;
    int mejorEval;
    int oponente = (jugadorActual == AI) ? PLAYER : AI;

    // Inicializar según el jugador (maximizar o minimizar la puntuación relativa a AI)
    if (jugadorActual == AI) {
        mejorEval = INT_MIN;
    } else { // jugadorActual == PLAYER
        mejorEval = INT_MAX;
    }

    bool hayMovimientosValidos = false;

    // Iterar sobre todas las columnas posibles
    for (int col = 0; col < COLS; col++) {
        if (isValidMove(board, col)) {
            hayMovimientosValidos = true;
            int row = hacerMovimiento(board, col, jugadorActual);

            // Determinar si el SIGUIENTE turno (del oponente) es el del maximizador (AI)
            bool proximoTurnoEsMaximizando = (oponente == AI);
            int eval = alphaBeta(board, profundidad - 1, INT_MIN, INT_MAX, proximoTurnoEsMaximizando);

            deshacerMovimiento(board, row, col);

            // Actualizar mejorCol basado en si el jugadorActual maximiza o minimiza 'eval'
            if (jugadorActual == AI) {
                if (eval > mejorEval) {
                    mejorEval = eval;
                    mejorCol = col;
                }
            } else { // jugadorActual == PLAYER
                if (eval < mejorEval) {
                    mejorEval = eval;
                    mejorCol = col;
                }
            }
        }
    }

    // Si no hubo movimientos válidos (tablero lleno)
    if (!hayMovimientosValidos) {
        fprintf(stderr, "Advertencia C: No se encontraron movimientos válidos para el jugador %d.\n", jugadorActual);
        return -1;
    }

    // Si hubo movimientos pero ninguno mejoró la eval inicial
    // Devolver la primera columna válida encontrada para evitar devolver -1 erróneamente.
    if (mejorCol == -1 && hayMovimientosValidos) {
        for (int col = 0; col < COLS; col++) {
            if (isValidMove(board, col)) {
                mejorCol = col;
                break;
            }
        }
    }

    return mejorCol;
}

 // ---F) Implementación de Funciones para leer/escribir Archivo ---

 /**
  * @brief Lee el estado del tablero desde un archivo de texto.
  * @param board El array 2D donde se cargará el tablero.
  * @param nombreArchivo El nombre del archivo a leer ("tablero.txt").
  * @return true si la lectura fue exitosa, false en caso contrario.
  */
 bool leerTableroDesdeArchivo(int board[ROWS][COLS], const char* nombreArchivo) {
    FILE *archivo = fopen(nombreArchivo, "r");
    if (archivo == NULL) {
        perror("Error C (leerTablero): fopen");
        return false;
    }

    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            // Lee un entero. fscanf devuelve el número de ítems leídos.
            if (fscanf(archivo, "%d", &board[r][c]) != 1) {
                fprintf(stderr, "Error C (leerTablero): Error al leer el valor en [%d][%d] o archivo incompleto.\n", r, c);
                fclose(archivo);
                return false;
            }
        }
    }

    fclose(archivo);
    return true;
}

/**
 * @brief Guarda el estado actual del tablero en un archivo de texto.
 * @param board El array 2D con el estado actual del tablero.
 * @param nombreArchivo El nombre del archivo donde guardar ("tablero.txt").
 * @return true si la escritura fue exitosa, false en caso contrario.
 */
bool guardarTableroEnArchivo(int board[ROWS][COLS], const char* nombreArchivo) {
    FILE *archivo = fopen(nombreArchivo, "w"); // "w" para escribir (sobrescribe)
    if (archivo == NULL) {
        perror("Error C (guardarTablero): fopen");
        return false;
    }

    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            // Escribe el número y un espacio (excepto para la última columna)
            fprintf(archivo, "%d%c", board[r][c], (c == COLS - 1) ? '\n' : ' ');
        }
        // fprintf(archivo, "\n"); // Nueva línea al final de cada fila
    }

    fclose(archivo);
    return true;
}
// By Said C. Cruz Trejo Aaron U. Téllez--MEX-IPN-ESCOM-IA 2025/2 spring 2025