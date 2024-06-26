# Se emplea la librería para suavizar la curva y quitar ruido, posteriormente posibilita ajustar
# de una manera más precisa la curva y calcular los valores
import statsmodels.api as sm
import numpy as np
from scipy.optimize import curve_fit
import math
from sklearn.linear_model import LinearRegression
from . import input_values
from sklearn.metrics import r2_score


# Definición de constantes
NDOP=1e+15 #unidades [cm^-3]
Q = 1.6e-19 #[Coulomb]
W= 0.0300 #Unidades : [cm]
NC = 3e+19 #unidades [cm^-3]
NV = 1e+19 #unidades [cm^-3]
EG = 1.1242 #Energy Bandgap unidades [eV]
K = 8.617333262145e-5 #cte Boltzmann unidades [eV/K]
temperatura = 300

W = input_values.W
NDOP = input_values.NDOP

# Se suaviza la curva 
def suavizado_curva(lista_tiempo_srh, lista_densidad_portadores):
    # Se importa el módulo lowess
    lowess = sm.nonparametric.lowess
    # Se aplica el suavizado
    curva_suavizada = lowess(lista_tiempo_srh, lista_densidad_portadores)
    lista_densidad_portadores_suave = curva_suavizada[:, 0]
    lista_srh_suave = curva_suavizada[:, 1]
    return lista_srh_suave, lista_densidad_portadores_suave

def ajuste_minimo_curva(lista_tiempo_srh, lista_tiempo_srh_suave):
    # Convertir la lista en array numpy
    lista_tiempo_srh_np = np.array(lista_tiempo_srh)
    lista_tiempo_srh_suave_np = np.array(lista_tiempo_srh_suave)
    # Calcular la diferencia entre los valores de las dos listas
    diferencia = np.abs(lista_tiempo_srh_np - lista_tiempo_srh_suave_np)
    indice_parecido = np.argmin(diferencia)
    return indice_parecido
# Se tiene una función lineal del tipo A = B + CX, de los cuales se conocen A y C
# Mediante el ajuste de curvas de una función lineal, se pretende ajustar las incógnitas
# B y la pendiente X
def custom_curve_fit(lista_densidad_portadores, lista_tiempo_srh): #(X,Y)
    def linear_func(x, m, c):
        return [c + m*xi for xi in x]
    # Se calcula el valor independiente conocido
    NI = (math.sqrt(NC*NV)) * ((math.e)**((-EG)/(2*K*temperatura)))
    lista_valor_independiente = []
    for i in range(len(lista_densidad_portadores)):
        indice = (NDOP + lista_densidad_portadores[i])/(Q*W*(math.pow(NI,2)))
        lista_valor_independiente.append(indice)
    # Se formatean a arrarys numpy
    lista_valor_independiente_np = np.array(lista_valor_independiente)
    lista_tiempo_srh_np = np.array(lista_tiempo_srh)
    # Se aplica el ajuste de curvas siendo popt el valor óptimo y pcov los valores de covarianza
    popt, pcov = curve_fit(linear_func, lista_valor_independiente_np, lista_tiempo_srh_np)
    # Obtener los valores de SRH y J0E
    SRH = popt[0]
    J0E = popt[1]
    valores_ajustados = linear_func(lista_valor_independiente, SRH, J0E)
    return SRH, J0E, valores_ajustados 

def custom_linear_fit(lista_densidad_portadores, lista_tiempo_srh):
    # Se calcula el valor independiente conocido
    NI = (math.sqrt(NC*NV)) * ((math.e)**((-EG)/(2*K*temperatura)))
    lista_valor_independiente = []
    for i in range(len(lista_densidad_portadores)):
        indice = (NDOP + lista_densidad_portadores[i])/(Q*W*(math.pow(NI,2)))
        lista_valor_independiente.append(indice)
    
    # Se formatean a arrarys numpy
    lista_valor_independiente_np = np.array(lista_valor_independiente).reshape(-1, 1)
    lista_tiempo_srh_np = np.array(lista_tiempo_srh)
    
    # Crear un objeto de regresión lineal y ajustar el modelo
    regresion_lineal = LinearRegression()
    regresion_lineal.fit(lista_valor_independiente_np, lista_tiempo_srh_np)
    
    # Obtener los coeficientes de la regresión
    SRH = regresion_lineal.coef_[0]
    J0E = regresion_lineal.intercept_
    
    # Calcular los valores ajustados
    valores_ajustados = regresion_lineal.predict(lista_valor_independiente_np)
    
    return SRH, J0E, valores_ajustados


def one_linear_fit(X,Y):
    def linear_func(x, m, b):
        return m * x + b
    # Ajustar los parámetros usando curve_fit 
    popt, pcov = curve_fit(linear_func, X, Y)
    m_1recta, b_1recta = popt
    fit_values_1recta = linear_func(X, m_1recta, b_1recta)

    # Calcular el coeficiente de determinación R^2
    r2 = r2_score(Y, fit_values_1recta)

    return fit_values_1recta, r2, m_1recta, b_1recta

def dual_linear_fit(X, Y):
# Definir la función Fit
    def fit_function(X, m1, b1, m2, b2):
        term1 = 1 / (m1 * X + b1)
        term2 = 1 / (m2 * X + b2)
        fit = 1 / (term1 + term2)
        return fit
    def linear_func(x, m, b):
        return m * x + b
    
    # Ajustar los parámetros usando curve_fit 
    popt, pcov = curve_fit(fit_function, X, Y)

    # Obtener los valores ajustados de los parámetros
    m1, b1, m2, b2 = popt
    # Calcular los valores ajustados de Fit
    fit_values = fit_function(X, m1, b1, m2, b2)
    #Calculamos los valores de cada fit
    fit_values_1 = linear_func(X, m1, b1)
    fit_values_2 = linear_func(X, m2, b2)

    # Calcular el coeficiente de determinación R^2
    r2 = r2_score(Y, fit_values)
  
    return fit_values_1, fit_values_2, fit_values, r2, m1, m2, b1, b2
    
    
def custom_gradient(lista_densidad_portadores, lista_tiempo_srh):
     # Se calcula el valor independiente conocido
    NI = (math.sqrt(NC*NV)) * ((math.e)**((-EG)/(2*K*temperatura)))
    lista_valor_independiente = []
    for i in range(len(lista_densidad_portadores)):
        indice = (NDOP + lista_densidad_portadores[i])/(Q*W*(math.pow(NI,2)))
        lista_valor_independiente.append(indice)

    # Se formatean a arrays numpy
    lista_valor_independiente_np = np.array(lista_valor_independiente)
    lista_tiempo_srh_np = np.array(lista_tiempo_srh)

    # Se calcula la pendiente
    J0e = np.gradient(lista_tiempo_srh_np, lista_valor_independiente_np)

    # Se calcula el término independiente

    SRH = lista_tiempo_srh_np - (2 * J0e * lista_valor_independiente_np)

    lista_srh_ajustada = SRH + (2 * J0e * lista_valor_independiente_np)

    return SRH, J0e, lista_srh_ajustada








