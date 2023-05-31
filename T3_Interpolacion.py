!pip install numpy
!pip install scipy
!pip install matplotlib

# ---------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline as CS

# ---------------------------------------------

# Iniciamos creando una función de python donde guardamos la función a plotear.
def funcion_a_plotear(x):
    return 1 / (1 + 9 * (x**2))

x = np.linspace(-2, 2, 1000) # Definimos el dominio, pero no de los splines sino del canvas en el que python va a dibujar nuestras lineas.
y = funcion_a_plotear(x) # Aquí llamamos a la función de python donde guardamos nuestra función a graficar.

# Definimos el figsize, y ploteamos la función, por ahora no hemos ploteado los splines.
plt.figure(figsize = (10, 6))
plt.plot(x, y, label = '$f(x) = 1 / 1+9x^2$')


# GENERANDO SPLINES
# Generamos con un loop los splines de todos los puntos que pidió.
for n in [6, 8, 10, 13]: # Mientras más puntos tenga el spline, se parecerá más a nuestra función.
    x_spline = np.linspace(-2, 2, n) # Aquí es donde aplicamos el dominio de los splines. # n es el número de puntos que queremos en el spline.
    y_spline = funcion_a_plotear(x_spline) # Aquí volvemos a llamar a la función de python f(x) y les aplica los valones que establecimos arriba.
    plt.plot(x_spline, y_spline, label = f'Spline con {n} puntos')

# Ploteamos y añadimos formato a la gráfica.
plt.title('Splines de Grado 1 para $f(x)=\dfrac{1}{1+9x^2}$')
plt.legend()
plt.grid(True)
plt.show()

# ---------------------------------------------

def interpolacion_lagrange(puntos: np.ndarray, x: np.ndarray, y_puntos_evaluados):

    l = [1] * len(puntos)

    for k in range(len(puntos)):
        for j in range(len(puntos)):
            if k != j:
                l[k] = l[k] * ((x - puntos[j]) / (puntos[k] - puntos[j]))

    resultado_final = y_puntos_evaluados[0] * l[0]

    for i in range(1, len(puntos)):
        resultado_final += y_puntos_evaluados[i] * l[i]

    return resultado_final


fig, axes = plt.subplots(2, 2, figsize=(10, 6))

for i, n in enumerate([6, 8, 10, 13]):
    x_spline = np.linspace(-2, 2, n)
    y_spline = funcion_a_plotear(x_spline)

    x_extra = np.linspace(-2, 2, 1000)
    lagrange = interpolacion_lagrange(x_spline, x_extra, y_spline)

    row = i // 2
    col = i % 2

    ax = axes[row, col]
    ax.plot(x_extra, lagrange, label = f"Lagrange")
    ax.scatter(x_spline, y_spline, label = f"{n} puntos")
    ax.plot(x, y, label = '$f(x)=\dfrac{1}{1+9x^2}$', linewidth = 2, linestyle = '--')

    ax.set_title(f'Interpolación de Lagrange con {n} puntos')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()

# ---------------------------------------------

x = np.linspace(-2, 2, 1000)

fig, ax = plt.subplots(3, 1, figsize = (8, 8))

condiciones_limites = ['clamped', 'natural', 'not-a-knot']

for i, sp in enumerate(condiciones_limites):
    ax[i].plot(x, funcion_a_plotear(x), label = '$f(x) = 1 / (1+9x^2)$', linewidth = 5, linestyle = ':')
    
    for n in [6, 8, 10, 13]:
        x_spline = np.linspace(-2, 2, n)
        y_spline = funcion_a_plotear(x_spline)

        if sp == 'clamped':
            cs = CS(x_spline, y_spline, bc_type = sp, extrapolate = True)
        elif sp == 'natural':
            cs = CS(x_spline, y_spline, bc_type = sp, extrapolate = True)
        elif sp == 'not-a-knot':
            cs = CS(x_spline, y_spline, bc_type = sp)
            
        y_spline_interp = cs(x)
        ax[i].plot(x, y_spline_interp, label = f'Spline {sp} con {n} puntos')

    ax[i].set_title(f'Spline {sp} para $f(x) = 1 / (1+9x^2)$')
    ax[i].legend()
    ax[i].grid(True)

plt.tight_layout()
plt.show()

# ---------------------------------------------

h = 3
k = 3

puntos_control_izquierda = np.array([[-1, 0], [-1, k/3], [-h/3, 1], [0, 1]])
puntos_control_derecha = np.array([[0, 1], [h/3, 1], [1, k/3], [1, 0]])

t = np.linspace(0, 1, 100)

def calcular_puntos_curva_bezier(puntos_control, t):
    return (
        puntos_control[0]*(1-t)**3
        + puntos_control[1]*3*t*(1-t)**2
        + puntos_control[2]*3*(1-t)*t**2
        + puntos_control[3]*t**3
    )

coordenadas_bezier_x_izq = calcular_puntos_curva_bezier(puntos_control_izquierda[:, 0], t)
coordenadas_bezier_y_izq = calcular_puntos_curva_bezier(puntos_control_izquierda[:, 1], t)
coordenadas_bezier_x_der = calcular_puntos_curva_bezier(puntos_control_derecha[:, 0], t)
coordenadas_bezier_y_der = calcular_puntos_curva_bezier(puntos_control_derecha[:, 1], t)

coordenadas_bezier_x = np.concatenate((coordenadas_bezier_x_izq, coordenadas_bezier_x_der))
coordenadas_bezier_y = np.concatenate((coordenadas_bezier_y_izq, coordenadas_bezier_y_der))

plt.figure()
plt.plot(coordenadas_bezier_x, coordenadas_bezier_y)
puntos_control = np.concatenate((puntos_control_izquierda, puntos_control_derecha))
plt.scatter(puntos_control[:, 0], puntos_control[:, 1], color='black')
plt.title("Curva de Bézier")
plt.show()