# Se declaran las variables que hay que solicitar al usuario.

def solicitar_valor(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print(f"Por favor, introduce un valor numérico válido para {mensaje}.")

print("Valores Tipicos: W[cm]= 0.0300  OPTICAL_FACTOR: 0.70 NDOP[cm^-3]: 1e+16 ") 
W = solicitar_valor("Introduce el valor de W en [cm]: ")
OPTICAL_FACTOR = solicitar_valor("Introduce el valor de OPTICAL_FACTOR: ")
NDOP = solicitar_valor("Introduce el Valor de NDOP en [cm^-3]: ")



#Código Shangde

"""
W = float(input("Introduce el valor de W en [cm]: "))
OPTICAL_FACTOR = float(input("Introduce el valor de OPTICAL_FACTOR: "))
NDOP = float(input("Introduce el Valor de NDOP en [cm^-3]: "))
"""