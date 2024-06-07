# Script donde se toma los valores del archivo excel, se tratan llamando a functions_timelife y se pinta 
# la curva de vida
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from matplotlib.widgets import Slider
from matplotlib.widgets import RangeSlider
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from PyQt5.QtWidgets import QMessageBox
from .. import functions_timelife
from .. import functions_curvefit
from .. import excel_formatter
import os

import plotly.graph_objects as go

# Configuración global de Matplotlib
plt.rcParams.update({
    'axes.titlesize': 20,       # Tamaño del título de los ejes
    'axes.labelsize': 16,       # Tamaño de las etiquetas de los ejes
    'xtick.labelsize': 14,      # Tamaño de las etiquetas de los ticks del eje X
    'ytick.labelsize': 14,      # Tamaño de las etiquetas de los ticks del eje Y
    'legend.fontsize': 14,      # Tamaño de la fuente de la leyenda
    'font.size': 14             # Tamaño de la fuente general
})
tau = '\u03C4'

class LifetimeGraphic:
    def __init__(self, path):
        self.path = path
        #definimos las columnas iniciales
        num_cols = 3
        if path.endswith('.xlsx'):
            # Se lee el archivo excel y se toma las columnas necesarias
            self.datos = pd.read_excel(path, usecols=range(num_cols))
            # Tomamos 2 valores posteriores al máximo de la columna de Photovoltage
            self.datos = self.datos.loc[self.datos.iloc[:,1] >=0]
            max_index = self.datos.iloc[:, 1].idxmax() +2
            self.lista_nueva = self.datos.loc[max_index:]
        else:
            self.datos = pd.read_csv(path, header = 0, delimiter='\t', usecols=range(num_cols)) 
            # Se toman los valores de la segunda columna
            columnas_numericas = [0, 1, 2]
            # Se toman los valores de la segunda columna
            self.datos.iloc[:, columnas_numericas] = self.datos.iloc[:, columnas_numericas].apply(lambda x: x.str.replace(',', '.').astype(float))
            self.datos = self.datos.loc[self.datos.iloc[:,1] >=0] 
            max_index = np.argmax(self.datos.iloc[:,1])
            self.lista_nueva = self.datos.loc[max_index:]
            

    # Se calcula y se devuelve la lista de tasa de generación.
    def generacionList(self): 
        Vref = self.lista_nueva.iloc[:, 2].values.tolist()
        Vref = np.where(np.array(Vref) < 0, 0, Vref)
        lista_generacion = []
        for vref in Vref:
            indice_generacion= functions_timelife.generacion(vref)
            lista_generacion.append(indice_generacion)
        return lista_generacion
    
    # Se calcula y se devuelve la lista de valores de fotoconductividad.
    def fotoconductividadList(self):
        Vph = self.lista_nueva.iloc[:, 1].values.tolist()
        lista_fotoconductividad = []
        for vph in Vph:
            indice_fotoconductividad = functions_timelife.fotoconductividad(vph)
            lista_fotoconductividad.append(indice_fotoconductividad)
        return lista_fotoconductividad
    
    # Se toma como parámetros la elección del usuario y la temperatura para tomar los valores de la
    # densidad de portadores
    def densidad_portadoresList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores    
    def densidad_portadoresSintonList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores_sinton(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores
    def densidad_portadoresDorkelList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores_dorkel(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores
    def densidad_portadoresKlaassenList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores_klaassen(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores
    def densidad_portadoresSchindlerList(self, choice, temperatura):
        lista_fotoconductividad = self.fotoconductividadList()
        lista_densidadPortadores = functions_timelife.densidad_portadores_schindler(lista_fotoconductividad, 1700, choice, temperatura)
        return lista_densidadPortadores

    # Se toma como parámetros la elección del usuario y la temperatura para tomar los valores del
    # tiempo de recombinación
    def tiempo_recombinacionList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
    def tiempo_recombinacionSintonList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresSintonList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
    def tiempo_recombinacionDorkelList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresDorkelList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
    def tiempo_recombinacionKlaassenList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresKlaassenList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
    def tiempo_recombinacionSchindlerList(self, choice, temperatura):
        lista_tiempo = self.lista_nueva.iloc[:, 0].values.tolist()
        lista_densidadPortadores = self.densidad_portadoresSchindlerList(choice, temperatura)
        lista_generacion = self.generacionList()
        lista_tiempo_recombinacion = functions_timelife.tiempo_recombinacion(lista_densidadPortadores, lista_generacion, lista_tiempo)
        return lista_tiempo_recombinacion
        
    def tiempo_intrinsecoList(self, choice, temperatura):
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_densidadPortadores_filtrada = [num for num in lista_densidadPortadores if num >=0]
        lista_tiempo_intrinseco = functions_timelife.tiempo_intrinseco(lista_densidadPortadores_filtrada, temperatura)
        return lista_tiempo_intrinseco
    
    def tiempo_srhList(self, choice, temperatura):
        lista_tiempo_recombinacion = self.tiempo_recombinacionList(choice, temperatura)
        lista_tiempo_intrinseco = self.tiempo_intrinsecoList(choice, temperatura)
        lista_tiemposrh = functions_timelife.tiempo_srh(lista_tiempo_intrinseco,lista_tiempo_recombinacion)
        return lista_tiemposrh
    
    def x_List(self, choice, temperatura):
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_densidadPortadores_filtrada = [num for num in lista_densidadPortadores if num >=0]
        lista_X = functions_timelife.calculo_X(lista_densidadPortadores_filtrada, temperatura)
        return lista_X

    # Se muestra en una gráfica el tiempo de recombinación respecto a la densidad de portadores
    # en cada instante de tiempo
    def pintar_tiempo_recombinacion(self, choice, temperatura):
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_tiempo_recombinacion = self.tiempo_recombinacionList(choice, temperatura)
        lista_tiempo_recombinacion_micros = [t * 1e+6 for t in lista_tiempo_recombinacion]  # Conversión a microsegundos
        # Se crea la figura y los ejes con un tamaño determinado    
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot()
        # Configurar los límites del deslizador
        slider_ax = plt.axes([0.15, 0.0001, 0.7, 0.03])  # Modificar las coordenadas y del deslizador
        slider = Slider(slider_ax, 'Rango de valores', 1, len(lista_densidadPortadores), valinit=len(lista_densidadPortadores), valstep=1, color ="green")
        # Se define n como global para acceder al numero de elementos en las funciones posteriores
        global n
        def update_graph(val,slider):
            global n
            # Obtener el valor actual del deslizador
            n = int(val)
            # Obtener los subconjuntos de datos a mostrar
            lista_densidadPortadores_variable = lista_densidadPortadores[:n]
            lista_tiempo_recombinacion_micros_variable = lista_tiempo_recombinacion_micros[:n]
            data = pd.DataFrame({"Carrier Density (cm^-3)": lista_densidadPortadores_variable, "Lifetime (us)": lista_tiempo_recombinacion_micros_variable})
            # Guardar los datos en un archivo Excel
            data.to_excel("Lifetime_Sinton_Mode.xlsx", index=False)
            # Limpiar la figura y graficar los datos actualizados
            ax.clear()
            ax.semilogx(lista_densidadPortadores_variable, lista_tiempo_recombinacion_micros_variable, marker ='o', markersize=3, label="Lifetime", color ='green')
            ax.set_title(f"Lifetime vs. Carrier Density -{choice} Mode")
            ax.set_xlabel("Carrier Density (cm^-3)")
            ax.set_ylabel("Lifetime (us)")
            ax.set_ylim(0, None)
            ax.yaxis.set_major_formatter('{:.1f}'.format)
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            fig.canvas.draw_idle()
            plt.pause(0.0001)
        # Conectar el slider a la función de actualización del gráfico
        slider.on_changed(lambda val: update_graph(val,slider))
        # Graficar los datos iniciales
        update_graph(len(lista_densidadPortadores),slider)
        # Se muestra la gráfica
        plt.ion()
        plt.show(block=False)

    # Se muestra en una gráfica el tiempo de recombinación respecto a la densidad de portadores
    # en cada instante de tiempo. Se toma en cuenta la temperatura seleccionada
    def pintar_tiempo_recombinacion_temperatura(self,choice,temperatura):
        # Para graficar correctamente
        global n
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot()
        ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
        temperatura_kelvin  = temperatura + 273.15
        # se define una temperatura mínima de 300K y se pintan con un intervalo de 50K
        # las gráficas sucesivas
        while temperatura_kelvin >= 300:
                lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura_kelvin)
                lista_tiempo_recombinacion = self.tiempo_recombinacionList(choice, temperatura_kelvin)
                lista_tiempo_recombinacion_micros = [t * 1e+6 for t in lista_tiempo_recombinacion]  # Conversión a microsegundos
                data = pd.DataFrame({"Carrier Density (cm^-3)": lista_densidadPortadores[:n], "Lifetime (us)": lista_tiempo_recombinacion_micros[:n]})
                # Guardar los datos en un archivo Excel
                data.to_excel(f"Lifetime_{choice}_Mode_{temperatura_kelvin}K.xlsx", index=False)
                ax.semilogx(lista_densidadPortadores[:n], lista_tiempo_recombinacion_micros[:n], marker ='o', markersize=3, label="Lifetime")
                ax.text(lista_densidadPortadores[0], lista_tiempo_recombinacion_micros[0], f"{temperatura_kelvin} K", fontsize=8)
                ax.set_title(f"Lifetime vs. Carrier Density -{choice} Mode") 
                ax.set_xlabel("Carrier Density (cm^-3)")
                ax.set_ylabel("Lifetime (us)")
                ax.set_ylim(0, None)
                ax.yaxis.set_major_formatter('{:.1f}'.format)
                temperatura_kelvin-=50
        plt.show(block=False)


    ######################################################################################
    ######################################################################################

    global J0E_suavizado_2_mean
    J0E_suavizado_2_mean = None  # Inicializamos la variable global

    def pintar_tiempo_intrinseco(self, choice, temperatura):
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_densidadPortadores_filtrada = [num for num in lista_densidadPortadores if num >=0]
        lista_tiempo_srh = self.tiempo_srhList(choice, temperatura)

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot()
        plt.subplots_adjust(right=0.83, bottom=0.15)
        
        button_connected = False  # Bandera para controlar la conexión del botón

        def update_graph(val):
            # Obtener los valores de los límites superior e inferior del slider
            lower_limit, upper_limit = slider.val

            global n
            global s
            global suav
            global J0E_suavizado_2_mean
            nonlocal button_connected

            #Obtener estado suavizado
            suav = check.get_status()[0]
            # Obtener el valor actual del deslizador
            s = lower_limit
            n = upper_limit
            # Obtener los subconjuntos de datos a mostrar
            lista_densidadPortadores_filtrada_variable = lista_densidadPortadores_filtrada[s:n]
            lista_tiempo_srh_filtrada_variable = lista_tiempo_srh[s:n]
            #Suavizamos la curva de tiempo intrinseco
            lista_tiempo_srh_suave, lista_densidadPortadores_filtrada_suave = functions_curvefit.suavizado_curva(lista_tiempo_srh_filtrada_variable, lista_densidadPortadores_filtrada_variable)
            
            # Mediante ajuste de curvas calculamos los J0e
            global J0e_fin            
            SRH, J0E, lista_srh_ajustada = functions_curvefit.custom_gradient(lista_densidadPortadores_filtrada_variable,lista_tiempo_srh_filtrada_variable)
            #Calculamos J0e con los datos suavizados
            SRH, J0E_s, lista_srh_ajustada = functions_curvefit.custom_gradient(lista_densidadPortadores_filtrada_suave,lista_tiempo_srh_suave)
            SRH_2, J0E_2, valores_ajustados_2 = functions_curvefit.custom_linear_fit(lista_densidadPortadores_filtrada_variable,lista_tiempo_srh_filtrada_variable)

            #Almacenar los datos en un dataframe           
            data = pd.DataFrame({
                "Carrier Density (cm^-3)": lista_densidadPortadores_filtrada_variable,
                f"1/{tau} eff - 1/{tau} intrinseco": lista_tiempo_srh_filtrada_variable,
                "J0E": J0E,
                "J0e medio": np.mean(J0E),
                "J0E_suave": J0E_s,
                "J0e medio suave": np.mean(J0E_s)
            })
            #Pasamos los datos a un excel con una anchura de columnas dada
            excel_formatter.format_and_save_to_excel(data, "Lifetime.xlsx", "Lifetime Intrinseco", "TableStyleMedium2", column_widths=[25, 33, 15, 25, 25, 30])

            #Limpiar la figura y graficar los datos actualizados
            ax.clear()
            #Muestra valores 1/tiempo eff - 1/tiempo intrinseco frente a la densidad de portadores
            if(not suav):   #Si la opcion de suavizado no esta seleccionada se muestran los valores normales
                ax.plot(lista_densidadPortadores_filtrada_variable,lista_tiempo_srh_filtrada_variable, marker ="o", markersize = 6, color ="blue", linewidth=2, label="Original")
                J0e_fin = J0E
            else:       #Si la opcion de suavizado si esta seleccionada se muestran los valores suavizados
                #Muestra los valores NO suavizados
                ax.plot(lista_densidadPortadores_filtrada_variable,lista_tiempo_srh_filtrada_variable, marker ="o", markersize = 6, color ="blue", linewidth=2, label="Original")
                #Muestra los valores suavizados
                ax.plot(lista_densidadPortadores_filtrada_suave,lista_tiempo_srh_suave, marker ="8", markersize = 6, color ="green", linewidth=2, label="Suavizado")
                ax.plot(lista_densidadPortadores_filtrada_variable, valores_ajustados_2, color='red', linewidth=1.5, label='Regresión Lineal')
                #Para usar con el boton se eligen los datos suavizados
                J0e_fin = J0E_s

            J0E_suavizado, lista_densidarPortadores_filtrada_suave = functions_curvefit.suavizado_curva(J0e_fin, lista_densidadPortadores_filtrada_variable)
            J0E_suavizado_2, lista_densidarPortadores_filtrada_suave = functions_curvefit.suavizado_curva(J0E_suavizado, lista_densidadPortadores_filtrada_variable)

            # Guardar el valor de J0E_suavizado_2
            J0E_suavizado_2_mean = np.mean(J0E_suavizado_2)


            #Se muestra el valor de J0e a la derecha de la gráfica
            value_ax = fig.add_axes([0.85, 0.6, 0.12, 0.05])
            value_ax.set_xticks([])  # Ocultar ticks del eje X
            value_ax.set_yticks([])  # Ocultar ticks del eje Y
            value_ax.text(0.5, 0.5, f'J0e: { J0E_suavizado_2_mean:.4e}', horizontalalignment='center', verticalalignment='center', transform=value_ax.transAxes)

            # Solo conectar el botón una vez
            if not button_connected:
                button.on_clicked(clickado)
                button_connected = True

            ax.set_title(f"Lifetime & -{choice} Mode")
            ax.set_xlabel("Carrier Density (cm^-3)")
            ax.set_ylabel(f"1/{tau} eff - 1/{tau} intrinseco")
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            ax.legend()
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            fig.canvas.draw_idle()
            plt.pause(0.1)

        def clickado(event):
                if J0E_suavizado_2_mean is not None and J0E_suavizado_2_mean > 0:
                    self.pintar_tiempo_SRH(choice,temperatura,J0E_suavizado_2_mean )
                else:
                    QMessageBox.critical(None, 'Error', 'J0e no puede ser negativo, revisa si estas en alta inyección"')


        #Se crea un botón para obtener el tiempo SRH
        button_ax = plt.axes([0.85, 0.4, 0.12, 0.05])  # Ajusta las dimensiones según tus necesidades
        button = Button(button_ax, 'SRH Lifetime', color='lightblue', hovercolor='0.975')
        #button.label.set_fontsize(14)
        #button.on_clicked(clickado)
        

        # Posición del checkbox
        check_ax = fig.add_axes([0.85, 0.8, 0.12, 0.05])  # [left, bottom, width, height]
        check = CheckButtons(check_ax, ['Suavizar Datos'], [False])
            # Ajustar el tamaño de la fuente del checkbox
        #for label in check.labels:
            #label.set_fontsize(14)
        #Cuando se pulsa el boton se actualiza la grafica a suavizada
        check.on_clicked(update_graph)


        # Definir el rango de valores del slider
        val_min = 1
        val_max = len(lista_densidadPortadores)
        # Crear el slider con los límites inicial y final
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        slider = RangeSlider(slider_ax, '', val_min, val_max, valstep=1 , valinit=(val_min, val_max))
        # Rotar visualmente el slider
        slider_ax.invert_xaxis()
        # Ocultar el eje y por completo
        slider_ax.axis('off')
        # Conectar el slider a la función de actualización del gráfico
        slider.on_changed(update_graph)

        # Graficar los datos iniciales
        update_graph((1,len(lista_densidadPortadores)))

        # Se muestra la gráfica
        plt.ion()
        plt.show(block=False)

    ######################################################################################
    ######################################################################################
    
    def pintar_tiempo_SRH(self, choice, temperatura, j0e):
        lista_densidadPortadores = self.densidad_portadoresList(choice, temperatura)
        lista_densidadPortadores_filtrada = [num for num in lista_densidadPortadores if num >=0]
        lista_tiempo_recombinacion = self.tiempo_recombinacionList(choice, temperatura)
        lista_tiempo_intrinseco = self.tiempo_intrinsecoList(choice,temperatura)
        lista_tiempo_srh = self.tiempo_srhList(choice, temperatura)
        #lista_tiempo_srh_micros = [t * 1e+6 for t in lista_tiempo_srh] 

        #Sacamos una lista con los valores de X
        lista_X = self.x_List(choice,temperatura)


        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot()
        plt.subplots_adjust(right=0.83, bottom=0.15)
        
        button_connected = False  # Bandera para controlar la conexión del botón

    
        def update_graph(val):
            # Obtener los valores de los límites superior e inferior del slider
            lower_limit, upper_limit = slider.val

            global n
            global s
            global suav
            nonlocal button_connected

            #Se crea la lista de srh y de X para luego usarla en SRH/X
            global lista_srh_fin
            global lista_X_variable
            #Obtener estado suavizado
            suav = check.get_status()[0]
            # Obtener el valor actual del deslizador
            s = lower_limit
            n = upper_limit
            # Obtener los subconjuntos de datos a mostrar
            lista_densidadPortadores_filtrada_variable = lista_densidadPortadores_filtrada[s:n]
            lista_tiempo_intrinseco_micros_variable = lista_tiempo_intrinseco[s:n]
            lista_tiempo_srh_micros_variable = lista_tiempo_srh[s:n]
            lista_X_variable = lista_X[s:n]
            
            # Mediante ajuste de curvas calculamos los valores de SRH que mejor se ajustan con un valor de J0e introducido por el usuario
            lista_srh_independiente,lista_valor_independiente, NI = functions_curvefit.get_SRH_con_J0e(lista_densidadPortadores_filtrada_variable,lista_tiempo_srh_micros_variable,j0e)
            lista_srh_independiente_micros = [t * 1e+6 for t in lista_srh_independiente]
            #Suavizamos la curva de tiempo SRH
            lista_srh_independiente_micros_suave, lista_densidadPortadores_filtrada_suave = functions_curvefit.suavizado_curva(lista_srh_independiente_micros, lista_densidadPortadores_filtrada_variable)
            lista_srh_fin = lista_srh_independiente_micros

            #Almacenar los datos en un dataframe           
            data = pd.DataFrame({
                "Carrier Density (cm^-3)": lista_densidadPortadores_filtrada_variable,
                f"1/{tau} eff - 1/{tau} intrinseco": lista_tiempo_srh_micros_variable,
                f"{tau} SRH (us)": lista_srh_independiente_micros

            })

            #Pasamos los datos a un excel con una anchura de columnas dada
            excel_formatter.format_and_save_to_excel(data, "Lifetime.xlsx", "Lifetime SRH", "TableStyleMedium3", column_widths=[25, 33, 20])
            

            
            #Limpiar la figura y graficar los datos actualizados
            ax.clear()
            #Muestra valores SRH frente a la densidad de portadores
            if(not suav):   #Si la opcion de suavizado no esta seleccionada se muestran los valores normales
                ax.loglog(lista_densidadPortadores_filtrada_variable,lista_srh_independiente_micros, marker ="8", markersize = 6, color ="green")
    
            else:       #Si la opcion de suavizado si esta seleccionada se muestran los valores suavizados y los NO suavizados
                #Muestra los valores NO suavizados
                ax.loglog(lista_densidadPortadores_filtrada_variable,lista_srh_independiente_micros, marker ="8", markersize = 6, color ="green")
                #Muestra los valores suavizados
                ax.loglog(lista_densidadPortadores_filtrada_suave,lista_srh_independiente_micros_suave, marker ="8", markersize = 6, color ="blue", label="Suavizado")
            


            # Solo conectar el botón una vez
            if not button_connected:
                button.on_clicked(clickado)
                button_connected = True

            ##Muestra valores SRH frente a la densidad de portadores
            #ax.loglog(lista_densidadPortadores_filtrada_variable,lista_srh_independiente_micros, marker ="8", markersize = 6, color ="blue")

            ax.set_title(f"Lifetime & {tau} SRH") 
            ax.set_xlabel("Carrier Density (cm^-3)")
            ax.set_ylabel(f"{tau} SRH (us)")
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            ax.legend()
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            fig.canvas.draw_idle()
            plt.pause(0.1)

      
        def clickado(event):
            self.pintar_SRH_X(choice,temperatura,lista_srh_fin, lista_X_variable)


        #Se crea un botón para obtener el tiempo SRH
        button_ax = plt.axes([0.85, 0.4, 0.12, 0.05])  # Ajusta las dimensiones según tus necesidades
        button = Button(button_ax, 'SRH/X', color='lightgreen', hovercolor='0.975')

        # Posición del checkbox
        check_ax = fig.add_axes([0.85, 0.8, 0.12, 0.05])  # [left, bottom, width, height]
        check = CheckButtons(check_ax, ['Suavizar Datos'], [False])
        #Cuando se pulsa el boton se actualiza la grafica a suavizada
        check.on_clicked(update_graph)
        # Definir el rango de valores del slider
        val_min = 1
        val_max = len(lista_densidadPortadores)

        # Crear el slider con los límites inicial y final
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        slider = RangeSlider(slider_ax, '', val_min, val_max, valstep=1 , valinit=(val_min, val_max))
        # Rotar visualmente el slider
        slider_ax.invert_xaxis()
        # Ocultar el eje y por completo
        slider_ax.axis('off')


        # Conectar el slider a la función de actualización del gráfico
        slider.on_changed(update_graph)

        # Graficar los datos iniciales
        update_graph((1,len(lista_densidadPortadores)))

        # Se muestra la gráfica
        plt.ion()
        plt.show(block=False)


    ######################################################################################
    ######################################################################################


    def pintar_SRH_X(self, choice, temperatura, lista_srh_independiente_micros,lista_X ):

        lista_X_filtrada = [num for num in lista_X if num >=0]

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot()
        plt.subplots_adjust(right=0.83, bottom=0.15)

        button_connected = False  # Bandera para controlar la conexión del botón

        def update_graph(val):
            # Obtener los valores de los límites superior e inferior del slider
            lower_limit, upper_limit = slider.val

            global n
            global s        
            global valores_rectas
            nonlocal button_connected
            R2 = 0

            #Creamos un array para guardar los valores de las rectas:
            valores_rectas = [None, None, None, None]

            #Obtener estado suavizado
            linea_1 = check.get_status()[0]
            linea_2 = check_2.get_status()[0]
            # Obtener el valor actual del deslizador
            s = lower_limit
            n = upper_limit
            # Obtener los subconjuntos de datos a mostrar
            lista_X_filtrada_variable = lista_X_filtrada[s:n]
            lista_srh_independiente_micros_variable = lista_srh_independiente_micros[s:n]

            # Se define la curva suavizada llamando a función
            lista_srh_independiente_micros_variable_suave, lista_X_filtrada_variable_suave = functions_curvefit.suavizado_curva(lista_srh_independiente_micros_variable, lista_X_filtrada_variable)
            #Suavizamos de nuevo
            lista_srh_independiente_micros_variable_suave_2, lista_X_filtrada_variable_suave_2 = functions_curvefit.suavizado_curva(lista_srh_independiente_micros_variable_suave, lista_X_filtrada_variable_suave)
            #Suavizamos de nuevo
            lista_srh_independiente_micros_variable_suave_3, lista_X_filtrada_variable_suave_3 = functions_curvefit.suavizado_curva(lista_srh_independiente_micros_variable_suave_2, lista_X_filtrada_variable_suave_2)

            #Se saca los valores a una recta
            fit_values_1recta, r2_1, m_1recta, b_1recta = functions_curvefit.one_linear_fit(lista_X_filtrada_variable_suave_3, lista_srh_independiente_micros_variable_suave_3)
            #Se saca los valores a dos rectas
            fit_values_1, fit_values_2, fit_values, r2_2, m1, m2, b1, b2 = functions_curvefit.dual_linear_fit(lista_X_filtrada_variable_suave_3, lista_srh_independiente_micros_variable_suave_3)

            #Creamos un array para guardar los valores de las rectas:
            valores_rectas = [None, None, None, None]

            #Almacenar los datos en un dataframe           
            data2 = pd.DataFrame({
                "Lifetime (us)": lista_srh_independiente_micros_variable_suave_3,
                "X(n/p)": lista_X_filtrada_variable_suave_3,
                "m Verde" : m_1recta,
                "b Verde" : b_1recta,
                "m Rojo": m1,
                "b Rojo": b1,
                "m Azul": m2,
                "b Azul": b2
            })
            #Pasamos los datos a un excel con una anchura de columnas dada
            excel_formatter.format_and_save_to_excel(data2, "Lifetime.xlsx", "Lifetime SRH_X", "TableStyleMedium4", column_widths=[30, 30, 20, 20,  20, 20, 20, 20])

            #Limpiar la figura y graficar los datos actualizados
            ax.clear()

            #Muestra valores SRH frente a la densidad de portadores
            if(linea_1):   #Si la opcion de 1 linea no esta seleccionada se muestran los valores normales
                ax.plot(lista_X_filtrada_variable_suave_3, lista_srh_independiente_micros_variable_suave_3, marker = "o", markersize = 6, color ="black", label='Datos')
                ax.plot(lista_X_filtrada_variable_suave_3, fit_values_1recta, color='green', linestyle='--', label='Ajuste segmento total')
                valores_rectas =[m_1recta, b_1recta, None, None]
                R2 = r2_1
            elif(linea_2):
                ax.plot(lista_X_filtrada_variable_suave_3, lista_srh_independiente_micros_variable_suave_3, marker = "o", markersize = 6, color ="black", label='Datos')
                ax.plot(lista_X_filtrada_variable_suave_3, fit_values_1, color='red', linestyle='--', label='Ajuste Defecto 1')
                ax.plot(lista_X_filtrada_variable_suave_3, fit_values_2, color='blue', linestyle='--', label='Ajuste Defecto 2')
                ax.plot(lista_X_filtrada_variable_suave_3, fit_values, color='magenta', linestyle='--', label='Ajuste combinado')
                valores_rectas =[m1, b1, m2, b2]
                R2 = r2_2
            else:
                ax.plot(lista_X_filtrada_variable_suave_3, lista_srh_independiente_micros_variable_suave_3, marker = "o", markersize = 6, color ="black", label='Datos')

            #Se muestra el valor de R^2 a la derecha de la gráfica
            value_ax = fig.add_axes([0.85, 0.4, 0.12, 0.05])
            value_ax.set_xticks([])  # Ocultar ticks del eje X
            value_ax.set_yticks([])  # Ocultar ticks del eje Y
            value_ax.text(0.5, 0.5, f'$R^2$: { R2:.5f}', horizontalalignment='center', verticalalignment='center', transform=value_ax.transAxes)

            # Solo conectar el botón una vez
            if not button_connected:
                button.on_clicked(clickado)
                button_connected = True

            ax.set_title(f"X(n/p) - SRH Lifetime -{choice} Mode") 
            ax.set_xlabel("X(n/p)")
            ax.set_ylabel("Lifetime SRH (us)")
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            ax.legend()
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            fig.canvas.draw_idle()
            plt.pause(0.1)


        def clickado(event):
            #Pinta la grafica con los defectos
            self.pintar_defectos(choice, temperatura, valores_rectas)
            #Si esta seleccionado 1 linea se pinta una grafica de esa linea
            if(check.get_status()[0]):
                self.pintar_tau_n0(choice, temperatura, valores_rectas[0], valores_rectas[1], 'red')
            #Si esta seleccionado 2 lineas se pintan dos graficas una con cada linea
            elif(check_2.get_status()[0]):
                self.pintar_tau_n0(choice, temperatura, valores_rectas[0], valores_rectas[1], 'red')
                self.pintar_tau_n0(choice, temperatura, valores_rectas[2], valores_rectas[3], 'blue')



        #Se crea un botón para obtener los defectos
        button_ax = plt.axes([0.85, 0.2, 0.12, 0.05])  # Ajusta las dimensiones según tus necesidades
        button = Button(button_ax, 'Defectos', color='lightblue', hovercolor='0.975')

        # Posición del checkbox de una linea
        check_ax = fig.add_axes([0.85, 0.8, 0.12, 0.05])  # [left, bottom, width, height]
        check = CheckButtons(check_ax, ['1 Recta'], [False])
        #Cuando se pulsa el boton se actualiza la grafica a suavizada
        check.on_clicked(update_graph)

        # Posición del checkbox de dos lineas
        check_ax_2 = fig.add_axes([0.85, 0.6, 0.12, 0.05])  # [left, bottom, width, height]
        check_2 = CheckButtons(check_ax_2, ['2 Rectas'], [False])
        #Cuando se pulsa el boton se actualiza la grafica a suavizada
        check_2.on_clicked(update_graph)

        # Definir el rango de valores del slider
        val_min = 1
        val_max = len(lista_X)
        # Crear el slider con los límites inicial y final
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        slider = RangeSlider(slider_ax, '', val_min, val_max, valstep=1 , valinit=(val_min, val_max))
        # Rotar visualmente el slider
        slider_ax.invert_xaxis()
        # Ocultar el eje y por completo
        slider_ax.axis('off')
        # Conectar el slider a la función de actualización del gráfico
        slider.on_changed(update_graph)

        # Graficar los datos iniciales
        update_graph((1,len(lista_X)))

        # Se muestra la gráfica
        plt.ion()
        plt.show(block=False)
    

    ######################################################################################
    ######################################################################################

    #Posible mejora con zoom en la gráfica
    def pintar_defectos(self, choice, temperatura, valores_rectas):
        m1 = valores_rectas[0]
        b1 = valores_rectas[1]
        m2 = valores_rectas[2]
        b2 = valores_rectas[3]

        lista_valores_k_1, Et_1 = functions_timelife.calculo_linea_defecto(m1, b1, temperatura)
        if (m2 !=None and b2 != None):
            lista_valores_k_2, Et_2 = functions_timelife.calculo_linea_defecto(m2, b2, temperatura)

        # Cargar el Excel con los valores de los defectos
        #file_path = os.path.join(os.getcwd(), 'data_defects_Etk.xlsx') ##Se puede usar un excel con datos mucho mas amplios
        file_path = os.path.join(os.getcwd(), 'data_defects_Etk_reduced.xlsx')
        df = pd.read_excel(file_path)

        #Almacenar los datos en un dataframe           
        data = pd.DataFrame({
            "k Rojo": lista_valores_k_1,
            "Et Rojo": Et_1,
            "k Azul": lista_valores_k_2,
            "Et Azul": Et_2
            })
            #Pasamos los datos a un excel con una anchura de columnas dada
        excel_formatter.format_and_save_to_excel(data, "Lifetime.xlsx", "Defectos", "TableStyleMedium5", column_widths=[25, 25, 25, 25])

        # Extraer los datos relevantes
        x = df['Et-Ev (eV)']
        y = df['k']
        labels = df['Element']

        # Crear la figura
        fig = go.Figure()

        # Añadir los puntos de los defectos
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='markers+text',
            text=labels,
            textposition='top center',
            marker=dict(size=10),
            name='Defectos'
        ))

        # Añadir la línea de defectos de la primera recta calculada
        fig.add_trace(go.Scatter(
            x=Et_1, y=lista_valores_k_1,
            mode='lines+markers',
            marker=dict(size=5, color='red'),
            line=dict(color='red'),
            name='Línea de Defecto 1'
        ))
        # Añadir la línea de defectos de la segunda recta calculada 
        if (m2 !=None and b2 != None):
            fig.add_trace(go.Scatter(
                x=Et_2, y=lista_valores_k_2,
                mode='lines+markers',
                marker=dict(size=5, color='blue'),
                line=dict(color='blue'),
                name='Línea de Defecto 2' 
            ))

        # Configurar el título y los ejes
        fig.update_layout(
            title=f"Defectos - {choice} Mode",
            xaxis_title="Et - Ev (eV)",
            yaxis_title="kDPSS",
            yaxis_type="log",
            yaxis=dict(
                tickmode='array',
               tickvals=[0.01, 0.1, 1, 10, 100, 1000, 10000],
                ticktext=['0.01', '0.1', '1', '10', '100', '1000', '10000']
            ),
            xaxis=dict(range=[0, 1.1242]),
            height=800,
            width=1200
        )

        # Mostrar la figura
        fig.show()


    ######################################################################################
    ######################################################################################

    def pintar_tau_n0(self, choice, temperatura, m, b, color_recta):

        taun0, Et = functions_timelife.calculo_tau_n0(m, b, temperatura)

        # Crear la figura
        fig = go.Figure()

        # Añadir la línea de defectos de la primera recta calculada
        fig.add_trace(go.Scatter(
            x=Et, y=taun0,
            mode='lines+markers',
            marker=dict(size=5, color=color_recta),
            line=dict(color=color_recta),
            name='Línea de Defecto'
        ))

        # Configurar el título y los ejes
        fig.update_layout(
            title=f"Defecto 1",
            xaxis_title="Et - Ev (eV)",
            yaxis_title=f"{tau}n0 [us]",
            height=800,
            width=1200
        )
        if(color_recta == 'red'):
            fig.update_layout(
            title="Defecto 1"
            )
        elif(color_recta == 'blue'):
            fig.update_layout(
            title="Defecto 2"
            )
        # Mostrar la figura
        fig.show()


    ######################################################################################
    ######################################################################################

        
    def pintar_todas_movilidades(self, choice, temperatura):
        lista_densidadPortadoresSinton = self.densidad_portadoresSintonList(choice, temperatura)
        lista_tiempo_recombinacionSinton = self.tiempo_recombinacionSintonList(choice, temperatura)
        lista_densidadPortadoresDorkel = self.densidad_portadoresDorkelList(choice, temperatura)
        lista_tiempo_recombinacionDorkel = self.tiempo_recombinacionDorkelList(choice, temperatura)
        lista_densidadPortadoresKlaassen = self.densidad_portadoresKlaassenList(choice, temperatura)
        lista_tiempo_recombinacionKlaassen = self.tiempo_recombinacionKlaassenList(choice, temperatura)
        lista_densidadPortadoresSchindler = self.densidad_portadoresSchindlerList(choice, temperatura)
        lista_tiempo_recombinacionSchindler = self.tiempo_recombinacionSchindlerList(choice, temperatura)
        lista_tiempo_recombinacionSinton_micros = [t * 1e+6 for t in lista_tiempo_recombinacionSinton]  # Conversión a microsegundos
        lista_tiempo_recombinacionDorkel_micros = [t * 1e+6 for t in lista_tiempo_recombinacionDorkel]  # Conversión a microsegundos
        lista_tiempo_recombinacionKlaassen_micros = [t * 1e+6 for t in lista_tiempo_recombinacionKlaassen]  # Conversión a microsegundos
        lista_tiempo_recombinacionSchindler_micros = [t * 1e+6 for t in lista_tiempo_recombinacionSchindler]  # Conversión a microsegundos
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot()
        slider_ax = plt.axes([0.15, 0.0001, 0.7, 0.03])  # Modificar las coordenadas y del deslizador
        slider = Slider(slider_ax, 'Rango de valores', 1, len(lista_densidadPortadoresSinton), valinit=len(lista_densidadPortadoresSinton), valstep=1, color ="green")
        def update_graph(val,slider):
            # Obtener el valor actual del deslizador
            n = int(val)
            # Obtener los subconjuntos de datos a mostrar
            lista_densidadPortadoresSinton_variable = lista_densidadPortadoresSinton[:n]
            lista_tiempo_recombinacionSinton_micros_variabe = lista_tiempo_recombinacionSinton_micros[:n]
            lista_densidadPortadoresDorkel_variable = lista_densidadPortadoresDorkel[:n]
            lista_tiempo_recombinacionDorkel_micros_variabe = lista_tiempo_recombinacionDorkel_micros[:n]
            lista_densidadPortadoresKlaassen_variable = lista_densidadPortadoresKlaassen[:n]
            lista_tiempo_recombinacionKlaassen_micros_variabe = lista_tiempo_recombinacionKlaassen_micros[:n]
            lista_densidadPortadoresSchindler_variable = lista_densidadPortadoresSchindler[:n]
            lista_tiempo_recombinacionSchindler_micros_variabe = lista_tiempo_recombinacionSchindler_micros[:n]
            data = pd.DataFrame({"Carrier Density (cm^-3) Sinton": lista_densidadPortadoresSinton_variable, "Lifetime (us) Sinton": lista_tiempo_recombinacionSinton_micros_variabe, "Carrier Density (cm^-3) Dorkel": lista_densidadPortadoresDorkel_variable,"Lifetime (us) Dorkel" :lista_tiempo_recombinacionDorkel_micros_variabe, "Carrier Density (cm^-3) Klaassen" :lista_densidadPortadoresKlaassen_variable, "Lifetime (us) Klaassen": lista_tiempo_recombinacionKlaassen_micros_variabe, "Carrier Density (cm^-3) Schindler" : lista_densidadPortadoresSchindler_variable, "Lifetime (us) Schindler": lista_tiempo_recombinacionSchindler_micros_variabe  })
            # Guardar los datos en un archivo Excel
            data.to_excel("Lifetime_All_Modes.xlsx", index=False)
            # Limpiar la figura y graficar los datos actualizados
            ax.clear()
            ax.semilogx(lista_densidadPortadoresSinton_variable, lista_tiempo_recombinacionSinton_micros_variabe, marker ='o', markersize=3, label="Sinton")
            ax.semilogx(lista_densidadPortadoresDorkel_variable, lista_tiempo_recombinacionDorkel_micros_variabe, marker ='o', markersize=3, label="Dorkel")
            ax.semilogx(lista_densidadPortadoresKlaassen_variable, lista_tiempo_recombinacionKlaassen_micros_variabe, marker ='o', markersize=3, label="Klaassen")
            ax.semilogx(lista_densidadPortadoresSchindler_variable, lista_tiempo_recombinacionSchindler_micros_variabe, marker ='o', markersize=3, label="Schindler")
            ax.set_title("Lifetime vs. Carrier Density All Modes") 
            ax.grid(which='both', axis='both', linestyle=':', linewidth=0.5)
            ax.set_xlabel("Carrier Density (cm^-3)")
            ax.set_ylabel("Lifetime (us)")
            ax.set_ylim(0, None)
            ax.legend()
            fig.canvas.draw_idle()
            plt.pause(0.0001)
        # Conectar el slider a la función de actualización del gráfico
        slider.on_changed(lambda val: update_graph(val,slider))
        update_graph(len(lista_densidadPortadoresSinton),slider)
        plt.ion()
        plt.show(block = False)



