# Clasificación de CIFAR-100: CNN desde cero, Transfer Learning y Fine-Tuning

Este repositorio contiene el desarrollo, entrenamiento y evaluación de múltiples arquitecturas de Redes Neuronales Convolucionales (CNN) para resolver el problema de clasificación de imágenes del dataset **CIFAR-100** (etiquetas finas de 100 clases). 

Contiene: 
- **Reporte en PDF**
- **Archivo ipyn con la primera tarea**
- **Archivo ipyn con la segunda tarea**

Este proyecto fue desarrollado como parte de las actividades de la asignatura de Redes Neuronales y Aprendizaje Profundo en la Escuela Superior de Cómputo (ESCOM). El objetivo principal es demostrar un proceso experimental controlado dividido en dos grandes fases:
1. Diseño de arquitecturas desde cero y prevención del sobreajuste.
2. Adaptación de modelos preentrenados masivos (ImageNet) mediante técnicas de Transfer Learning y Fine-Tuning protegido.

---

## Entorno y Requisitos

El código está optimizado para ejecutarse en **Google Colab** utilizando aceleración por hardware. Consta de dos cuadernos independientes (`.ipynb`) para evitar la saturación de la memoria.

### Ejecución en Google Colab
Todas las bibliotecas utilizadas están preinstaladas de forma nativa en el entorno de Colab. 
**Importante:** Para que el entrenamiento se realice en un tiempo óptimo, es obligatorio activar el uso de GPU.
1. Ve al menú `Entorno de ejecución` > `Cambiar tipo de entorno de ejecución`.
2. En `Acelerador de hardware`, selecciona **T4 GPU** (o superior).

### Ejecución Local
Si deseas correr estos cuadernos en tu máquina local, necesitarás tener Python instalado y ejecutar el siguiente comando para instalar las dependencias necesarias:

### Nota sobre tiempos de ejecución
Cuidado con las ejecuciones pues se tarda como 30 minutos en el modelo de TL/FT con mejores reusultados usando GPU

```bash
pip install tensorflow matplotlib numpy pandas seaborn scikit-learn
