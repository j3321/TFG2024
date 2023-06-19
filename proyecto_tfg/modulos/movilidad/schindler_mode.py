# Se define la movilidad Schindler tomando como parámetros la temperatura y 
# una lista de densidad de portadores
#Results is in cm2/Vs
import math
from .. import input_values


###########################
# VALORES PARA ELECTRONES #
###########################
UMAXE = 1414
UMINE = 68.5
U1E = 56.1
NREF1E = 9.20e+16
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
U1H = 29.0
NREF1H = 2.23e+17
NREF2H = 6.1e+20
ALPHA1H = 0.719
ALPHA2H = 2.0
CIH = 0.5
NREFIH = 7.2e+20
MIM0H = 1.258

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
NREF3 = 1.276e+17
BETA1 = 24.82
CLREF = 1.092
NDOP=input_values.NDOP
NC = 3e+19 #unidades [cm^-3]
NV = 1e+19 #unidades [cm^-3]
EG = 1.1242 #Energy Bandgap unidades [eV]
K = 8.617333262145e-5 #cte Boltzmann unidades [eV/K]
C = NDOP + NDOP
CI = (NDOP + NDOP)/(C)
CIRT = (NDOP + NDOP)/(C)


def schindler_mode(temperatura, densidad_portadores):
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
        UiNh1 = (UMAXH**2)/(UMAXH-UMINH) 
        UiNh2 = (temperatura/300)**(3*ALPHA1H-1.5)
        UiNh = UiNh1 * UiNh2
        UiNe1 = (UMAXE**2)/(UMAXE-UMINE) 
        UiNe2 = (temperatura/300)**(3*ALPHA1E-1.5)
        UiNe = UiNe1 * UiNe2
        # Variables Uic
        Uich1 = (UMINH*UMAXH)/(UMAXH-UMINH)
        Uich2 = (temperatura/300)**(1/2)
        Uich = Uich1*Uich2
        Uice1 = (UMINE*UMAXE)/(UMAXE-UMINE)
        Uice2 = (temperatura/300)**(1/2)
        Uice = Uice1*Uice2
        # Variable Z
        Zh1 = (1)
        Zh2 = (1)/(CIH + (NREFIH**2)/(NDOP))
        Zh = Zh1 + Zh2
        Ze1 = (1)
        Ze2 = (1)/(CIE + (NREFIE**2)/(NDOP))
        Ze = Ze1 + Ze2
        # Variable Nisc
        Nisch = NDOP + NDOP + n0h
        Nisce = NDOP + NDOP + p0e
        # Variable Pcw
        Pcwh1 = 3.97e+13
        Pcwh2 = ((1)/((Zh**3) * Nisch * (temperatura/300)**3))**(2/3)
        Pcwh = Pcwh1 * Pcwh2
        Pcwe1 = 3.97e+13
        Pcwe2 = ((1)/((Ze**3) * Nisce * (temperatura/300)**3))**(2/3)
        Pcwe = Pcwe1 * Pcwe2 
        # Variable Pbh
        Pbhh1 = (1.36e+20)/(C*MIM0H)
        Pbhh2 = (temperatura/300)**2
        Pbhh = Pbhh1*Pbhh2
        Pbhe1 = (1.36e+20)/(C*MIM0E)
        Pbhe2 = (temperatura/300)**2
        Pbhe = Pbhe1*Pbhe2
        # Variable Pi
        Pih1 = (1)
        Pih2 = (FCW/Pcwh)+(FBH/Pbhh)
        Pih = Pih1/Pih2
        Pie1 = (1)
        Pie2 = (FCW/Pcwe)+(FBH/Pbhe)
        Pie = Pie1/Pie2
        # Variable FP
        FPh1 = (R1) * (Pih)**(R6) + (R2) +(R3)*(MIM0H/MIM0E)
        FPh2 = (Pih)**(R6) + (R4) + R5*(MIM0H/MIM0E)
        FPh = FPh1/FPh2
        FPe1 = (R1) * (Pie)**(R6) + (R2) +(R3)*(MIM0E/MIM0H)
        FPe2 = (Pie)**(R6) + (R4) + R5*(MIM0E/MIM0H)
        FPe = FPe1/FPe2
        # Variable GP
        GPh1 = (1)
        GPh2_num = (S1)
        GPh2_denom = ((S2) + ((temperatura)/(300*MIM0H))**(S4) * (Pih))**(S3)
        GPh2 = (GPh2_num)/(GPh2_denom)
        GPh3_num = (S5)
        GPh3_denom = (((MIM0H*300)/(temperatura))**(S7) * (Pih))**(S6)
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
        # Variable Nisceff 
        Nisceffh = NDOP + GPh*NDOP + (n0h/FPh)
        Nisceffe = NDOP + GPe*NDOP + (p0e/FPe)
        # Variables UiL
        UiLh = UMAXH
        UiLe = UMAXE
        # Variables UiN
        # UiNh = (UMAXH**2)/(UMAXH-UMINH)
        # UiNe = (UMAXE**2)/(UMAXE-UMINE)
        # Variables UiDAj
        UiDAjh1 = (Uich)
        UiDAjh2 = (n0h+p0h)/Nisceffh
        UiDAjh3 = (UiNh*Nisch)/Nisceffh
        UiDAjh4 = (NREF1H/Nisch)**(ALPHA1H)
        UiDAjh5 = (NDOP + NDOP)/NREF3
        UiDAjh6 = ((CIRT-1)/CLREF)**(BETA1)
        UiDAjh = UiDAjh1 * UiDAjh2 + UiDAjh3 * ((UiDAjh4 + UiDAjh5*UiDAjh6)**(-1))
        UiDAje1 = (Uice)
        UiDAje2 = (n0e+p0e)/Nisceffe
        UiDAje3 = (UiNe*Nisce)/Nisceffe
        UiDAje4 = (NREF1E/Nisce)**(ALPHA1E)
        UiDAje5 = (NDOP + NDOP)/NREF3
        UiDAje6 = ((CIRT-1)/CLREF)**(BETA1)
        UiDAje = UiDAje1 * UiDAje2 + UiDAje3 * ((UiDAje4 + UiDAje5*UiDAje6)**(-1))
        #Variables Usch
        Uschh1 = (1)
        Uschh2 = (1/UiLh) + (1/UiDAjh)
        Uschh = Uschh1/Uschh2
        Usche1 = (1)
        Usche2 = (1/UiLe) + (1/UiDAje)
        Usche = Usche1/Usche2
        lista_movilidad_total.append(Uschh+Usche)
    return lista_movilidad_total






