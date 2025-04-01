/*
27 de marzo de 2025
*/
#ifndef STRUCTS
#define STRUCTS
/// Definir el tamaño del tablero desde el principio
#define ROWS 6
#define COLS 7
#define EMPTY 0
// Identificadores 
#define PLAYER 1 
#define AI 2

#define JUGADOR_ESTE_PROGRAMA AI //Humano
#define PROFUNDIDAD_IA 6 // Profundidad de búsqueda para Alpha-Beta


//////////////////////////////////////////
// movimientos
bool isValidMove(int board[ROWS][COLS], int col);
int hacerMovimiento(int board[ROWS][COLS], int col, int jugador);
void deshacerMovimiento(int board[ROWS][COLS], int row, int col);

// mecanica
bool checkWinner(int board[ROWS][COLS], int jugador);
bool isGameOver(int board[ROWS][COLS]);

// Heristica
int evaluarLineas(int board[ROWS][COLS], int jugador, int longitud);
int evaluarTablero(int board[ROWS][COLS]);
int alphaBeta(int board[ROWS][COLS], int depth, int alpha, int beta, bool esMaximizando);

// Conexión con Python
int obtenerMejorMovimientoParaJugador(int *flat_board, int rows, int cols, int jugadorActual, int profundidad);
bool guardarTableroEnArchivo(int board[ROWS][COLS], const char* nombreArchivo);
bool leerTableroDesdeArchivo(int board[ROWS][COLS], const char* nombreArchivo);

#include "functionsp4.h"
#endif

// By Said C. Cruz Trejo Aaron U. Téllez--MEX-IPN-ESCOM-IA 2025/2 spring 2025