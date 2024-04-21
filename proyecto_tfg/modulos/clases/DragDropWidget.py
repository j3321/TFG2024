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
        # Leer el archivo y mostrar los datos en la consola
        for url in event.mimeData().urls():
            self.path = url.toLocalFile()  # Almacenar la ruta del archivo en la variable de instancia
            if self.path.endswith('.csv') or self.path.endswith('.txt'):
                self.Measurebutton.setEnabled(True)
                grafica_referencia=ReferenceGraphic() 
                grafica_referencia.pintar(self.path) # Pasar la ruta del archivo a la función pintar
                self.label.setText(f'Se importó el archivo "{self.path}"')
            elif self.path.endswith('.xlsx'):
                self.Measurebutton.setEnabled(True)
                grafica_referencia=ReferenceGraphic() 
                grafica_referencia.pintar(self.path) # Pasar la ruta del archivo a la función pintar
                self.label.setText(f'Se importó el archivo "{self.path}"')
            else:
                print("Error: el archivo debe ser un archivo CSV o Excel.")
                QMessageBox.about(self, "Error", "El archivo debe ser un archivo CSV o Excel.")
                self.label.setText('Arrastre un archivo aquí')

    def showDialog(self):
        objeto_pintar = LifetimeGraphic(self.path)
        while True:
            # Muestra un cuadro para que el usuario escoja entre las opciones
            options = ["Escoge una opción:","Sinton", "Dorkel", "Klaassen","Schindler" ,"Todas las movilidades" ,"Sinton-Intrinseco", "Dorkel-Intrinseco", "Klaassen-Intrinseco", "Schindler-Intrinseco","Sinton-SRH","SRH-X"]
            choice, _ = QInputDialog.getItem(self, 'Selección de opción', 'Seleccione una opción:', options )
            self.choice = choice
            funciones_modo = {
            "Sinton": objeto_pintar.pintar_tiempo_recombinacion,
            "Dorkel": objeto_pintar.pintar_tiempo_recombinacion_temperatura,
            "Klaassen": objeto_pintar.pintar_tiempo_recombinacion_temperatura,
            "Schindler": objeto_pintar.pintar_tiempo_recombinacion_temperatura,
            "Todas las movilidades": objeto_pintar.pintar_todas_movilidades,
            "Sinton-Intrinseco": objeto_pintar.pintar_tiempo_intrinseco,
            "Dorkel-Intrinseco": objeto_pintar.pintar_tiempo_intrinseco,
            "Klaassen-Intrinseco": objeto_pintar.pintar_tiempo_intrinseco,
            "Schindler-Intrinseco": objeto_pintar.pintar_tiempo_intrinseco,
            "Sinton-SRH": objeto_pintar.pintar_tiempo_SRH,
            "SRH-X": objeto_pintar.pintar_SRH_X
            }
            if choice in funciones_modo:
                if choice == "Sinton":
                    funciones_modo[choice](self.choice, None)
                elif choice == "Sinton-SRH":
                    # Obtener el valor de la temperatura
                    val_temp, ok_temp = QInputDialog.getDouble(self, "Temperatura", "Ingrese el valor de la temperatura en Celsius:")
                    if ok_temp:
                        # Obtener el valor de Joe
                        val_J0e, ok_J0e = QInputDialog.getDouble(self, "J0e", "Ingrese el valor de J0e:")
                        if ok_J0e:
                            funciones_modo[choice](self.choice, val_temp, val_J0e)  # Llamar a la función con los valores de temperatura y Joe
                        break
                else:
                    val, ok = QInputDialog.getDouble(self, "Temperatura", "Ingrese el valor de la temperatura en Celsius:")
                    if ok:
                        funciones_modo[choice](self.choice, val)
                break
            else:
                QMessageBox.about(self, "Error", "Debe escoger una opción válida.")
                break