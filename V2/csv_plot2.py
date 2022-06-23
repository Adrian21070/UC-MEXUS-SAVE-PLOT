# Archivo que contiene las funciones utilizadas para el graficado con csv
import plots as Func
import PySimpleGUI as sg
import pandas as pd
import numpy as np
import sys
import os
import math
from datetime import datetime, timedelta
from dateutil import tz

# Fuentes para la interfaz
font = ('Times New Roman', 16)
font2 = ('Times New Roman', 12)
font3 = ('Times New Roman', 14)

# Columnas de interfaz reutilizables.
col1=[[sg.Text('Selecciona los datos a analizar')],
        [sg.Radio('Canal A', "Canal", default=True, key='Channel_A'), sg.Radio('Canal B', "Canal", default=False, key='Channel_B')],
        [sg.Radio('PM 1.0 ATM', 'PM', default=False, key="PM 1.0 ATM"), sg.Radio('PM 2.5 ATM', 'PM', default=True, key="PM 2.5 ATM")],
        [sg.Radio('PM 10.0 ATM', 'PM', default=False, key="PM 10.0 ATM"), sg.Radio('PM 1.0 CF', 'PM', default=False, key="PM 1.0 CF")],
        [sg.Radio('PM 2.5 CF', 'PM', default=False, key="PM 2.5 CF"), sg.Radio('PM 10.0 CF', 'PM', default=False, key="PM 10.0 CF")]]

PA_Onl = {"PM 1.0 ATM": "PM1.0_ATM_ug/m3", "PM 2.5 ATM": "PM2.5_ATM_ug/m3",
        "PM 10.0 ATM": "PM10.0_ATM_ug/m3", "PM 1.0 CF": "PM1.0_CF1_ug/m3",
        "PM 2.5 CF": "PM2.5_CF1_ug/m3", "PM 10.0 CF": "PM10.0_CF1_ug/m3",
        "PM 1.0 ATM B": "PM1.0_ATM_B_ug/m3", "PM 2.5 ATM B": "PM2.5_ATM_B_ug/m3",
        "PM 10.0 ATM B": "PM10.0_ATM_B_ug/m3", "PM 1.0 CF B": "PM1.0_CF1_B_ug/m3",
        "PM 2.5 CF B": "PM2.5_CF1_B_ug/m3", "PM 10.0 CF B": "PM10.0_CF1_B_ug/m3"}

