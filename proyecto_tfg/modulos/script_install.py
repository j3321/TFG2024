#Este script tiene como función el instalar en el ordenador las librerías 
#necesarias para que se pueda ejecutar el programa
import subprocess

# Comando de instalación
comandos = [
    "pip3 install pyqt5",
    "pip3 install pandas",
    "pip3 install numpy",
    "pip3 install simpy",
    "pip3 install matplotlib",
    "pip install scipy",
    "pip install statsmodels"
]

# Ejecutar comandos uno por uno en el terminar para instalar las librerías
for comando in comandos:
    try:
        subprocess.check_call(comando, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Se ha producido un error: {comando}")
