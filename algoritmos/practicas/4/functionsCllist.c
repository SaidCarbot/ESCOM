/*
12-may-24
Compendio del desarrollo de funciones correctas para clistaS ENLAZADAS SIMPLES CIRCULARES
que yo nombrare cllist
al 14-may-24 ya quedo*/

#include <stdio.h>
#include <stdlib.h>
#include "functionsCllist.h"

/* A Functions
INDICE
    A.1 createCllist
    A.2 isEmptyCllist
    A.3 insertNodeAtStartCllist
    A.4 insertNodeAtEndCllist
    A.5 removeAtStartCllist
    A.6 removeAtEndCllist
    A.7 eraseAllCllist
    A.8 searchElementCllist
    A.9 deleteNodeElementCllist
    A.10 inserNodeAfterElementCllist
    A.11 mostrar clista simple
    A.12 eliminar el enesimo elemnto
    */

//A.1 createCllist
void createCllist(cllist* clista)
{
    clista->first = NULL;
}
//A.2 isEmptyCllist
int isEmptyCllist(cllist* clista)
{
    if(clista->first == NULL)
            //printf("La clista simple esta vacia(isEmptyCllist).\n");
            return(1);
    return(0);
}
//A.3 insertNodeAtStartCllist
void insertNodeAtStartCllist(cllist* clista, element elemento)
{
    // Caso cuando esta vacia
    cllistNode* new = (cllistNode*) malloc(sizeof(cllistNode));
    if(isEmptyCllist(clista))
    {
        new->e = elemento;
        new->next = clista->first = new;// apunto el next del nodo y
        // el first d ela lista a nodo mismo
    }
    // Caso cuando NO esta vacia
    else
    {
        new->next = clista->first;//1
        new->e = elemento;//2
        cllistNode* aux = clista->first;//3
        while (aux->next != clista->first)// mientras no este apuntando
        // al final -inicio
            aux = aux->next;//4 recorro hasta que sea al final-primero
        aux->next = clista->first = new;// cuando ya es el final-primero
        // muevo el first al nuevos
    }
}
//A.4 insertNodeAtEndLlist
void insertNodeAtEndCllist(cllist* clista, element elemento)
{
    if(isEmptyCllist(clista))
        insertNodeAtStartCllist(clista,elemento);
    else
    {
        cllistNode* new = (cllistNode*) malloc(sizeof(cllistNode));
        new->e = elemento;

        // Recorro hasta el final, pero solo en los next(nodo), no en los element
        cllistNode* aux;
        aux = clista->first;
        while(aux->next != clista->first)
            aux = aux->next;
        aux->next = new;// esta es la direccion a la que apunta el ultimo
        new->next = clista->first;
    }
}

//A.5 removeAtStartCllist
element removeAtStartCllist(cllist* clista)
{
    if(isEmptyCllist(clista))
    {
        printf("La clista ya esta vacia(removeAtStartCllist).\n");
        return(1);// MODIFICABLE tiene que coincidir con element
    }
    else
    {
        cllistNode* aux = clista->first;
        element elemento = aux->e;
        // Son dos casos
        // 1 Cuando quedaría sin nodos
        if(clista->first->next == clista->first)
            clista->first = NULL;
        // 2 cuando en la lista SI quedan nodos
        else
        {
            cllistNode* last = clista->first;
            while(last->next != clista->first)//recorrer lista hasta fin-inicio
            // pero solo en los next, no en los element
                last = last->next;
            last->next = clista->first = aux->next;// el next del ultimo nodo y la direccion de
            // memporia dle primero son ahora la direccion del nodo auxilar donde
            // se gaurdo la dirección del primero priemro
        }
        elemento = aux->e;
        free(aux);
        return elemento;
    }
}
//A.6 removeAtEndLlist ME QUEDE ACA, FALTA LO DE ABAJO
element removeAtEndCllist(cllist* clista)
{
    // Son tres casos,cuando est avacia, cuando hay un solo nodo y  cuando hay mas de un nodo
    if(isEmptyCllist(clista))
    {
        printf("La clista está vacia(removeAtEndCllist).\n");
        return 1;//MODIFICABLE con base en mi ele, si son int => 1 si son char finao cadena
    }
    else
    {
        cllistNode* aux = clista->first;
        element elemento = aux->e;
        // caso dos, solo un nodo
        if(clista->first->next == clista->first)
            clista->first->next = NULL;
        // caso 3, mas d eun nodo
        else
        {
            cllistNode* penultimo = clista->first;
            while(penultimo->next->next != clista->first)//recorrer lista hasta penultimo
            // IMPORTANTE LO DE ARRIBA
                penultimo = penultimo->next;
            // De apuntar el nuevo ultimo nodo al principio para
            // mantener cirucularidad y actualziar el valor de first al nuevo priemro
            aux = penultimo->next;// Actualizo aux al ultimo nodo para borrar el ultimo
            penultimo->next = clista->first; //actualizo el nuevo nodo final-inicio
            // para que apunte al inciio de la lista
        }
    elemento = aux->e;
    free(aux);
    return elemento;
    }
}

//A.7 eraseAllLList
void eraseAllCllist(cllist* clista)
{
    printf("Borrando toda la lista\n");
    while(!isEmptyCllist(clista))
       removeAtStartCllist(clista);
    printf("Ahora la cllist está vacia(eraseAllCllist)\n");
}

