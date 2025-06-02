import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Universos para entradas y salida
xScreenHours = np.arange(0, 10.1, 0.1)
xHalts = np.arange(0, 10.1, 0.1)
xNoise = np.arange(0, 100, 0.1)
xFatigue = np.arange(0, 10.1, 0.1)


# Variables lingüisticas de entrada
screenHours = ctrl.Antecedent(xScreenHours, 'Screen Hours')
halts = ctrl.Antecedent(xHalts, 'Halts')
noise = ctrl.Antecedent(xNoise, 'Noise')


# Variable lingüistica de salida
fatigue = ctrl.Consequent(xFatigue, 'Fatigue')

# Funciones de membresía para ScreenHours,Halts,Noise
screenHours['Few'] = fuzz.zmf(xScreenHours, 2, 4)
screenHours['Moderate'] = fuzz.trapmf(xScreenHours,[3 ,5, 6, 7])
screenHours['A lot'] = fuzz.smf(xScreenHours, 6,8)


halts['Few'] = fuzz.zmf(xHalts, 2, 4)
halts['Moderate'] = fuzz.trapmf(xHalts, [3, 5, 6, 7])
halts['A lot'] = fuzz.smf(xHalts, 6, 8)

noise['Low'] = fuzz.zmf(xNoise, 30, 50)
noise['Moderate'] = fuzz.trapmf(xNoise, [40, 60, 70, 80])
noise['High'] = fuzz.smf(xNoise, 70, 85)

# Funciones de membresía para Fatigue
fatigue['Not that much'] = fuzz.zmf(xFatigue, 2, 4)
fatigue['Average'] = fuzz.trapmf(xFatigue, [3, 5, 6, 8])
fatigue['Zombie level'] = fuzz.smf(xFatigue, 7, 10)# no segui el ejemplo del pdf, se topaba hasta 8.46 la fatiga en la salida del programa
fatigue.defuzzify_method = 'mom'  # Usar el máximo de los máximos(mom) para poder alcanzar el 10 de fatigue, proque sino no dejaba
#mom preferencia el nivel zombie 


# Reglas difusas
# agregue peso (cuarto parametro de las reglas) para que no hubiera tantos solapameintos, no podia haber pesos repetidos
rules = [
    # Not that much (pesos bajo)
    ctrl.Rule(screenHours['Few'] & halts['Few'] & noise['Low'], fatigue['Not that much'], 0.7),
    ctrl.Rule(screenHours['Few'] & halts['Few'] & noise['Moderate'], fatigue['Not that much'], 0.71),
    ctrl.Rule(screenHours['Few'] & halts['Moderate'] & noise['Low'], fatigue['Not that much'], 0.72),
    ctrl.Rule(screenHours['Moderate'] & halts['Few'] & noise['Low'], fatigue['Not that much'], 0.8),

    # Average (pesos medios=
    ctrl.Rule(screenHours['Few'] & halts['Moderate'] & noise['Moderate'], fatigue['Average'], 1.0),
    ctrl.Rule(screenHours['Moderate'] & halts['Few'] & noise['Moderate'], fatigue['Average'], 1.01),
    ctrl.Rule(screenHours['Moderate'] & halts['Moderate'] & noise['Moderate'], fatigue['Average'], 1.02),
    ctrl.Rule(screenHours['Moderate'] & halts['A lot'] & noise['Low'], fatigue['Average'], 1.03),
    ctrl.Rule(screenHours['A lot'] & halts['Moderate'] & noise['Moderate'], fatigue['Average'], 1.1),

    # 🧟 level (pesos altos)
    ctrl.Rule(screenHours['A lot'] & halts['A lot'] & noise['High'], fatigue['Zombie level'], 1.5),
    ctrl.Rule(screenHours['A lot'] & halts['A lot'] & noise['Moderate'], fatigue['Zombie level'], 1.4),
    ctrl.Rule(screenHours['A lot'] & halts['Moderate'] & noise['High'], fatigue['Zombie level'], 1.41),
    ctrl.Rule(screenHours['Moderate'] & halts['A lot'] & noise['High'], fatigue['Zombie level'], 1.3),
]


