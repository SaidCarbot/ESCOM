/*
12-may-24
De la práctica 4 para casa Ejercicio 2. Implementa un tad de clista simple circular,
donde el siguiente del último elemento apuntará al primer elemento.
 Pide implementar:
 1) crear,ok
 2) esta vacía,ok
 3) insertar al inicio,ok
 4) insertar al final,ok
 5) insertar después de un elemento i,ok
 6) eliminar al inicio,ok
 7) eliminar al final,ok
 8) eliminar un elemento i,ok
 9) buscar un elemento,ok
 10) buscar un elemento i,ok
 11) eliminar toda la clista,OK
 12) imprimir clista.ok
// Notas mias
 1) YO INFIERO QUE NO ES AQUELLA QUE SEA FINITA EN TAMAÑO ASI QUE
 CIRCULO PUEDE HACERCE MAS Y MAS GRANDE
 2) hay dos ADT, para cCllist y cdllits; yo solo cCllist
 al 14-may-24 ya quedo
 */
#include <stdio.h>
#include <stdlib.h>
typedef int element; // MODIFICABLE base para el tipo de element
#include "functionsCllist.h"

// A) Global variables
// Todas están en el fucntionsCllist.h

// B) In Place Prototypes
// Todas están en el fucntionsCllist.h

// C) Main
int main() // if so, command-lines argument (int argc, string argv[])
{

    cllist clista;
    createCllist(&clista);                                                     // B.1
    element paraVerQueMetoYSaco;
    // Inserto
    printf("Inserto 1 al principio\n");
    insertNodeAtStartCllist(&clista,1);                                        // B.3
    printf("Veo si está\n");
    if(isEmptyCllist(&clista) == 0)
        printf("No esta vacia(Usando isEmptyCllist).\n");                                          // B.2
    printf("Inserto 2 al principio\n");
    insertNodeAtStartCllist(&clista,2);                                        // B.3
    printf("Inserto 3 al final\n");
    insertNodeAtEndCllist(&clista,3);
    printf("Inserto 4 al final\n");                                          // B.4
    insertNodeAtEndCllist(&clista,4);                                          // B.4
    //queda: 2134
    mostrarCllist(&clista);

    // Remuevo
    printf("Remuevo 2 del inicio\n");
    paraVerQueMetoYSaco = removeAtStartCllist(&clista);                                              // B.5
    printf("Lo removido fue %i del inicio\n",paraVerQueMetoYSaco);//MODIFICABLE con base en el tipo de element
    //queda 134
    mostrarCllist(&clista);
    printf("Remuevo 4 del final\n");
    paraVerQueMetoYSaco= removeAtEndCllist(&clista);
    printf("Lo removido fue %i del final\n",paraVerQueMetoYSaco);//MODIFICABLE con base en el tipo de element                                              // B.6
    //queda 13
    mostrarCllist(&clista);
    cllistNode* direccion= searchElementCllist(&clista,3);                      // B.8

    // INSERTO
    printf("Inserto 5 al final de la clista\n");
    insertNodeAtEndCllist(&clista,5);                                          // B.4
    //queda 135
    mostrarCllist(&clista);


    //BORRO
    printf("Borro el 5 que ya sé esta en final, pero supongo que no sé dond esta\n");
    paraVerQueMetoYSaco = deleteNodeElement(&clista,5);                                             // B.9
    printf("Lo borrado fue %i en lagun lado\n",paraVerQueMetoYSaco);//MODIFICABLE con base en el tipo de element                                              // B.6
    //queda 13
    mostrarCllist(&clista);

    // Inserto
    printf("Inserto el 6 despues de 3\n");
    insertNodeAfterElementCllist(&clista,6,3);// B.10
    //quedaria 136
    mostrarCllist(&clista);
    insertNodeAtEndCllist(&clista,7);
    insertNodeAtEndCllist(&clista,8);
    insertNodeAtEndCllist(&clista,9);
    //quedaria 136789
    insertNodeAtStartCllist(&clista,8);
    insertNodeAtStartCllist(&clista,7);
    //quedaria 78136789

    // borrar en enesima posicion
    element eEnNodoBuscado = deleteTHelement(&clista,6);
    printf("Lo borrado fue %i en la enesima posicion\n",eEnNodoBuscado);//MODIFICABLE con base en el tipo de element                                              // B.6
    /*Tuve que actualizar remover al final(B.6 y B.7) y pero no borrar(B.9) porque sí
    borraban pero cuando las use en deleteTHelement me di cuenta de que no regresaban
    el elemento borrado, ya quedo 14-05-24; sí funcionan las tres funciones, aunque en la
    enesima me falta el caso de que mete un enesimo mas grande que la cantidad de nodos
    en la clista, no lo pondré por tiempo.
    */

    // Borro todo
    printf("Borro toda la clista\n");
    eraseAllCllist(&clista);//IMPLEMENTADA OK                                                   // B.7
    printf("\n");
    return 0;
}
// D Inplace Functions
// Todas quedaron en fucntionsClist.h/.c

// Por Elian & Said Carbot Cruz Trejo, ESCOM-IPN, México-may-2024
