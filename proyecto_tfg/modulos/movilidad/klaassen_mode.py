# Se define la movilidad Klaassen tomando como parámetros la temperatura y 
# una lista de densidad de portadores
#Results is in cm2/Vs
import math

###########################
# VALORES PARA ELECTRONES #
###########################
UMAXE = 1414
UMINE = 68.5
U1E = 56.1
NREF1E = 9.2e+16
NREF2E = 3.4e+20
ALPHA1E = 0.711
ALPHA2E = 1.98
CIE = 0.21
NREFIE = 4e+20
MIM0E = 1

#######################
# VALORES PARA HUECOS #
#######################
UMAXH = 470.5
UMINH = 44.9
U1H = 29
NREF1H = 2.23e+17
NREF2H = 6.1e+20
ALPHA1H = 0.719
ALPHA2H = 2.0
CIH = 0.5
NREFIH = 7.2e+20
MIMOH = 1.258

####################
# VALORES GLOBALES #
####################
S1 = 0.89233
S2 = 0.41372
S3 = 0.19778
S4 = 0.28227
S5 = 0.005978
S6 = 1.80618
S7 = 0.72169
R1 = 0.7643
R2 = 2.2999
R3 = 6.5502
R4 = 2.3670
R5 = -0.01552
R6 = 0.6478
FCW = 2.459
FBH = 3.828
NA = 1e+17#1e+15 #unidades [cm^-3] FALTA COMPROBAR!
ND = 1e+17#2.4771e+15#1e+15 #unidades [cm^-3] FALTA COMPROBAR!
NDOP=1e+17 #unidades [cm^-3]
NC = 3e+19 #unidades [cm^-3]
NV = 1e+19 #unidades [cm^-3]
EG = 1.1242 #Energy Bandgap unidades [eV]
K = 8.617333262145e-5 #cte Boltzmann unidades [eV/K]
C = NA + ND

def klaassen_mode(temperatura, densidad_portadores):
    lista_movilidad_total = []
    #definir NI respecto a la variación de la temperatura
    NI = (math.sqrt(NC*NV)) * ((math.e)**((-EG)/(2*K*temperatura)))
    
    # Se van a definir las variables para tipo n y tipo p
    for i in range(len(densidad_portadores)):
        # Variables p0 y n0
        p0h = ((1/2) * ( NDOP + math.sqrt(NDOP**2 + 4*(NI**2)))) + densidad_portadores[i]
        n0h = (NI**2)/p0h
        n0e = ((1/2) * ( NDOP + math.sqrt(NDOP**2 + 4*(NI**2)))) + densidad_portadores[i]
        p0e = (NI**2)/n0e
        # Variables UiN 
        UiNh = ((UMAXH**2)/(UMAXH- UMINH)) * ((temperatura/300)**(3*ALPHA1H - 1.5))
        UiNe = ((UMAXE**2)/(UMAXE- UMINE)) * ((temperatura/300)**(3*ALPHA1E - 1.5))
        # Variables Uic
        Uich = ((UMINH*UMAXH)/(UMAXH - UMINH)) * ((temperatura/300)**(1/2))
        Uice = ((UMINE*UMAXE)/(UMAXE - UMINE)) * ((temperatura/300)**(1/2))
        # Variablez Z
        Zh = (1) + ((1)/(CIH + ((NREFIH**2)/NA)))
        Ze = (1) + ((1)/(CIE + ((NREFIE**2)/ND)))
        # Variables Nisc
        Nisch = NA + ND + n0h
        Nisce = NA + ND + p0e
        # Variables Pcw
        Pcwh = (3.97e+13) * (((1)/((Zh**3) * Nisch * ((temperatura/300)**3))) ** (2/3))
        Pcwe = (3.97e+13) * (((1)/((Ze**3) * Nisce * ((temperatura/300)**3))) ** (2/3))
        # Variables Pbh
        Pbhh = ((1.36e+20)/(C * MIMOH)) * ((temperatura/300)**2)
        Pbhe = ((1.36e+20)/(C * MIM0E)) * ((temperatura/300)**2)
        # Variables Pih
        Pih = (1)/((FCW/Pcwh) + (FBH/Pbhh))
        Pie = (1)/((FCW/Pcwe) + (FBH/Pbhe))
        # Se define a trozos FPh, se junta en la variable FPh
        FPh_num = (R1)*(Pih**R6) + (R2) + (R3)*(MIMOH/MIM0E)
        FPh_denom = (Pih**R6) + (R4) + (R5)*(MIMOH/MIM0E)
        FPh = FPh_num/FPh_denom
        FPe_num = (R1)*(Pie**R6) + (R2) + (R3)*(MIM0E/MIMOH)
        FPe_denom = (Pie**R6) + (R4) + (R5)*(MIM0E/MIMOH)
        FPe = FPe_num/FPe_denom
        # Se define GPh a trozos, se junta en la variable GPh
        GPh1 = (1)
        GPh2_num = (S1)
        GPh2_denom = ((S2) + ((temperatura)/(300*MIMOH))**(S4) * (Pih))**(S3)
        GPh2 = (GPh2_num)/(GPh2_denom)
        GPh3_num = (S5)
        GPh3_denom = (((MIMOH*300)/(temperatura))**(S7) * (Pih))**(S6)
        GPh3 = (GPh3_num)/(GPh3_denom)
        GPh = (GPh1) - (GPh2) + (GPh3)
        GPe1 = (1)
        GPe2_num = (S1)
        GPe2_denom = ((S2) + ((temperatura)/(300*MIM0E))**(S4) * (Pie))**(S3)
        GPe2 = (GPe2_num)/(GPe2_denom)
        GPe3_num = (S5)
        GPe3_denom = (((MIM0E*300)/(temperatura))**(S7) * (Pie))**(S6)
        GPe3 = (GPe3_num)/(GPe3_denom)
        GPe = (GPe1) - (GPe2) + (GPe3)
        # Variables Nisceff
        Nisceffh = (NA) + (GPh*ND) + (n0h/FPh)
        Nisceffe = (ND) + (GPe*NA) + (p0e/FPe)
        # Variables UiL
        UiLh = UMAXH
        UiLe = UMAXE
        # Variables UiN
        # UiNh = (UMAXH**2)/(UMAXH-UMINH)
        # UiN3 = (UMAXE**2)/(UMAXE-UMINE)
        # Se define UiD+A+j,h a trozos, la variable final pasará a llamarse UiDAjh
        UiDAjh1 = (UiNh*Nisch)/(Nisceffh)
        UiDajh2 = (NREF1H/Nisch)**(ALPHA1H)
        UiDajh3 = (Uich*(n0h+p0h))/(Nisceffh)
        UiDajh = UiDAjh1*UiDajh2+UiDajh3
        UiDAje1 = (UiNe*Nisce)/(Nisceffe)
        UiDaje2 = (NREF1E/Nisce)**(ALPHA1E)
        UiDaje3 = (Uice*(n0e+p0e))/(Nisceffe)
        UiDaje = UiDAje1*UiDaje2+UiDaje3
        # Se define uKL a trozos, la variable final pasará a llamarse uKL
        uKLh_nom = 1
        uKLh_denom = (1/UiLh) + (1/UiDajh)
        uKLh = uKLh_nom/uKLh_denom
        uKLe_nom = 1
        uKLe_denom = (1/UiLe) + (1/UiDaje)
        uKLe = uKLe_nom/uKLe_denom
        # Añadir los valores finales en una lista de movilidades
        lista_movilidad_total.append(uKLh+uKLe)
    return lista_movilidad_total

        



