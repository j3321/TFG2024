import pandas as pd
from openpyxl import load_workbook  # Importa load_workbook desde openpyxl
from openpyxl.styles import Alignment

def format_and_save_to_excel(data, file_name, column_widths=None):
    """
    Aplica el formato científico y ajusta el ancho de las columnas antes de guardar el DataFrame en un archivo Excel.
    """
    # Especificar el formato científico para todas las columnas
    formato_cientifico = "{:.4e}"  # Puedes ajustar el número de decimales según tus preferencias

    # Aplicar el formato científico a todas las columnas
    for columna in data.columns:
        data[columna] = data[columna].apply(lambda x: formato_cientifico.format(x))

    # Guardar el DataFrame en un archivo Excel
    data.to_excel(file_name, index=False)

    if column_widths:
        # Abrir el archivo Excel y ajustar el ancho de las columnas
        wb = load_workbook(file_name)  # Usa load_workbook de openpyxl
        ws = wb.active
        for i, column_width in enumerate(column_widths):
            ws.column_dimensions[ws.cell(row=1, column=i+1).column_letter].width = column_width

        # Centrar los datos en todas las celdas
        for row in ws.iter_rows(min_row=2, min_col=1):  # Excluye la fila de encabezados
            for cell in row:
                cell.alignment = Alignment(horizontal='center', vertical='center')
                
        wb.save(file_name)