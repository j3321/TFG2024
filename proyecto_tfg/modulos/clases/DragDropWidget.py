# Interfaz de usuario que desplega una ventana y permite al usuario arrastrar un archivo para
# ser posteriormente tratado y analizado

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt
from .ReferenceGraphic import ReferenceGraphic
from .LifetimeGraphic import LifetimeGraphic

class DragDropWidget(QWidget):
    def __init__(self, ):
        super().__init__()
        self.initUI()
        self.path = None  # Agregar una variable de instancia para almacenar la ruta del archivo
        self.choice = None

    def initUI(self):
        self.setWindowTitle('Importa el archivo que quieres analizar')
        self.setGeometry(300, 300, 450, 550)

        # Crear una etiqueta para mostrar el archivo arrastrado
        self.label = QLabel('Arrastre un archivo aquí', self)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        # Crear un botón para imprimir
        self.Measurebutton = QPushButton("Analizar tiempo de vida usando:", self)
        self.Measurebutton.clicked.connect(self.showDialog)  # Conectar a la función que muestra el cuadro de diálogo
        self.Measurebutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Measurebutton.setFixedHeight(70)
        self.Measurebutton.setEnabled(False)  # Ocultar el botón inicialmente


        # Crear un diseño vertical para la ventana
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.Measurebutton)  # Agregar el botón al diseño
        self.setLayout(vbox)

        # Permitir que la ventana acepte archivos que se arrastran
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Verificar si el evento contiene datos de archivo
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        global temp
        # Leer el archivo y mostrar los datos en la consola
        for url in event.mimeData().urls():
            self.path = url.toLocalFile()  # Almacenar la ruta del archivo en la variable de instancia
            if self.path.endswith('.csv') or self.path.endswith('.txt') or self.path.endswith('.xlsx'):
                self.Measurebutton.setEnabled(True)
                grafica_referencia = ReferenceGraphic()
                grafica_referencia.pintar(self.path)  # Pasar la ruta del archivo a la función pintar

                objeto_pintar = LifetimeGraphic(self.path)
                val, ok = QInputDialog.getDouble(self, "Temperatura", "Ingrese el valor de la temperatura en Celsius:")
                if ok:
                    objeto_pintar.pintar_todas_movilidades("Todas las movilidades", val)  # Pintar todas las movilidades 
                    temp = val

                self.label.setText(f'Se importó el archivo "{self.path}"')
            else:
                print("Error: el archivo debe ser un archivo CSV o Excel.")
                QMessageBox.about(self, "Error", "El archivo debe ser un archivo CSV o Excel.")
                self.label.setText('Arrastre un archivo aquí')

    def showDialog(self):
        objeto_pintar = LifetimeGraphic(self.path)
        while True:
            # Muestra un cuadro para que el usuario escoja entre las opciones
            options = ["Escoge una opción:","Sinton", "Dorkel", "Klaassen","Schindler" ,"Sinton-Intrinseco", "Dorkel-Intrinseco", "Klaassen-Intrinseco", "Schindler-Intrinseco"]
            choice, _ = QInputDialog.getItem(self, 'Selección de opción', 'Seleccione una opción:', options )
            self.choice = choice
            funciones_modo = {
            "Sinton": objeto_pintar.pintar_tiempo_recombinacion,
            "Dorkel": objeto_pintar.pintar_tiempo_recombinacion_temperatura,
            "Klaassen": objeto_pintar.pintar_tiempo_recombinacion_temperatura,
            "Schindler": objeto_pintar.pintar_tiempo_recombinacion_temperatura,
            "Sinton-Intrinseco": objeto_pintar.pintar_tiempo_intrinseco,
            "Dorkel-Intrinseco": objeto_pintar.pintar_tiempo_intrinseco,
            "Klaassen-Intrinseco": objeto_pintar.pintar_tiempo_intrinseco,
            "Schindler-Intrinseco": objeto_pintar.pintar_tiempo_intrinseco
            }
            if choice in funciones_modo:
                if choice == "Sinton":
                    funciones_modo[choice](self.choice, None)
                else:
                    funciones_modo[choice](self.choice, temp)
                break
            else:
                QMessageBox.about(self, "Error", "Debe escoger una opción válida.")
                break