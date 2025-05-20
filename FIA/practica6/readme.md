# 🧠 Sistema Experto en Tipos de Neuronas

> Sistema experto basado en reglas para la identificación interactiva de tipos de neuronas.

---

## 📋 Descripción

Este proyecto implementa un **sistema experto basado en reglas** que permite deducir el tipo de neurona (sensorial, interneurona, motora, inhibidora o excitadora) a partir de respuestas del usuario.  
Está desarrollado en **Prolog**, utilizando lógica de predicados y un motor lógico que interactúa con el usuario mediante preguntas simples de sí/no.

---

## ⚙️ Estructura del Sistema

- **Menú Principal:**  
  Permite consultar el tipo de neurona o salir del programa.

- **Motor Lógico:**  
  Realiza la inferencia y muestra el resultado según las respuestas almacenadas.

- **Lógica de Inferencia:**  
  Verifica si un atributo es cierto, falso, o necesita preguntarse al usuario.

- **Interacción con el Usuario:**  
  Formula preguntas para recolectar información sobre los atributos de la neurona.

- **Base de Conocimientos:**  
  Contiene las reglas que definen los distintos tipos de neuronas y sus características.

---

## 🚀 Uso

1. Cargar el archivo Prolog en tu intérprete (ej. SWI-Prolog):

    ```prolog
    ?- [nombre_del_archivo].
    ```

2. Ejecutar el predicado principal:

    ```prolog
    ?- main.
    ```

3. Seguir las instrucciones del menú y responder las preguntas con:

   - **s** o **si** para "sí"  
   - Cualquier otra respuesta se interpreta como "no"

---

## 💡 Ejemplo de interacción

```prolog
?- main.
Sistema experto en tipos de neuronas

Menú

1 Consultar el tipo de neurona
2 Salir

Teclea tu opción: 
|: 1.

¿Tu neurona detecta_estimulos? (s/si para sí, cualquier otra para no) s.

¿Tu neurona es_unipolar_o_bipolar? (s/si para sí, cualquier otra para no) si.

...

Deduzco que el tipo de neurona es: sensorial

Tal que: [detecta_estimulos, es_unipolar_o_bipolar, envia_a_interneuronas_o_medula, responde_a_luz]
