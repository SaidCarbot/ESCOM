/*
12-may-24
Por buenas prácticas de programación se creó este. Es el compendio
de los prototipos de las funciones inmersas en functionsLlist.c Además,
aquí definí las estruturas que usare. PARA LLIST SIMPLE CIRUCLARES
al 14-may-24 ya quedo
*/

#ifndef STRUCTS
#define STRUCTS

// A. Variables globales
    // A.1 nodos de la clista simple
    typedef struct cllistNode
{
    element e;
    struct cllistNode* next;
}
cllistNode;
    // A.2 para la clista completa en si
typedef struct cllist
{
   struct  cllistNode* first;
}
cllist;
// B. Prototipos de funciones
void createCllist(cllist* cclista);                                                     //B.1
int isEmptyCllist(cllist* cclista);                                                     //B.2
void insertNodeAtStartCllist(cllist* clista, element elemento);                         //B.3
void insertNodeAtEndCllist(cllist* clista, element elemento);                           //B.4
element removeAtStartCllist(cllist* clista);                                            //B.5
element removeAtEndCllist(cllist* clista);                                              //B.6
void eraseAllCllist(cllist* clista);                                                    //B.7
cllistNode* searchElementCllist(cllist* clista,element valorBuscado);                   //B.8
element deleteNodeElement(cllist* clista,element elemento);                             //B.9
void insertNodeAfterElementCllist(cllist* clista, element ParaMeter, element despuesDe);//B.10
void mostrarCllist(cllist* clista);                                                     //B.11
element deleteTHelement(cllist* clista, int posicionDelNodoParaBorrarlo);               //B.12
//B.13

#include "functionsCllist.c"
#endif
// Por Elian & Said Carbot Cruz Trejo, ESCOM-IPN, México-may-2024
