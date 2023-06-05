# Se define la movilidad Sinton que recibe como parámetro una lista de la densidad de portadores
#Result is in cm2/Vs
import math
NDOP=1e+17 #unidades [cm^-3]
def sinton_mode(temperatura, densidad_portadores):
    lista_movilidad = []
    for i in range(len(densidad_portadores)):
        C=densidad_portadores[i]+NDOP
        f=0.8431* math.log10(C/1.2e+18)
        movilidad= 1800 * ((1+10**f)/(1+8.36*10**f))
        lista_movilidad.append(movilidad)
    return lista_movilidad


