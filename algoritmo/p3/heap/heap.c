/*11-jun-24

Del primer acercamiento en codigo de los heap, no hace diferencia la profesora
entre los maxiheaop y miniheap, que soloc ambian en las vueltas
Este es para miniheap

hijoIzq(i)= i*2+1
hijoDer(i)= i*2+2

padre(i)= (i-1)/2 ....debe ser pizo
13-jun-24 creo esta bien
17-ju-24 actualizado con delete
*/

#include <stdio.h>
#include <stdlib.h>
#include "functionsHeap.h"

void printHeap(heap h);

int main()
{
    heap hp;
    createMaxi_MiniHeap(&hp,5);//A.1 De crear el heap(array)con 10 espacios

    //meto unos cuantos elementos
    // Recuerda que se van metiendo de izqueird aa derecha de arriba a abajo
        // No importa si derecho es mayor que izquierdo o viceversa
    insertarMaxi_MiniHeapNodo(&hp,1);//A.2
    insertarMaxi_MiniHeapNodo(&hp,10);//A.2
    insertarMaxi_MiniHeapNodo(&hp,3);//A.2
    insertarMaxi_MiniHeapNodo(&hp,9);//A.2
    insertarMaxi_MiniHeapNodo(&hp,7);//A.2
    insertarMaxi_MiniHeapNodo(&hp,5);//A.2

    printHeap(hp);

    // Quito unos cuantos
        // recuerda que solo regresa el mas pequeño asi que no necesita cual borrar
    element a = deleteMaxiMiniHeap(&hp);// regresa 0
    // recuerda que para bajar baja con el hijo mas pequeño, asi que peud eir dercha o izqueirda
    printHeap(hp);

    element b = deleteMaxiMiniHeap(&hp);// regresa 1
    // Vi en debugger que los que voy sacado se pasan al final y no se borrar per se,
    // si tengo un 1 de heap y lo saco despyes se va a al final de todo, no sé porque
    // pero si funciona y regresa lo bueno
    printHeap(hp);
    //Libero memoria
    removeHeap(&hp);


    return 0;
}


// Insite functions

void printHeap(heap hp)
{
    printf("El array es:");
    for(int i = 0;i < hp.last;i++)
    {
        printf("%d,",hp.heap[i]);// MODIFICABLE CON BASE EN EL ELEMENT
    }
    printf("\n");
}

