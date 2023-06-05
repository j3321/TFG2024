# Se define la movilidad Dorkel que recibe como parámetros la temperatura
# y una lista de densidad de portadores
# Results is in cm2/Vs
import math

#######################
# VALORES PARA p-type #
#######################
UL0P = 495
ALPHAP = 2.2
AP = 1.17e+17
BP = 6.25e+14

#######################
# VALORES PARA n-type #
#######################
UL0N = 1430
ALPHAN = 2.2
AN = 4.61e+17
BN = 1.52e+15

####################
# VALORES GLOBALES #
####################
NDOP=1e+17 #unidades [cm^-3]
# NI = 1e+10 #unidades [cm^-3]
NC = 3e+19 #unidades [cm^-3]
NV = 1e+19 #unidades [cm^-3]
EG = 1.1242 #Energy Bandgap unidades [eV]
K = 8.617333262145e-5 #cte Boltzmann unidades [eV/K]


def dorkel_mode(temperatura, densidad_portadores):
    lista_movilidad_ptype = []
    lista_movilidad_ntype = []
    lista_movilidad_total = []
    #definir NI respecto a la variación de la temperatura
    NI = (math.sqrt(NC*NV)) * ((math.e)**((-EG)/(2*K*temperatura)))
    for i in range(len(densidad_portadores)):
        #calculo con p-type
        p0p = ((1/2) * ( NDOP + math.sqrt(NDOP**2 + 4*(NI**2)))) + densidad_portadores[i]
        n0p = (NI**2)/p0p
        uLp = (UL0P) * ((temperatura/300)**(-ALPHAP))
        uIp = ((AP) *((temperatura**(3/2))/NDOP)) * ((math.log10( 1 + ((BP *temperatura**2)/NDOP))) - ((BP * temperatura**2)/(NDOP+ BP * temperatura**2)))** (-1)
        Uccsp = ((2e+17 * (temperatura**3/2))/math.sqrt(p0p * n0p)) * ((math.log10(1 + 8.28e+8 * temperatura**2 * ((p0p * n0p)**(-1/3))))**(-1))
        Xp = math.sqrt((6 * uLp * (uIp + Uccsp)) / (uIp * Uccsp))
        up = (uLp) * ((1.025/(1+ (Xp/1.68)**1.43) - 0.025))
        # #calculo con n-type
        n0n = (1/2) * ( NDOP + math.sqrt(NDOP**2 + 4*(NI**2))) + densidad_portadores[i]
        p0n = (NI**2)/n0n
        uLn = (UL0N) * ((temperatura/300)**(-ALPHAN))
        uIn = ((AN) *((temperatura**(3/2))/NDOP)) * ((math.log10( 1 + ((BN *temperatura**2)/NDOP))) - ((BN * temperatura**2)/(NDOP+ BN * temperatura**2)))** (-1)
        Uccsn = ((2e+17 * (temperatura**3/2))/math.sqrt(p0n * n0n)) * ((math.log10(1 + 8.28e+8 * temperatura**2 * ((p0n * n0n)**(-1/3))))**(-1))
        Xn = math.sqrt((6 * uLn * (uIn + Uccsn)) / (uIn * Uccsn))
        un = (uLn) * ((1.025/(1+ (Xn/1.68)**1.43) - 0.025))
        #incluir el valor en la lista
        lista_movilidad_ptype.append(up)
        lista_movilidad_ntype.append(un)
        lista_movilidad_total.append(up+un)
    return lista_movilidad_total



    
    









