# Se define la movilidad Sinton que recibe como parámetro una lista de la densidad de portadores
#Result is in cm2/Vs
import math
from .. import input_values
NDOP=input_values.NDOP
def sinton_mode(temperatura, densidad_portadores):
    lista_movilidad = []
    for i in range(len(densidad_portadores)):
        C=densidad_portadores[i]+NDOP
        f=0.8431* math.log10(C/1.2e+18)
        movilidad= 1800 * ((1+10**f)/(1+8.36*10**f))
        lista_movilidad.append(movilidad)
    return lista_movilidad