sistema = ctrl.ControlSystem(rules)

# Cálculo automático
def calcular(event=None):
    sim = ctrl.ControlSystemSimulation(sistema)
    sim.input['Screen Hours'] = screenHours_slider.get()
    sim.input['Halts'] = halts_slider.get()
    sim.input['Noise'] = noise_slider.get()  # Nombre correcto
    sim.compute()
    resultado_var.set(f"Fatigue: {sim.output['Fatigue']:.2f}")  # Usa 'Fatigue' que es el nombre del Consequent
    screenHours_valor.set(f"{screenHours_slider.get():.1f}")
    halts_valor.set(f"{halts_slider.get():.1f}")
    noise_valor.set(f"{noise_slider.get():.1f}")
# Mostrar gráficas en la ventana
def mostrar_graficas():
    ventana_graf = tk.Toplevel(ventana)
    ventana_graf.title("Funciones de membresía")
    fig = Figure(figsize=(10, 8))
    axs = [fig.add_subplot(411), fig.add_subplot(412), fig.add_subplot(413), fig.add_subplot(414)]

    # Screen Hours
    for etiqueta in screenHours.terms:
        axs[0].plot(xScreenHours, screenHours[etiqueta].mf, label=etiqueta)
    axs[0].set_title('Screen Hours')
    axs[0].legend()
    axs[0].grid(True)

    # Halts
    for etiqueta in halts.terms:
        axs[1].plot(xHalts, halts[etiqueta].mf, label=etiqueta)
    axs[1].set_title('Halts')
    axs[1].legend()
    axs[1].grid(True)

    # noise
    for etiqueta in noise.terms:
        axs[2].plot(xNoise, noise[etiqueta].mf, label=etiqueta)
    axs[2].set_title('Noise')
    axs[2].legend()
    axs[2].grid(True)

    # Fatigue 
    for etiqueta in fatigue.terms:
        axs[3].plot(xFatigue, fatigue[etiqueta].mf, label=etiqueta)
    axs[3].set_title('Fatigue')
    axs[3].legend()
    axs[3].grid(True)

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=ventana_graf)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Crear GUI
ventana = tk.Tk()
ventana.title("Are you really tired?")
ventana.geometry("400x400")

frame = tk.Frame(ventana)
frame.pack(pady=5, fill='x')

# Deslizantes
tk.Label(frame, text="Screen Hours (0-10)").pack(anchor='w')
screenHours_slider = ttk.Scale(frame, from_=0, to=10, orient='horizontal', command=calcular)

screenHours_slider.pack(fill='x', padx=10)
screenHours_valor = tk.StringVar(value="0.0")
tk.Label(frame, textvariable=screenHours_valor).pack(anchor='e', padx=10)

tk.Label(frame, text="Halts (0-10)").pack(anchor='w')
halts_slider = ttk.Scale(frame, from_=0, to=10, orient='horizontal', command=calcular)
halts_slider.pack(fill='x', padx=10)
halts_valor = tk.StringVar(value="0.0")
tk.Label(frame, textvariable=halts_valor).pack(anchor='e', padx=10)

tk.Label(frame, text="noise (Noise)").pack(anchor='w')
noise_slider = ttk.Scale(frame, from_=0, to=100, orient='horizontal', command=calcular)
noise_slider.pack(fill='x', padx=10)
noise_valor = tk.StringVar(value="0.0")
tk.Label(frame, textvariable=noise_valor).pack(anchor='e', padx=10)

# Resultado
resultado_var = tk.StringVar()
tk.Label(ventana, textvariable=resultado_var, font=('Arial', 14)).pack(pady=10)

# Botón de gráficas
tk.Button(ventana, text="Ver funciones de membresía", command=mostrar_graficas).pack(pady=5)


ventana.mainloop()

#By Said Carbot & Aáron Ugalde
#MEX-IPN-ESCOM-IIA-2025/2
