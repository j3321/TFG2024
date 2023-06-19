# Archivo que muestra la gráfica inicial de los datos del archivo arrastrado para poder ser analizado
# y tratados posteriormente
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class ReferenceGraphic:
    def __init__(self):
        pass
    def pintar(self, path): #self, path
        # Tomamos las 3 columnas iniciales
        num_cols = 3
        # Condicional que depende de la extensión del archivo 
        if path.endswith('.xlsx'):
            # Se lee el archivo excel y se toma las columnas necesarias
            datos = pd.read_excel(path, usecols=range(num_cols))
            # Se toma los valores posteiores al máximo encontrado en Photovoltage
            # max_index = datos.iloc[:, 1].idxmax()
            # lista_nueva = datos.loc[max_index:]
        else:
            # Delimeters más comunes (, ; \t | :)
            datos = pd.read_csv(path,header = 0, delimiter='\t', usecols=range(num_cols)) 
            columnas_numericas = [0, 1, 2]
            # Se toman los valores de la segunda columna
            datos.iloc[:, columnas_numericas] = datos.iloc[:, columnas_numericas].apply(lambda x: x.str.replace(',', '.').astype(float)) 
            # max_index = np.argmax(datos.iloc[:,1])
            # lista_nueva = datos.loc[max_index:]
            
        # Extraer columnas de datos
        datos = datos.loc[datos.iloc[:,1] >=0]
        time = datos.iloc[:, 0]
        photovoltage = datos.iloc[:, 1]
        reference_voltage = datos.iloc[:, 2]
        reference_voltage = np.where(reference_voltage < 0, 0, reference_voltage)

        # Crear una figura y un eje en la figura
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot()

        # Trazar los datos en el gráfico
        ax.plot(time, photovoltage, label='Photovoltage', color ='blue')
        ax.plot(time, reference_voltage, label='Reference Voltage', color ='red')
        ax.grid()
        #set xlabel
        ax.set_xlabel('Time (s)')
        timeMax = datos.iloc[:, 0].max()
        timeMin = datos.iloc[:, 0].min()
        ax.set_xlim(timeMin,timeMax)
        #set ylabel
        ax.set_ylabel('Voltage (v)')
        Photovoltage_columna = datos.iloc[:, 1]
        ReferenceVoltage_columna = datos.iloc[:, 2]
        ylimMax = max(Photovoltage_columna.max(), ReferenceVoltage_columna.max())
        ylimMin = min(Photovoltage_columna.min(), ReferenceVoltage_columna.min())
        ax.set_ylim(ylimMin,ylimMax)
        ax.set_title('Reference Graphic')
        ax.legend()

        # Mostrar el gráfico y el flujo de eventos sigue sin esperar que se cierre la ventana
        plt.show(block = False) # False