//A.8 searchElementCllist
cllistNode* searchElementCllist(cllist* clista,element valorBuscado)
{
    cllistNode* aux = clista->first;
    do
    {
        if (aux->e == valorBuscado)
            // Si encontramos el nodo con el valor deseado, devolvemos
            //su dirección de memoria
            return aux;
        aux = aux->next;
    }
    while(aux != clista->first);// IMPORTANTE recorrer toda la clista en sus element
    // Si no se encuentra el valor deseado en la clista, devolvemos NULL
    printf("No se encontro el valor deseado(searchElementCllist).\n");
    return NULL;
}
// A.9 deleteNodeElement
// este si importa cual borro, puede ser el ultimo, pero yo no sé donde estén
element deleteNodeElement(cllist* clista,element elemento)
{
    cllistNode *aux,*f;
    element elementoElminado;
    f = searchElementCllist(clista,elemento);
    if(f != NULL)
    {
        // Si es el nodo a eliminar es el inicio-fin
        if(clista->first->next == NULL || elemento == clista->first->e)
        {
            elementoElminado = removeAtStartCllist(clista);
            return elementoElminado;
        }
        aux = clista->first;

        while(aux->next != f)
            aux = aux->next;
        if(f->next == clista->first)
            aux->next = clista->first;
        else
            aux->next = f->next;
        elementoElminado = f->e;
        free(f);
        return elementoElminado;
    }
    // sino existe en la clista
    printf("El emlemnto buscado no esta en la clista(deleteNodeElement).\n");
    return 1;//MODIFICABLE CON BAS EN EL TIPO DE ELEMENT
}

// A.10 inserNodeAfterElementLlist
void insertNodeAfterElementCllist(cllist* clista, element paraMeter, element despuesDe)
{
    cllistNode *nuevo, *p;
    p = searchElementCllist(clista, despuesDe);

    // Si se encuentra el nodo después del cual se debe insertar
    if (p != NULL)
    {
        nuevo = (cllistNode*)malloc(sizeof(cllistNode)); // Asignar memoria para el
        // nuevo nodo
        if (nuevo == NULL)
            printf("Error: No se pudo asignar memoria para el nuevo nodo (insertNodeAfterElementCllist).\n");
        nuevo->e = paraMeter;
        nuevo->next = p->next;
        p->next = nuevo;

        // Si el nodo después del cual se inserta es el último nodo de la lista
        if (p->next == clista->first)
            clista->first = nuevo; // El nuevo nodo ahora es el primer nodo
    }
    else
        printf("El elemento buscado no fue encontrado (insertNodeAfterElementCllist).\n");
}

// A.11 Mostrar clista simple
void mostrarCllist(cllist* clista)
{
    if(isEmptyCllist(clista))
        printf("La clista esta vacia(mostrarLlist).\n");
    cllist aux;
    createCllist(&aux);
    printf("clista: ");
    // Creo una lista simple circular auxiliar para no mover original y le voy haciendo
    // pop para ver el primero de la lista y asi hasta que est evacia, o sea como se borra el que voy haicendo pop,
    // entocnes esta bien que vaya viendo solo el primero
    while(!isEmptyCllist(clista))
    {
        element auxE = removeAtStartCllist(clista);   // deque
        printf("%i ",auxE);
        insertNodeAtStartCllist(&aux,auxE);     // enque
    }
    printf("\n");

    // regreso los datos a la original
    while(!isEmptyCllist(&aux))
    {
        element auxE = removeAtStartCllist(&aux);   // B.4
        insertNodeAtStartCllist(clista,auxE);
    }
    printf("\n");
}

/* A.12 eliminar el enesimo elemnto:
borrar el enesimo, como si fuera un array, devuelve el elemento eliminado
si fuera abc en miembro elemento de structs y borro el 3th nodo entonces devuelvo c
Son 5 casos */
element deleteTHelement(cllist* clista, int posicionDelNodoParaBorrarlo)
{
    // caso 1 Si esta vacia
    if(isEmptyCllist(clista))
    {
        printf("La clista esta vacia(deleteTHelement).\n");
        return 0; //MODIFICABLE  con base en el tipo de element
    }

    int contadorPosicion = 1;
    cllistNode* auxActual = clista->first;
    cllistNode* auxAnterior = NULL;
    element eliminado = 0;
    // Recorro mientras la posicion no sea la buscada
    // ASI RECORRO DE INCIIO A FIN NODOS IMPORTANTE
    while(contadorPosicion != posicionDelNodoParaBorrarlo)
    {
        auxAnterior = auxActual;
        auxActual = auxActual->next;
        contadorPosicion++;
    }

    // caso 2, sino esta vacia y si el nodo está al final
    if(auxActual == clista->first)
        return(removeAtStartCllist(clista));

    // caso 3 sino esta vacia y el nodo está al final
    if(auxActual->next == clista->first)
        return(removeAtEndCllist(clista));

    // Caso 4 sino está vacia y está enmedio entocnes puenteo el nodo
    // anterior con el siguiente de donde esta el nodo que borrare
    auxAnterior->next = auxActual->next;// puenteo
    // guardo el valor del miebro e del nodo
    eliminado = auxActual->e;
    free(auxActual);
    return eliminado;
}

// Por Elian & Said Carbot Cruz Trejo, ESCOM-IPN, México-may-2024
