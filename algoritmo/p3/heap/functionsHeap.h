/*
13-Jun-24
*/
#ifndef STRUCTS
#define STRUCTS

// A. Variables globales
typedef int element;

typedef struct heap
{
    element* heap;// debe ser iun numerico siempre
    int n;
    int last;
}heap;
// B. Prototipos de funciones
    void createMaxi_MiniHeap(heap* h, int size); //A.1OK
    void insertarMaxi_MiniHeapNodo(heap* h,int valorMeter);//A.2OK
    void upheap(heap* h, int i);//A.3OK
    void swap(heap* h, int a, int b);//A.4OK
    int hijoIzq(int i);//A.5OK
    int hijoDer(int i);//A.6OK
    int parent(int i);//A.7OK
    void downheap(heap* h, int i);//A.8
    void removeHeap(heap* h);//A.9
    element deleteMaxiMiniHeap(heap* h);//A.10

#include "functionsHeap.c"
#endif
// Por Said Carbot Cruz Trejo ESCOM-IPN-MEX-JUNIO-24
