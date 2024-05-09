# Se declaran las variables que hay que solicitar al usuario.

import numpy as np

def obtener_NDOP(resistividad):
    # Rango de resistividades conocidas
    resistividades_conocidas_precisas = np.arange(1, 21)
    concentraciones_conocidas_precisas = np.array([1.51205e+16, 7.16977e+15, 4.68405e+15, 3.47447e+15, 2.76188e+15,
                                                  2.28958e+15, 1.95494e+15, 1.70548e+15, 1.51238e+15, 1.35849e+15,
                                                  1.23298e+15, 1.12868e+15, 1.04062e+15, 9.65292e+14, 9.00121e+14,
                                                  8.43184e+14, 7.93014e+14, 7.48473e+14, 7.08665e+14, 6.72873e+14])
    resistividades_conocidas_simplificadas = np.arange(20, 101, 10)
    concentraciones_conocidas_simplificadas = np.array([6.72873e+14, 4.27446e+14, 2.73822e+14, 1.91503e+14,
                                                        1.44142e+14, 1.13833e+14, 9.14722e+13, 7.54144e+13,
                                                        6.44331e+13, 5.42615e+13])

    # Interpolación lineal para resistividades del 1 al 20
    if resistividad <= 20:
        concentracion_aprox = np.interp(resistividad, resistividades_conocidas_precisas, concentraciones_conocidas_precisas)
    # Interpolación lineal para resistividades de 20 a 100
    else:
        concentracion_aprox = np.interp(resistividad, resistividades_conocidas_simplificadas, concentraciones_conocidas_simplificadas)
    return concentracion_aprox


def solicitar_valor(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print(f"Por favor, introduce un valor numérico válido para {mensaje}.")

print("Valores Tipicos: W[cm]= 0.0300  OPTICAL_FACTOR: 0.70 ") 
W = solicitar_valor("Introduce el valor de W en [cm]: ")
OPTICAL_FACTOR = solicitar_valor("Introduce el valor de OPTICAL_FACTOR: ")
#NDOP = solicitar_valor("Introduce el Valor de NDOP en [cm^-3]: ")
BASE_RESISTIVITY = solicitar_valor("Introduce el Valor de la Resistividad Base en [ohm-cm]: ")
NDOP = obtener_NDOP(BASE_RESISTIVITY)
print("NDOP = ", NDOP )





#Código Shangde

"""
W = float(input("Introduce el valor de W en [cm]: "))
OPTICAL_FACTOR = float(input("Introduce el valor de OPTICAL_FACTOR: "))
NDOP = float(input("Introduce el Valor de NDOP en [cm^-3]: "))
"""