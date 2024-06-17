/*
13-04-24
Compendio del desarrollo de funciones para HEAPx
*/

#include <stdio.h>
#include "functionsHeap.h"
//1
void createMaxi_MiniHeap(heap* h, int size)// es indiferente al que se crea
{
    h->n = size;
    h->heap = (element*) malloc(sizeof(element)*size);
    h->last = 0;
}

//2
void insertarMaxi_MiniHeapNodo(heap* h,int valorMeter)
{
    h->heap[h->last] = valorMeter;
    h->last ++;
    if(h->last > 1 && h->heap[h->last-1] < h->heap[parent(h->last -1)])
        upheap(h,h->last - 1);
}

//3
void upheap(heap* h, int i)
{
    int iParent = parent(i);
    while(i > 0 && h->heap[i] < h->heap[iParent])
    {
         // aqui cambio de '<' a '>' para el maxiheap, no se exactamente cual
        swap(h,i,iParent);
        i = iParent;
        iParent = parent(i);
    }
}

//4
void swap(heap* h, int a, int b)
{
    element aux = h->heap[a];
    h->heap[a] = h->heap[b];
    h->heap[b] = aux;
}

//5
int hijoIzq(int i)
{
    return i * 2 + 1;
}

//6
int hijoDer(int i)
{
    return i * 2 + 2;
}

//7
int parent(int i)
{
    return (i - 1) / 2 ;
}

//8
void downheap(heap* h, int i)
{
    int size = h->last;        // Inicializa el mayor como la raíz//SIZE/largest
    int left = hijoIzq(i);   // Índice del hijo izquierdo
    int right = hijoDer(i);  // Índice del hijo derecho
    int small = i;

    // Si el hijo izquierdo es mayor que la raíz
    if (left < size && h->heap[left] < h->heap[small])
        small = left;

    // Si el hijo derecho es mayor que el mayor hasta ahora
    if (right < size && h->heap[right] < h->heap[small])
        small = right;

    // Si el mayor no es la raíz
    if (small != i)
    {
        swap(h,i,small);
        // Realiza recursivamente el downheap en el subárbol afectado
        downheap(h,small);
    }
}

//9
void removeHeap(heap* h)
{
    free(h->heap); // de liberar meoria
}

//10
element deleteMaxiMiniHeap(heap* h)
{
    element aux = h->heap[0];
    swap(h,0,h->last-1);
    h->last--;

    if(h->last>2 &&(h->heap[0]>h->heap[hijoIzq(0)] || h->heap[0] > h->heap[hijoDer(0)]))
        downheap(h,0);
    return aux;
}



// para imprimir solo con imprimir el arreglo