def csv_files(window):
    # Solicita archivos csv

    layout = [[sg.Text('Seleccione la carpeta donde se encuentras los archivos csv', font=font)],
            [sg.Text(f'Ubicación de la carpeta: '), sg.Input(), sg.FolderBrowse()],
            [sg.Button('Extraer',key='TypeData'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font=font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
    data, minimum, maximum, window = Func.open_csv(window, value)

    if isinstance(data, bool):
        return window, 'Extraction', 0, minimum, maximum

    data_sorted = {}
    indx_sort = sorted(data.items())

    for ii in indx_sort:
        data_sorted[ii[0]] = ii[1]
        
    return window, event, data_sorted, minimum, maximum

def data_type(window):
    # Se pregunta el tipo de dato que quiere analizar.
    layout = [col1, [sg.Button('Next', key='Sensor_info'), sg.Button('Return',key='Extraction'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    elif 'Extraction' in event:
        return window, event, 0

    PMType = {}

    if value['Channel_B']:
        for ii in value.keys():
            if value[ii] and ii != 'Channel_B':
                PMType[ii + ' B'] = True

    else:
        for ii in value.keys():
            if value[ii] and ii != 'Channel_A':
                PMType[ii] = True

    return window, event, PMType

def sensors_info(window):
    # Solicita información de los sensores
    layout = [[sg.Text('Datos acerca del número de sensores y su disposición',font=font)],
                [sg.Text('Num. de Sensores', size =(25, 1)), sg.InputText(key='NumSen')],
                [sg.Text('Num. Columnas de Sensores', size =(25, 1)), sg.InputText(key='Columns')],
                [sg.Text('Num. Filas de Sensores', size =(25, 1)), sg.InputText(key='Rows')],
                [sg.Text('Distancia entre Columnas', size =(25, 1)), sg.InputText(key='Col_dis')],
                [sg.Text('Distancia entre Filas', size =(25, 1)), sg.InputText(key='Row_dis')],
                [sg.Text('Distancia respecto a la carretera', size=(25,1)), sg.InputText(key='Y0')],
                [sg.Text('Distancia lateral a otras vias', size=(25,1)), sg.InputText(key='X0')],
                [sg.Button("Next",key='SensorDistribution'), sg.Button('Return',key='TypeData'), sg.Button('Exit')]]
            
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
    return window, event, value

def distribution(window,num_sen,rows,columns,row_dist,col_dist,x0,y0):
    # Solicita como se distribuyeron los sensores en el campo.

    # Creación de un grid para la interfaz
    chain = list(range(1,num_sen+1))
    coordenadas = {}
    it = 0
    
    for i in range(rows):
        for j in range(columns):
            coordenadas[f'{i},{j}'] = chain[it]
            it += 1

    layout = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
                [sg.Frame('Disposición de los sensores', [[sg.Input(coordenadas[f'{row},{col}'],
                key=f'{row},{col}', size=(5,1)) for col in range(columns)]
                for row in range(rows)])],
                [sg.Button('Next'),sg.Button('Return',key='Sensor_info'),sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, indx = window.read()

    if 'Exit' in event:
        shutdown(window)

    # Calculo de X y Y
    x = np.array(list(range(0,columns)))*col_dist + x0
    y = np.array(list(range(0,rows)))*row_dist + y0
    x_axis = []
    y_axis = []

    # Matriz de coordenadas
    layout = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
                [sg.Frame('Coordenadas de los sensores', [[sg.Input(f'{col},{row}',
                key=(col,row), size=(5,1)) for col in x]
                for row in y])],
                [sg.Button('Next',key='Date_hour'),sg.Button('Return',key='Sensor_info'),sg.Button('Exit')]]
    
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)

    for ii in value.values():
        ii = eval(ii)
        x_axis.append(ii[0])
        y_axis.append(ii[1])

    x_axis = np.array([x_axis])
    y_axis = np.array([y_axis])

    """ X y Y deben ser matrices, no vectores """

    indx = dict(zip(list(value.values()), list(indx.values())))

    for jj in indx.keys():
        num = int(indx[jj])
        if num > 99:
            continue
        elif num >= 10 and num <= 99:
            indx[jj] = f'0{indx[jj]}'
        else:
            indx[jj] = f'00{indx[jj]}'

    return window, event, indx, x_axis, y_axis

def date_hour(window, key=0):
    layout = [[sg.Text('Selección de fecha y hora de las mediciones',font=font)],
                [sg.CalendarButton('Dia de inicio de la medición',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='Start')],
                [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(key='Start_hour')],
                [sg.Text('')],
                [sg.CalendarButton('Dia del fin de la medición',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='End')],
                [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(key='End_hour')],
                [sg.Button("Next",key='Extraction'), sg.Button('Return',key='SensorDistribution'),sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)

    if key == 1:
        # Paso las fechas a datetime y saco los dias entre ambas fechas en utc.
        start = datetime.strptime(value['Start'], '%Y-%m-%d').replace(tzinfo=tz.tzutc())
        end = datetime.strptime(value['End'], '%Y-%m-%d').replace(tzinfo=tz.tzutc())
        days = [ii for ii in range(start.day, end.day+1, 1)]
        return window, event, value, days

    else:
        return window, event, value

def graph_domain(window):
    # Se pregunta que graficas quiere realizar
    layout = [[sg.Text('Favor de seleccionar que graficas desea obtener')],
            [sg.Checkbox('Animación 3D (superficie)', default=False, key='Animation3D')],
            [sg.Checkbox('Lateral average', default=False, key='LateralAvg')],
            [sg.Checkbox('Registro historico de filas', default=False, key='Historico')],
            [sg.Text('Tiempo de duración animación (Min.)', size =(25, 1)), sg.InputText(key='Length')],
            [sg.Text('Promedios de los datos en horas (1=60min)', size =(25, 1)), sg.InputText(key='delta')],
            [sg.Button('Graficar'), sg.Button('Exit')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)

    return window, value

def data_average(data, minimum, maximum, delta, PMType, begin, final):
    begin = datetime.strptime(begin, '%Y-%m-%d %H:%M').replace(tzinfo=tz.tzutc())
    final = datetime.strptime(final, '%Y-%m-%d %H:%M').replace(tzinfo=tz.tzutc())

    new_data = {}
    PMType = PA_Onl[list(PMType.keys())[0]]
    delta = float(delta)
    first_start = max(minimum.values())
    final_end = min(maximum.values())

    if first_start < begin:
        first_start = begin
    
    if final_end > final:
        final_end = final

    dif = final_end - first_start

    seconds = dif.seconds + dif.days*24*60*60
    cycles = math.ceil(seconds/(delta*60*60))
    
    maximum = []
    minimum = []

    for ii in data.keys():
        start = first_start
        end = first_start + timedelta(hours=delta)

        new_data[ii] = pd.DataFrame(columns=['created_at', PMType])

        # Filtrar data
        df = data[ii]
        df = df[['created_at', PMType]]
        date = df['created_at']
        
        for jj in range(cycles):
            # Se tomaran pedazos de datos en intervalos de tiempo para sacarles su promedio
            rows = df.loc[((date >= start) & (date < end))]

            # Calculamos promedios
            prom = [start.astimezone(tz.tzlocal()).strftime("%Y/%m/%d, %H:%M") + ' (hora de inicio)']
            prom.append(round(np.mean(rows[PMType]),4))

            new_data[ii].loc[jj] = prom

            if jj != cycles-2:
                start = end
                end = start + timedelta(hours=delta)
            else:
                start = end
                end = final_end + timedelta(seconds=1)

        maximum.append(max(new_data[ii][PMType]))
        minimum.append(min(new_data[ii][PMType]))

    limites = [min(minimum), max(maximum)]
    return new_data, limites, PMType

def graph(window, x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, PMType, indx, limites, value):
    PMType = [PMType]
    Func.graphs(x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, value, PMType, indx, limites, value['delta'])
    
    # Preguntamos si queremos modificar algo de las graficas, regresamos al inicio de esta función.
    layout = [[sg.Text('Si requiere modificar algo de las graficas de nuevo.')],
                [sg.Text('Favor de seleccionar "Repetir graficado"')],
                [sg.Button('Repetir graficado'), sg.Button('Finalizar programa')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if event == 'Repetir graficado':
        event = 'Graph'
        return window, event, value

    else:
        shutdown(window)

def shutdown(window):
    window.close()
    sys.exit()