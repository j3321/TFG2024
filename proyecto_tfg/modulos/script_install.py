#Este script tiene como función el instalar en el ordenador las librerías 
#necesarias para que se pueda ejecutar el programa, todas ellas se encuentran
#en el archivo requeriments.tx
import subprocess
import sys

def install_requirements():
    try:
        # Llama a pip para instalar las dependencias desde requirements.txt
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Todas las dependencias se han instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error durante la instalación de dependencias: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()