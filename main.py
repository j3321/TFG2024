#Se ejecuta el programa donde se integra todos los módulos.
import sys
from PyQt5.QtWidgets import QApplication
from proyecto_tfg.modulos.clases.DragDropWidget import DragDropWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragDropWidget()
    window.show()
    sys.exit(app.exec_())

    #Version Nuevo repositorio 13/05