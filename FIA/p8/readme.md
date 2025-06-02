# Sistema Difuso: ¿Estás realmente cansado?

Este proyecto implementa un sistema de inferencia difuso utilizando `scikit-fuzzy`, `Matplotlib` y una interfaz gráfica con `Tkinter`. El objetivo es estimar el nivel de **fatiga** de una persona según tres variables de entrada:

- **Horas frente a pantalla** (`Screen Hours`)
- **Interrupciones o pausas** (`Halts`)
- **Nivel de ruido** (`Noise`)

## Requisitos

- Python 3.x
- tkinter (incluido en la mayoría de instalaciones de Python)
- numpy
- matplotlib
- scikit-fuzzy

Instalación de dependencias (si es necesario):

```bash
pip install numpy matplotlib scikit-fuzzy
```

## Descripción del sistema difuso

### Universos de discurso

Se definen universos para las variables de entrada y salida:

- `Screen Hours`, `Halts`, `Fatigue`: valores de 0 a 10.
- `Noise`: valores de 0 a 100.

### Variables lingüísticas

**Entradas:**

- `Screen Hours`: Few, Moderate, A lot  
- `Halts`: Few, Moderate, A lot  
- `Noise`: Low, Moderate, High

**Salida:**

- `Fatigue`: Not that much, Average, Zombie level

### Funciones de membresía

Se utilizan funciones `zmf`, `trapmf`, y `smf` para representar las categorías:

```python
screenHours['Few'] = fuzz.zmf(xScreenHours, 2, 4)
screenHours['Moderate'] = fuzz.trapmf(xScreenHours, [3, 5, 6, 7])
screenHours['A lot'] = fuzz.smf(xScreenHours, 6, 8)
```

La salida `fatigue` usa el método de desdifusificación `mom` (máximo de los máximos), que permite alcanzar valores extremos como 10.

### Reglas difusas

Se definen reglas lógicas con pesos personalizados para evitar solapamientos extremos:

```python
ctrl.Rule(screenHours['Few'] & halts['Few'] & noise['Low'], fatigue['Not that much'], 0.7)
ctrl.Rule(screenHours['A lot'] & halts['A lot'] & noise['High'], fatigue['Zombie level'], 1.5)
```

## Interfaz gráfica

- Se usan deslizadores (`ttk.Scale`) para ajustar los valores de entrada.
- El resultado numérico se actualiza automáticamente al mover los deslizadores.
- Un botón adicional permite visualizar las funciones de membresía de las entradas y la salida.

## Ejecución

Ejecuta el script principal:

```bash
python cansancio.py
```

## Autores

Desarrollado por Said Carbot & Aáron Ugalde
MEX-IPN-ESCOM-IIA-2025/2

---
