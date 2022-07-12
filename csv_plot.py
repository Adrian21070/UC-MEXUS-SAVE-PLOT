# Archivo que contiene las funciones utilizadas para el graficado con csv
from matplotlib import animation
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
font = ('Times New Roman', 14)
font2 = ('Times New Roman', 12)
font3 = ('Times New Roman', 18)

PA_Onl = {"PM 1.0 ATM": "PM1.0_ATM_ug/m3", "PM 2.5 ATM": "PM2.5_ATM_ug/m3",
        "PM 10.0 ATM": "PM10.0_ATM_ug/m3", "PM 1.0 CF": "PM1.0_CF1_ug/m3",
        "PM 2.5 CF": "PM2.5_CF1_ug/m3", "PM 10.0 CF": "PM10.0_CF1_ug/m3",
        "PM 1.0 ATM B": "PM1.0_ATM_B_ug/m3", "PM 2.5 ATM B": "PM2.5_ATM_B_ug/m3",
        "PM 10.0 ATM B": "PM10.0_ATM_B_ug/m3", "PM 1.0 CF B": "PM1.0_CF1_B_ug/m3",
        "PM 2.5 CF B": "PM2.5_CF1_B_ug/m3", "PM 10.0 CF B": "PM10.0_CF1_B_ug/m3"}

def csv_files(window, path):
    # Solicita archivos csv

    if path:
        layout = [[sg.Text('Seleccione la carpeta donde se encuentran los archivos csv', font=font3)],
                [sg.Text(f'Ubicación de la carpeta: '), sg.Input(path), sg.FolderBrowse(initial_folder=path)],
                [sg.Button('Extraer',key='TypeData'), sg.Button('Exit')]]
    else:
        layout = [[sg.Text('Seleccione la carpeta donde se encuentran los archivos csv', font=font3)],
                [sg.Text(f'Ubicación de la carpeta: '), sg.Input(), sg.FolderBrowse()],
                [sg.Button('Extraer',key='TypeData'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480))
    event, value = window.read()

    if event in ('Exit', None):
        shutdown(window)

    if path:
        value['Browse'] = value[0]
    
    data, minimum, maximum, window = Func.open_csv(window, value)

    if isinstance(data, bool):
        return window, 'Extraction', 0, minimum, maximum

    data_sorted = {}
    indx_sort = sorted(data.items())
    del data
    for ii in indx_sort:
        data_sorted[ii[0]] = ii[1]
        
    return window, event, data_sorted, minimum, maximum

def data_type(window):
    # Se pregunta el tipo de dato que quiere analizar.

    col1=[[sg.Text('Selecciona los datos a analizar', font=font3, justification='center',expand_x=True)],
        [sg.Frame('',[[sg.Radio('Canal A', "Canal", default=True, key='Channel_A', size=(12,1)), sg.Radio('Canal B', "Canal", default=False, key='Channel_B')],
        [sg.Radio('PM 1.0 ATM', 'PM', default=False, key="PM 1.0 ATM", size=(12,1)), sg.Radio('PM 1.0 CF', 'PM', default=False, key="PM 1.0 CF")],
        [sg.Radio('PM 2.5 ATM', 'PM', default=True, key="PM 2.5 ATM", size=(12,1)), sg.Radio('PM 2.5 CF', 'PM', default=False, key="PM 2.5 CF")],
        [sg.Radio('PM 10.0 ATM', 'PM', default=False, key="PM 10.0 ATM", size=(12,1)), sg.Radio('PM 10.0 CF', 'PM', default=False, key="PM 10.0 CF")]],element_justification='center')]]
    
    layout = [col1, [sg.Button('Next', key='Sensor_info'), sg.Button('Return',key='Extraction'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480),element_justification='center')
    event, value = window.read()

    if event in ('Exit', None):
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

def sensors_info(names, window):
    # Obtengo sus nombres
    indx = []
    try:
        # Para que esto funcione, los archivos deben llamarse SXXX_20XX_YY_ZZ o SXXX_20XXYYZZ
        for ii in names:
            indx.append(ii[-3:])
            aa = int(ii[-3:]) # Si esto falla, entonces no tenian los nombres correctos.

        del aa
    except:
        layout = [[sg.Text('Error al leer un archivo', font=('Times New Roman',18))],
                [sg.Text(f'Se tuvo problemas al leer el archivo {ii}.')],
                [sg.Text('El nombre del archivo no es el correcto, debe tener la forma')],
                [sg.Text('SXXX_YYYY_MM_DD')],
                [sg.Button('Return', key='Extraction'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()

        return window, event, value, indx, True

    # Solicita información de los sensores
    layout = [[sg.Text('Datos acerca de la medición en campo',font=font3, justification='center', expand_x=True)],
                [sg.Text('',size=(1,1),font=('Times New Roman',1))],
                [sg.Text(f'Cuenta con {len(indx)} sensores a disposición.')],
                [sg.Text('Favor de seleccionar el número de columnas y filas utilizadas en el campo.\n')],
                [sg.Text('Num. Columnas de Sensores', size =(25, 1)), sg.InputText(key='Columns')],
                [sg.Text('Num. Filas de Sensores', size =(25, 1)), sg.InputText(key='Rows')],
                [sg.Text('Distancia entre Columnas', size =(25, 1)), sg.InputText(key='Col_dis')],
                [sg.Text('Distancia entre Filas', size =(25, 1)), sg.InputText(key='Row_dis')],
                [sg.Text('Distancia respecto a la carretera', size=(25,1)), sg.InputText(key='Y0')],
                [sg.Text('Distancia lateral a otras vias', size=(25,1)), sg.InputText(key='X0')],
                [sg.Text('',size=(1,1),font=('Times New Roman',1))],
                [sg.Button("Next",key='SensorDistribution'), sg.Button('Return',key='TypeData'), sg.Button('Exit')]]
            
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, value = window.read()

    if event in ('Exit', sg.WIN_CLOSED):
        shutdown(window)
    elif 'TypeData' in event:
        return window, event, value, indx, False

    try:
        a = int(value['Columns'])
        a1 = int(value['Rows'])
        a2 = float(value['Col_dis'])
        a3 = float(value['Row_dis'])
        a4 = float(value['Y0'])
        a5 = float(value['X0'])

        del a, a1, a2, a3, a4, a5
        return window, event, value, indx, False

    except:
        layout = [[sg.Text('Favor de introducir unicamente números en los campos', font=('Times New Roman',18))],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        return window, event, value, indx, True

def distribution(window,num_sen,rows,columns):
    # Solicita como se distribuyeron los sensores en el campo.

    # Creación de un grid para la interfaz
    chain = num_sen
    rows_sen = {}
    lay = []
    layout = []
    it = 0
    
    try:
        for i in range(rows):
            for j in range(columns):
                if it < len(chain):
                    lay.append(sg.Input(chain[it], key=f'({i},{j})',size=(5,1)))
                    #coordenadas[f'{i},{j}'] = chain[it]
                else:
                    lay.append(sg.Input('', key=f'({i},{j})', size=(5,1)))
                it += 1
            layout.append(lay)
            lay = []
    except:
        layout = [[sg.Text('Fallo en el número de filas y columnas', font=('Times New Roman',18))],
                [sg.Text(f'El número de filas y columnas no cubren a los {len(num_sen)} sensores')],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        event = 'Sensor_info'
        return window, event, value, indx, False, rows_sen

    #if it < len(num_sen):
    #    event = 'Sensor_info'
    #    return window, event, num_sen, False

    frame = [[sg.Frame('Disposicion de los sensores', layout, element_justification='center', expand_x=True)]]
    
    del layout, lay

    layout = [[sg.Text('Carretera', justification='center', font=('Times New Roman', 24), expand_x=True)],
            [sg.Column(frame, scrollable=True, expand_y=True, justification='center')],
        #    [sg.Column(frame, scrollable=True, justification='center')],
            [sg.Text('Escribe el número de identificación de los sensores en los recuadros (Ejemplo: 1, 6, 23).')],
            [sg.Text('En el recuadro se despliegan todos los sensores disponibles, si no requiere verificar')],
            [sg.Text('alguno de ellos, deje en blanco su recuadro. Tambien puede cambiarlos de posición,')],
            [sg.Text('pero no es valido repetir sensores. Carretera lateral'), sg.Combo(['Derecha','Izquierda','No'],default_value='Izquierda',key='Carretera_Lateral')],
            [sg.Button('Continue',key='Coordenadas'),sg.Button('Return',key='Sensor_info'),sg.Button('Exit')],
            [sg.Text('',size=(1,1),font=('Times New Roman', 1))]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, indx = window.read()
    carretera = []
    if event in ('Exit', sg.WIN_CLOSED):
        shutdown(window)
    if event != 'Coordenadas':
        return window, event, indx, carretera, False, rows_sen

    # Extraigo los valores dados por el usuario y quito los repetidos.
    result = {}
    carretera = indx['Carretera_Lateral']
    del indx['Carretera_Lateral']

    # Quito los espacios vacios.
    for key,val in indx.items():
        if val == '':
            continue
        elif val == ' ':
            continue
        elif val == '  ':
            continue
        elif val == '   ':
            continue
        elif val == '    ':
            continue
        else:
            result.update({key:val})

    # Hago una prueba para evitar que el usuario rompa el código.
    try:
        
        # Los paso de string a enteros.
        result2 = {}
        for key, ii in result.items():
            e = int(ii)
            if (e > 9) and (e < 100):
                e = f'0{e}'
            elif (e < 10):
                e = f'00{e}'
            else:
                e = f'{e}'
            result2.update({key:e})
    
        result = {}
    
        for key, val in result2.items():
            # Quito los repetidos.
            if val not in list(result.values()):
                result.update({key:val})

        indx = result
        del result, result2
    
        kk = 0
        k2 = 0
        for ii in indx.keys():
            e = eval(ii)
            y = e[0]
            if k2 == 0:
                k2 += 1
                rows_sen[kk] = []
                y2 = y
            if y != y2:
                kk += 1
                rows_sen[kk] = []
                rows_sen[kk].append(indx[ii])
            else:
                rows_sen[kk].append(indx[ii])
            y2 = y

        # Compruebo que los numeros esten dentro de los numeros dados por el usuario o del 1 a 30.
        llave = False

        for ii in indx.values():
            if ii in num_sen:
                pass

            else:
                llave = True
                # Si no se encuentra en el rango, se levanta un error y se pide ingresar de nuevo los datos.
                layout = [[sg.Text('Favor de introducir únicamente números enteros que estén',font=('Times New Roman', 18))],
                [sg.Text('entre el 1 y 30, o entre los números de los archivos csv cargados.',font=('Times New Roman', 18))],
                [sg.Button('Return'), sg.Button('Exit')]]
                window.close()
                window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
                event, value = window.read()
                if event in ('Exit', sg.WIN_CLOSED):
                    window.close()
                    sys.exit()
                break

        if llave:
            return window, event, num_sen, carretera, True, rows_sen

        return window, event, indx, carretera, False, rows_sen

    except:
        layout = [[sg.Text('Favor de introducir únicamente números enteros que estén',font=('Times New Roman', 18))],
                [sg.Text('entre 1 y 30, o entre los números de los archivos csv cargados.',font=('Times New Roman', 18))],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()

        return window, event, num_sen, carretera, True, rows_sen

def filtro_data(data, indx):
    data2 = {}
    for ii in indx.values():
        data2[f'Sensor {ii}'] = data[f'Sensor {ii}']
        
    return data2

def coordenadas(window, rows, row_dist, columns, col_dist, x0, y0, indx, lateral):
    # Calculo de X y Y
    x3 = np.array(list(range(0,columns)))*col_dist + x0
    y3 = np.array(list(range(0,rows)))*row_dist + y0
    x_axis = []
    y_axis = []

    lay = []
    layout = []
    for i in range(rows):
        y1 = i*row_dist + y0
        for j in range(columns):
            if lateral == 'Izquierda':
                x1 = j*col_dist + x0
            elif lateral == 'Derecha':
                x1 = (columns-j-1)*col_dist + x0
            else:
                x1 = j*col_dist

            if f'({i},{j})' in indx:
                lay.append(sg.Input(f'{x1},{y1}', key=f'({i},{j})',size=(10,1)))
            else:
                lay.append(sg.Input('', key=f'({i},{j})', size=(10,1)))
        layout.append(lay)
        lay = []
    
    frame = [[sg.Frame('Coordenadas de los sensores', layout, element_justification='center')]]

    # Matriz de coordenadas
    layout = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
                [sg.Column(frame,scrollable=True, expand_y=True, element_justification='center')],
                [sg.Text('Si requiere modificar las coordenadas de algun sensor modifique las casillas, cuide el')],
                [sg.Text('no introducir elementos que no sean números. Los espacios vacíos son debido')],
                [sg.Text('a sensores repetidos o espacios que el usuario dejo a propósito')],
                [sg.Button('Continue',key='Tipo_de_grafico'),sg.Button('Return',key='SensorDistribution'),sg.Button('Exit')]]
    
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480), element_justification='c')
    event, value = window.read()

    if event in ('Exit', sg.WIN_CLOSED):
        shutdown(window)
    elif event != 'Tipo_de_grafico':
        return window, event, indx, 0, 0

    try:
        for ii in value.keys():
            if ('' == value[ii]) or (' ' == value[ii]):
                pass
            else:
                e = eval(value[ii])
                x_axis.append(e[0])
                y_axis.append(e[1])
            
        x_axis = np.array([x_axis])
        y_axis = np.array([y_axis])
    except:
        layout = [[sg.Text('Favor de introducir únicamente números en las coordenadas')],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=('Times New Roman', 18), size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        
        event = 'Coordenadas'
        return window, event, indx, 0, 0

    """ X y Y deben ser matrices, no vectores """

    new_indx = dict(zip(list(value.values()), indx.values()))
    new_indx = {}
    for ii in value.keys():
        if ii in indx:
            new_indx[value[ii]] = indx[ii]

    return window, event, new_indx, x_axis, y_axis

def type_graph(window, memory):
    if memory:
        # Se pregunta que graficas quiere realizar
        layout = [[sg.Text('Favor de seleccionar que graficas desea obtener', font=font3)],
                [sg.Radio('Superficie', 'Type', default=memory['Superficie'], key='Surface'), sg.Radio('Animación', "Superficie", default=memory['Superficie_Anim'], key='An_superficie'), sg.Radio('Estática', "Superficie", default=memory['Superficie_Est'], key='Es_superficie')],
                [sg.Radio('Lateral average', 'Type', default=memory['LateralAvg'], key='LateralAvg'), sg.Radio('Animación', "Lateral", default=memory['LateralAvg_Anim'], key='An_lateral'), sg.Radio('Estática', "Lateral", default=memory['LateralAvg_Est'], key='Es_lateral')],
                [sg.Radio('Registro historico de filas', 'Type', default=memory['Historico'], key='Historico')],
                [sg.Button('Continue',key='Date_hour'), sg.Button('Return',key='Sensor_info'), sg.Button('Exit')]]

    else:
        # Se pregunta que graficas quiere realizar
        layout = [[sg.Text('Favor de seleccionar que graficas desea obtener', font=font3)],
                [sg.Radio('Superficie', 'Type', default=True, key='Surface'), sg.Radio('Animación', "Superficie", default=True, key='An_superficie'), sg.Radio('Estática', "Superficie", default=False, key='Es_superficie')],
                [sg.Radio('Lateral average', 'Type', default=False, key='LateralAvg'), sg.Radio('Animación', "Lateral", default=True, key='An_lateral'), sg.Radio('Estática', "Lateral", default=False, key='Es_lateral')],
                [sg.Radio('Registro historico de filas', 'Type', default=False, key='Historico')],
                [sg.Button('Continue',key='Date_hour'), sg.Button('Return',key='Sensor_info'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, value = window.read()

    if event in ('Exit', sg.WIN_CLOSED):
        shutdown(window)
    elif 'Sensor_info' in event:
        return window, value, event, False, memory

    # Se guarda en memoria los datos del usuario.
    memory['Superficie'] = value['Surface']
    memory['Superficie_Anim'] = value['An_superficie']
    memory['Superficie_Est'] = value['Es_superficie']
    memory['LateralAvg'] = value['LateralAvg']
    memory['LateralAvg_Anim'] = value['An_lateral']
    memory['LateralAvg_Est'] = value['Es_lateral']
    memory['Historico'] = value['Historico']

    if (value['Surface'] and value['An_superficie']) or (value['LateralAvg'] and value['An_lateral']):
        if 'Anim_Length' in memory:
            layout = [[sg.Text('Datos para la animación\n', font=font3, justification='center', expand_x=True)],
                    [sg.Text('Tiempo de duración animación (Min.)', size =(35, 1)), sg.InputText(memory['Anim_length'], key='Length')],
                    [sg.Text('Promedios de los datos en horas (1=60min)', size =(35, 1)), sg.InputText(memory['Anim_delta'], key='delta')],
                    [sg.Button('Continue',key='Date_hour'), sg.Button('Return', key='Tipo_de_grafico'), sg.Button('Exit')]]
        
        else:
            layout = [[sg.Text('Datos para la animación\n', font=font3, justification='center', expand_x=True)],
                    [sg.Text('Tiempo de duración animación (Min.)', size =(35, 1)), sg.InputText(key='Length')],
                    [sg.Text('Promedios de los datos en horas (1=60min)', size =(35, 1)), sg.InputText(key='delta')],
                    [sg.Button('Continue',key='Date_hour'), sg.Button('Return', key='Tipo_de_grafico'), sg.Button('Exit')]]
        
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
        event, value_anim = window.read()

        if event in ('Exit', sg.WIN_CLOSED):
            shutdown(window)

        if (not value_anim['Length']) or (not value_anim['delta']):
            # Se pide que ingrese datos validos
            layout = [[sg.Text('Favor de no dejar campos vacíos', font=font3)],
                    [sg.Button('Return'), sg.Button('Exit')]]
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
            event, value = window.read()
            if event in ('Exit', sg.WIN_CLOSED):
                window.close()
                sys.exit()

            return window, value, event, False, memory
        
        try:
            float(value_anim['delta'])
            float(value_anim['Length'])
        except:
            # Se pide que ingrese datos validos
            layout = [[sg.Text('Favor de introducir únicamente números en los campos', font=font3)],
                    [sg.Button('Return'), sg.Button('Exit')]]
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
            event, value = window.read()
            if event in ('Exit', sg.WIN_CLOSED):
                window.close()
                sys.exit()

            return window, value, event, False, memory

        # Se guarda en memoria los datos del usuario.
        memory['Anim_length'] = value_anim['Length']
        memory['Anim_delta'] = value_anim['delta']
        
        return window, value, event, value_anim, memory

    if ((value['Historico'])):
        if 'Anim_delta' in memory:
            layout = [[sg.Text('Datos para el gráfico\n', font=font3, justification='center', expand_x=True)],
                    [sg.Text('Promedios de los datos en horas (1=60min)', size =(35, 1)), sg.InputText(memory['Anim_delta'], key='delta')],
                    [sg.Button('Continue',key='Date_hour'), sg.Button('Return', key='Tipo_de_grafico'), sg.Button('Exit')]]
        
        else:
            layout = [[sg.Text('Datos para el gráfico\n', font=font3, justification='center', expand_x=True)],
                    [sg.Text('Promedios de los datos en horas (0.5=30min)', size =(35, 1)), sg.InputText('1', key='delta')],
                    [sg.Button('Continue',key='Date_hour'), sg.Button('Return', key='Tipo_de_grafico'), sg.Button('Exit')]]
        
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
        event, value_anim = window.read()

        if event in ('Exit', sg.WIN_CLOSED):
            shutdown(window)

        if (not value_anim['delta']):
            # Se pide que ingrese datos validos
            layout = [[sg.Text('Favor de no dejar campos vacíos', font=font3)],
                    [sg.Button('Return'), sg.Button('Exit')]]
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
            event, value = window.read()
            if event in ('Exit', sg.WIN_CLOSED):
                window.close()
                sys.exit()

            return window, value, event, False, memory
        
        try:
            float(value_anim['delta'])
        except:
            # Se pide que ingrese datos validos
            layout = [[sg.Text('Favor de introducir únicamente números en los campos', font=font3)],
                    [sg.Button('Return'), sg.Button('Exit')]]
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
            event, value = window.read()
            if event in ('Exit', sg.WIN_CLOSED):
                window.close()
                sys.exit()

            return window, value, event, False, memory

        # Se guarda en memoria los datos del usuario.
        memory['Anim_delta'] = value_anim['delta']
        
        return window, value, event, value_anim, memory

    return window, value, event, False, memory

def date_hour(window, maximum, minimum, memory, key=0):
    start = min(minimum.values()).strftime('%Y-%m-%d')
    end = max(maximum.values()).strftime('%Y-%m-%d')
    start_hr = min(minimum.values()).strftime('%H:%M')
    end_hr = max(maximum.values()).strftime('%H:%M')

    if 'Start_day' in memory:
        layout = [[sg.Text('Selección de fecha y hora de las mediciones a mostrar (UTC)\n',font=font3, justification='center', expand_x=True)],
                    [sg.CalendarButton('Dia de inicio',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(memory['Start_day'],key='Start')],
                    [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(memory['Start_hour'],key='Start_hour')],
                    [sg.Text('')],
                    [sg.CalendarButton('Dia final',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(memory['End_day'],key='End')],
                    [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(memory['End_hour'],key='End_hour')],
                    [sg.Button("Continue",key='Styles'), sg.Button('Return',key='Tipo_de_grafico'),sg.Button('Exit')]]

    else:
        layout = [[sg.Text('Selección de fecha y hora de las mediciones a mostrar (UTC)\n',font=font3, justification='center', expand_x=True)],
                    [sg.CalendarButton('Dia de inicio',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(start,key='Start')],
                    [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(start_hr,key='Start_hour')],
                    [sg.Text('')],
                    [sg.CalendarButton('Dia final',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(end,key='End')],
                    [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(end_hr,key='End_hour')],
                    [sg.Button("Continue",key='Styles'), sg.Button('Return',key='Tipo_de_grafico'),sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, value = window.read()

    if event in ('Exit', sg.WIN_CLOSED):
        shutdown(window)
    elif event != 'Styles':
        return window, event, value, 0, memory, False

    # Me aseguro que no esten vacios.
    if (not value['Start']) or (not value['End']) or (not value['Start_hour']) or (not value['End_hour']):
        layout = [[sg.Text('Favor de no dejar los espacios en blanco', justification='center', font=('Times New Roman', 18))],
            [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        return window, event, value, 0, memory, True # Mantengo el bucle
    
    start = value['Start'] + ' ' + value['Start_hour']
    end = value['End'] + ' ' + value['End_hour']

    # Compruebo que las horas esten bien
    try:
        start = datetime.strptime(start, '%Y-%m-%d %H:%M').replace(tzinfo=tz.tzutc())
        end = datetime.strptime(end, '%Y-%m-%d %H:%M').replace(tzinfo=tz.tzutc())
    except:
        layout = [[sg.Text('Favor de introducir de manera correcta las horas (hh:mm)', justification='center', font=('Times New Roman', 18))],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        return window, event, value, 0, memory, True # Mantengo el bucle

    delta = end - start
    delta = delta.days*24*60*60 + delta.seconds

    # Al menos debe haber una diferencia de 2 minutos entre inicio y fin de las fechas.
    if delta < 120:
        layout = [[sg.Text('La fecha de inicio debe ser por lo menos dos minutos menor a la final', justification='center', font=font3)],
            [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        return window, event, value, 0, memory, True # Mantengo el bucle
    
    # Guardo en memoria los datos del usuario
    memory['Start_day'] = value['Start']
    memory['Start_hour'] = value['Start_hour']
    memory['End_day'] = value['End']
    memory['End_hour'] = value['End_hour']

    if key == 1:
        # Paso las fechas a datetime y saco los dias entre ambas fechas en utc.
        start = datetime.strptime(value['Start'], '%Y-%m-%d').replace(tzinfo=tz.tzutc())
        end = datetime.strptime(value['End'], '%Y-%m-%d').replace(tzinfo=tz.tzutc())
        days = [ii for ii in range(start.day, end.day+1, 1)]
        return window, event, value, days, memory, False

    else:
        return window, event, value, 0, memory, False

def graph_domain(window, value, value_anim, PMType, memory):
    ### Se realizan ventanas para preguntar cosas sobre el diseño de las imagenes.
    ### Tipo de linea, colores, titulos, ticks, tamaño ...

    marker = {'Circle':'o', 'Diamond':'D', 'Triangle_up':'^', 'Triangle_down':'v', 'Star':'*', 'X':'X', 'No marker':'No marker'}
    color = {'Azul':'b', 'Rojo':'r', 'Verde':'g', 'Cyan':'c', 'Magenta':'m', 'Amarillo':'y', 'Negro':'k'}
    lines = {'Solid -':'-', 'Dashed --':'--', 'Dashdot -.':'-.', 'Dotted :':':', 'No line':'No line'}

    animation3d = []
    lateral_avg = []
    historico = []

    if value_anim:
        d = eval(value_anim['delta'])
    pm = list(PMType.keys())
    if 'ATM' in pm[0]:
        pm = pm[0].replace(' ATM','')

    
    if value['Surface']:

        if value['An_superficie']:
            # Para animación
            if 'Surface_anim_font' in memory:
                frame = [[sg.Text('Modifica el formato de la superficie animada.'), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo')],
                        [sg.Text('Tipo de fuente: ', size=(33,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value=memory['Surface_anim_font'],key='Font'), sg.Checkbox('Bold title',default=memory['Surface_anim_Bold'],key='Bold')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Contenido del eje X: ',size=(33,1)), sg.InputText(memory['Surface_anim_xlabel_cont'], key='xlabel_content', size=(24,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Surface_anim_xlabel_style'],key='Xstyle')],
                        [sg.Text('Contenido del eje Y: ',size=(33,1)), sg.InputText(memory['Surface_anim_ylabel_cont'], key='ylabel_content', size=(24,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Surface_anim_ylabel_style'],key='Ystyle')],
                        [sg.Text('Contenido del eje Z: ',size=(33,1)), sg.InputText(memory['Surface_anim_zlabel_cont'], key='zlabel_content', size=(24,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Surface_anim_zlabel_style'],key='Zstyle')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Tamaño de letra para el titulo: ',size=(33,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=memory['Surface_anim_title_size'],key='Title_size')],
                        [sg.Text('Tamaño de letra para el subtitulo: ',size=(33,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=memory['Surface_anim_subtitle_size'],key='Subtitle_size')],
                        [sg.Text('Tamaño de letra para los ejes: ',size=(33,1)), sg.Combo([8, 9, 10, 11, 12],default_value=memory['Surface_anim_label_size'],key='Label_size')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Tipo de marcador a mostrar: ',size=(33,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value=memory['Surface_anim_marker'],key='Marker')],
                        [sg.Text('Tipo de interpolación:',size=(33,1)), sg.Combo(['Cúbica', 'Lineal'],default_value=memory['Surface_anim_Interp'], key='Interp')],
                        [sg.Text('Ángulo polar', size=(33,1)), sg.Text('Ángulo azimutal', size=(30,1))],
                        [sg.Slider(orientation ='horizontal', key='Polar', range=(0,90), default_value=memory['Surface_anim_polar'], size=(25.7,20)),sg.Slider(orientation ='horizontal', key='Azimutal', range=(-180,180), default_value=memory['Surface_anim_azimutal'],size=(27,20))],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                        
                        [sg.Text('Tipo de fecha a visualizar: ',size=(33,1)), sg.Combo(['UTC', 'Local'], default_value=memory['Surface_anim_date'], key='DateType')],
                        [sg.Text('Nombre del gif resultante: ',size=(33,1)), sg.Input(memory['Surface_anim_filename'], key='Name', size=(30,1))],
                        [sg.Text('Selecciona donde guardar',size=(33,1)),sg.Input(memory['Surface_anim_folder'],size=(30,1),key='Surf_folder'),sg.FolderBrowse()],
                        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]

            else:
                frame = [[sg.Text('Modifica el formato de la superficie animada.'), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo')],
                        [sg.Text('Tipo de fuente: ', size=(33,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value='Times New Roman',key='Font'), sg.Checkbox('Bold title',default=False,key='Bold')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Contenido del eje X: ',size=(33,1)), sg.InputText('Carretera (m)', key='xlabel_content', size=(24,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Xstyle')],
                        [sg.Text('Contenido del eje Y: ',size=(33,1)), sg.InputText('Profundidad (m)', key='ylabel_content', size=(24,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Ystyle')],
                        [sg.Text('Contenido del eje Z: ',size=(33,1)), sg.InputText('ug/m3', key='zlabel_content', size=(24,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Zstyle')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Tamaño de letra para el titulo: ',size=(33,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=14,key='Title_size')],
                        [sg.Text('Tamaño de letra para el subtitulo: ',size=(33,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=12,key='Subtitle_size')],
                        [sg.Text('Tamaño de letra para los ejes: ',size=(33,1)), sg.Combo([8, 9, 10, 11, 12],default_value=11,key='Label_size')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Tipo de marcador a mostrar: ',size=(33,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                        [sg.Text('Tipo de interpolación:',size=(33,1)), sg.Combo(['Cúbica', 'Lineal'],default_value='Cúbica', key='Interp')],
                        [sg.Text('Ángulo polar', size=(33,1)), sg.Text('Ángulo azimutal', size=(30,1))],
                        [sg.Slider(orientation ='horizontal', key='Polar', range=(0,90), default_value=15, size=(25.7,20)),sg.Slider(orientation ='horizontal', key='Azimutal', range=(-180,180), default_value=-135,size=(27,20))],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Tipo de fecha a visualizar: ',size=(33,1)), sg.Combo(['UTC', 'Local'], default_value='UTC', key='DateType')],
                        [sg.Text('Nombre del gif resultante: ',size=(33,1)), sg.Input('Superficie.gif', key='Name', size=(30,1))],
                        [sg.Text('Selecciona donde guardar',size=(33,1)),sg.Input(size=(30,1),key='Surf_folder'),sg.FolderBrowse()],
                        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]

            layout = [[sg.Text('Animación de la superficie', font = font3, justification='center', expand_x=True)],
                    [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Column(frame, expand_y=True, scrollable=True, vertical_scroll_only=True)]]

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
            event, animation3d = window.read()

            if event in ('Exit', sg.WIN_CLOSED):
                shutdown(window)
            elif event != 'Average':
                return window, event, animation3d, lateral_avg, historico, memory

            # Guardamos en memoria los datos
            memory['Surface_anim_font'] = animation3d['Font'];                  memory['Surface_anim_Bold'] = animation3d['Bold']
            memory['Surface_anim_xlabel_cont'] = animation3d['xlabel_content']; memory['Surface_anim_xlabel_style'] = animation3d['Xstyle']
            memory['Surface_anim_ylabel_cont'] = animation3d['ylabel_content']; memory['Surface_anim_ylabel_style'] = animation3d['Ystyle']
            memory['Surface_anim_zlabel_cont'] = animation3d['zlabel_content']; memory['Surface_anim_zlabel_style'] = animation3d['Zstyle']

            memory['Surface_anim_title_size'] = animation3d['Title_size'];      memory['Surface_anim_subtitle_size'] = animation3d['Subtitle_size']
            memory['Surface_anim_label_size'] = animation3d['Label_size'];      memory['Surface_anim_marker'] = animation3d['Marker']
            memory['Surface_anim_polar'] = animation3d['Polar'];                memory['Surface_anim_azimutal'] = animation3d['Azimutal']
            memory['Surface_anim_filename'] = animation3d['Name'];              memory['Surface_anim_folder'] = animation3d['Surf_folder']
            memory['Surface_anim_date'] = animation3d['DateType'];              typedate = animation3d['DateType']
            memory['Surface_anim_Interp'] = animation3d['Interp']

            # Pasamos los datos a simbolos que entienda matplotlib
            animation3d['Marker'] = marker[animation3d['Marker']]

        else:
            # Para una figura estatica
            if 'Surface_est_font' in memory:
                frame = [[sg.Text('Modifica el formato de la superficie.',size=(29,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo')],
                        [sg.Text('Tipo de fuente: ', size=(29,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value=memory['Surface_est_font'],key='Font'), sg.Checkbox('Bold title',default=memory['Surface_est_Bold'],key='Bold')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Contenido del titulo: ',size=(29,1)), sg.InputText(memory['Surface_est_title_cont'], key='Title_content', size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Surface_est_title_style'],key='Titlestyle')],
                        [sg.Text('Contenido del subtitulo: ',size=(29,1)), sg.InputText(memory['Surface_est_subtitle_cont'], key='Subtitle_content',size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Surface_est_subtitle_style'],key='Substyle')],
                        [sg.Text('Contenido del eje X: ',size=(29,1)), sg.InputText(memory['Surface_est_xlabel_cont'], key='xlabel_content', size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Surface_est_xlabel_style'],key='Xstyle')],
                        [sg.Text('Contenido del eje Y: ',size=(29,1)), sg.InputText(memory['Surface_est_ylabel_cont'], key='ylabel_content', size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Surface_est_ylabel_style'],key='Ystyle')],
                        [sg.Text('Contenido del eje Z: ',size=(29,1)), sg.InputText(memory['Surface_est_zlabel_cont'], key='zlabel_content', size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Surface_est_zlabel_style'],key='Zstyle')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Tamaño de letra para el titulo: ',size=(29,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=memory['Surface_est_title_size'],key='Title_size')],
                        [sg.Text('Tamaño de letra para el subtitulo: ',size=(29,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=memory['Surface_est_subtitle_size'],key='Subtitle_size')],
                        [sg.Text('Tamaño de letra para los ejes: ',size=(29,1)), sg.Combo([8, 9, 10, 11, 12],default_value=memory['Surface_est_label_size'],key='Label_size')],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Tipo de marcador a mostrar: ',size=(29,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value=memory['Surface_est_marker'],key='Marker')],
                        [sg.Text('Tipo de interpolación:',size=(29,1)), sg.Combo(['Cúbica', 'Lineal'],default_value=memory['Surface_est_interp'], key='Interp')],
                        [sg.Text('Ángulo polar (grados)', size=(29,1)), sg.Text('Ángulo azimutal (grados)', size=(30,1))],
                        [sg.Slider(orientation ='horizontal', key='Polar', range=(0,90), default_value=memory['Surface_est_polar'], size=(22.6,20)),sg.Slider(orientation ='horizontal', key='Azimutal', range=(-180,180), default_value=memory['Surface_est_azimutal'],size=(22.6,20))],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],

                        [sg.Text('Tipo de fecha a visualizar: ',size=(29,1)), sg.Combo(['UTC', 'Local'], default_value=memory['Surface_est_date'], key='DateType')],
                        [sg.Text('Nombre de la imagen resultante: ',size=(29,1)), sg.Input(memory['Surface_est_filename'], key='Name', size=(30,1))],
                        [sg.Text('Selecciona donde guardar',size=(29,1)),sg.Input(memory['Surface_est_folder'], size=(30,1),key='Surf_folder'),sg.FolderBrowse()],
                        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]
            else:
                frame = [[sg.Text('Modifica el formato de la superficie.',size=(29,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo')],
                        [sg.Text('Tipo de fuente: ', size=(29,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value='Times New Roman',key='Font'), sg.Checkbox('Bold title',default=False,key='Bold')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Contenido del titulo: ',size=(29,1)), sg.InputText(f'Concentración {pm}', key='Title_content', size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Titlestyle')],
                        [sg.Text('Contenido del subtitulo: ',size=(29,1)), sg.InputText('Promedio desde XX hasta YY', key='Subtitle_content',size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Substyle')],
                        [sg.Text('Contenido del eje X: ',size=(29,1)), sg.InputText('Carretera (m)', key='xlabel_content',size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Xstyle')],
                        [sg.Text('Contenido del eje Y: ',size=(29,1)), sg.InputText('Profundidad (m)', key='ylabel_content', size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Ystyle')],
                        [sg.Text('Contenido del eje Z: ',size=(29,1)), sg.InputText('ug/m3', key='zlabel_content', size=(28,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Zstyle')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tamaño de letra para el titulo: ',size=(29,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=14,key='Title_size')],
                        [sg.Text('Tamaño de letra para el subtitulo: ',size=(29,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=12,key='Subtitle_size')],
                        [sg.Text('Tamaño de letra para los ejes: ',size=(29,1)), sg.Combo([8, 9, 10, 11, 12],default_value=11,key='Label_size')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tipo de marcador a mostrar: ',size=(29,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                        [sg.Text('Tipo de interpolación:',size=(29,1)), sg.Combo(['Cúbica', 'Lineal'],default_value='Cúbica', key='Interp')],
                        [sg.Text('Ángulo polar (grados)', size=(29,1)), sg.Text('Ángulo azimutal (grados)', size=(30,1))],
                        [sg.Slider(orientation ='horizontal', key='Polar', range=(0,90), default_value=15, size=(22.6,20)),sg.Slider(orientation ='horizontal', key='Azimutal', range=(-180,180), default_value=-135,size=(22.6,20))],
                        [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                        
                        [sg.Text('Tipo de fecha a visualizar: ',size=(29,1)), sg.Combo(['UTC', 'Local'], default_value='UTC', key='DateType')],
                        [sg.Text('Nombre de la imagen resultante: ',size=(29,1)), sg.Input('Superficie.png', key='Name', size=(30,1))],
                        [sg.Text('Selecciona donde guardar',size=(29,1)),sg.Input(size=(30,1),key='Surf_folder'),sg.FolderBrowse()],
                        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]
            
            layout = [[sg.Text('Superficie', font = font3, justification='center', expand_x=True)],
                    [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Column(frame, expand_y=True, scrollable=True, vertical_scroll_only=True)]]

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
            event, animation3d = window.read()

            if event in ('Exit', sg.WIN_CLOSED):
                shutdown(window)
            elif event != 'Average':
                return window, event, animation3d, lateral_avg, historico, memory

            # Guardamos los datos en memoria
            memory['Surface_est_font'] = animation3d['Font'];                       memory['Surface_est_Bold'] = animation3d['Bold']
            memory['Surface_est_title_cont'] = animation3d['Title_content'];        memory['Surface_est_title_style'] = animation3d['Titlestyle'],
            memory['Surface_est_subtitle_cont'] = animation3d['Subtitle_content'];  memory['Surface_est_subtitle_style'] = animation3d['Substyle'],
            memory['Surface_est_xlabel_cont'] = animation3d['xlabel_content'];      memory['Surface_est_xlabel_style'] = animation3d['Xstyle']
            memory['Surface_est_ylabel_cont'] = animation3d['ylabel_content'];      memory['Surface_est_ylabel_style'] = animation3d['Ystyle']
            memory['Surface_est_zlabel_cont'] = animation3d['zlabel_content'];      memory['Surface_est_zlabel_style'] = animation3d['Zstyle']

            memory['Surface_est_title_size'] = animation3d['Title_size'];           memory['Surface_est_subtitle_size'] = animation3d['Subtitle_size']
            memory['Surface_est_label_size'] = animation3d['Label_size'];           memory['Surface_est_marker'] = animation3d['Marker']
            memory['Surface_est_polar'] = animation3d['Polar'];                     memory['Surface_est_azimutal'] = animation3d['Azimutal']
            memory['Surface_est_filename'] = animation3d['Name'];                   memory['Surface_est_folder'] = animation3d['Surf_folder']
            memory['Surface_est_date'] = animation3d['DateType'];                   typedate = animation3d['DateType']
            memory['Surface_est_interp'] = animation3d['Interp']

            # Pasamos los datos a simbolos que entienda matplotlib
            animation3d['Marker'] = marker[animation3d['Marker']]
    
    if value['LateralAvg']:

        if value['An_lateral']:
            # Para animación
            if 'Lateral_anim_Fondo' in memory:
                frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                        [sg.Text('Formato de la gráfica lateral animada.',size=(30,1)), sg.Checkbox('Fondo transparente: ', default=memory['Lateral_anim_Fondo'], key='Fondo'), sg.Checkbox('Recorrer el eje x: ', default=memory['Lateral_anim_recorrer'], key='Recorrer')],
                        [sg.Text('Tipo de fuente: ', size=(30,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value=memory['Lateral_anim_font'],key='Font'), sg.Checkbox('Bold title',default=memory['Lateral_anim_Bold'],key='Bold')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Contenido del eje X: ',size=(30,1)), sg.InputText(memory['Lateral_anim_xlabel_cont'], key='xlabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Lateral_anim_xlabel_style'],key='Xstyle')],
                        [sg.Text('Contenido del eje Y: ',size=(30,1)), sg.InputText(memory['Lateral_anim_ylabel_cont'], key='ylabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Lateral_anim_ylabel_style'],key='Ystyle')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=memory['Lateral_anim_title_size'],key='Title_size')],
                        [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=memory['Lateral_anim_subtitle_size'],key='Subtitle_size')],
                        [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=memory['Lateral_anim_label_size'],key='Label_size')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value=memory['Lateral_anim_marker'],key='Marker')],
                        [sg.Text('Tamaño de marcador: ',size=(30,1)), sg.Combo([30, 35, 40, 45, 50, 55],default_value=memory['Lateral_anim_marker_size'],key='MarkerSize')],
                        [sg.Text('Color del marcador: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value=memory['Lateral_anim_marker_color'],key='MarkerColor')], 
                        [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value=memory['Lateral_anim_line_style'],key='LineStyle')],
                        [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=memory['Lateral_anim_line_size'],key='LineSize')],
                        [sg.Text('Color de linea: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value=memory['Lateral_anim_line_color'],key='LineColor')], 
                        [sg.Text('Posición de la leyenda: ',size=(30,1)), sg.Combo(['best','upper right','upper left','lower right','lower left','upper center','lower center','center right','center left'],default_value=memory['Lateral_anim_legend'],key='Legend')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],
                        
                        [sg.Text('Tipo de interpolación:',size=(30,1)), sg.Combo(['Cuadrática', 'Lineal'],default_value=memory['Lateral_anim_interp'], key='Interp')],
                        [sg.Text('Tipo de fecha a visualizar: ',size=(30,1)), sg.Combo(['UTC', 'Local'], default_value=memory['Lateral_anim_date'], key='DateType')],
                        [sg.Text('Nombre del gif resultante: ',size=(30,1)), sg.Input(memory['Lateral_anim_filename'], key='Name')],
                        [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(memory['Lateral_anim_folder'],key='Lateral_folder',size=(30,1)),sg.FolderBrowse()],
                        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]

            else:
                frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                        [sg.Text('Formato de la gráfica lateral animada.',size=(30,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo'), sg.Checkbox('Recorrer el eje x: ', default=False, key='Recorrer')],
                        [sg.Text('Tipo de fuente: ', size=(30,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value='Times New Roman',key='Font'), sg.Checkbox('Bold title',default=False,key='Bold')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Contenido del eje X: ',size=(30,1)), sg.InputText('profundidad (m)', key='xlabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Xstyle')],
                        [sg.Text('Contenido del eje Y: ',size=(30,1)), sg.InputText('Valor promedio (ug/m3)', key='ylabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Ystyle')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=16,key='Title_size')],
                        [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=14,key='Subtitle_size')],
                        [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=12,key='Label_size')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                        [sg.Text('Tamaño de marcador: ',size=(30,1)), sg.Combo([30, 35, 40, 45, 50, 55],default_value=40,key='MarkerSize')],
                        [sg.Text('Color del marcador: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Rojo',key='MarkerColor')], 
                        [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value='Dashed --',key='LineStyle')],
                        [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=2,key='LineSize')],
                        [sg.Text('Color de linea: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Azul',key='LineColor')], 
                        [sg.Text('Posición de la leyenda: ',size=(30,1)), sg.Combo(['best','upper right','upper left','lower right','lower left','upper center','lower center','center right','center left'],default_value='upper right',key='Legend')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tipo de interpolación:',size=(30,1)), sg.Combo(['Cuadrática', 'Lineal'],default_value='Cuadrática', key='Interp')],
                        [sg.Text('Tipo de fecha a visualizar: ',size=(30,1)), sg.Combo(['UTC', 'Local'], default_value='UTC', key='DateType')],
                        [sg.Text('Nombre del gif resultante: ',size=(30,1)), sg.Input('Lateral.gif', key='Name')],
                        [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(key='Lateral_folder',size=(30,1)),sg.FolderBrowse()],
                        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]

            layout = [[sg.Text('Promedio lateral', font = font3, justification='center', expand_x=True)],
                    [sg.Column(frame, expand_y=True, scrollable=True, vertical_scroll_only=True)]]

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
            event, lateral_avg = window.read()

            if event in ('Exit', sg.WIN_CLOSED):
                shutdown(window)
            elif event != 'Average':
                return window, event, animation3d, lateral_avg, historico, memory

            # Guardamos en memoria
            memory['Lateral_anim_Fondo'] = lateral_avg['Fondo'];                memory['Lateral_anim_recorrer'] = lateral_avg['Recorrer']
            memory['Lateral_anim_font'] = lateral_avg['Font'];                  memory['Lateral_anim_Bold'] = lateral_avg['Bold']

            memory['Lateral_anim_xlabel_cont'] = lateral_avg['xlabel_content']; memory['Lateral_anim_xlabel_style'] = lateral_avg['Xstyle']
            memory['Lateral_anim_ylabel_cont'] = lateral_avg['ylabel_content']; memory['Lateral_anim_ylabel_style'] = lateral_avg['Ystyle']

            memory['Lateral_anim_title_size'] = lateral_avg['Title_size'];      memory['Lateral_anim_subtitle_size'] = lateral_avg['Subtitle_size']
            memory['Lateral_anim_label_size'] = lateral_avg['Label_size'];      memory['Lateral_anim_marker'] = lateral_avg['Marker']
            memory['Lateral_anim_marker_size']= lateral_avg['MarkerSize'];      memory['Lateral_anim_marker_color'] = lateral_avg['MarkerColor']

            memory['Lateral_anim_line_style'] = lateral_avg['LineStyle'];       memory['Lateral_anim_line_size'] = lateral_avg['LineSize']
            memory['Lateral_anim_line_color'] = lateral_avg['LineColor'];       memory['Lateral_anim_legend'] = lateral_avg['Legend']
            
            memory['Lateral_anim_filename'] = lateral_avg['Name'];              memory['Lateral_anim_folder'] = lateral_avg['Lateral_folder']
            memory['Lateral_anim_date'] = lateral_avg['DateType'];              typedate = lateral_avg['DateType']
            memory['Lateral_anim_interp'] = lateral_avg['Interp']

            # Pasamos los datos a simbolos que entienda matplotlib
            lateral_avg['Marker'] = marker[lateral_avg['Marker']]
            lateral_avg['MarkerColor'] = color[lateral_avg['MarkerColor']]
            lateral_avg['LineStyle'] = lines[lateral_avg['LineStyle']]
            lateral_avg['LineColor'] = color[lateral_avg['LineColor']]

        else:
            # Para una figura estatica
            if 'Lateral_est_title_cont' in memory:
                frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                        [sg.Text('Modifica el formato de la gráfica lateral.',size=(30,1)), sg.Checkbox('Fondo transparente: ', default=memory['Lateral_est_Fondo'], key='Fondo'), sg.Checkbox('Recorrer el eje x: ', default=memory['Lateral_est_recorrer'], key='Recorrer')],
                        [sg.Text('Tipo de fuente: ', size=(30,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value=memory['Lateral_est_font'],key='Font'), sg.Checkbox('Bold title',default=memory['Lateral_est_Bold'],key='Bold')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Contenido del titulo: ',size=(30,1)), sg.InputText(memory['Lateral_est_title_cont'], key='Title_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Lateral_est_title_style'],key='Titlestyle')],
                        [sg.Text('Contenido del subtitulo: ',size=(30,1)), sg.InputText(memory['Lateral_est_subtitle_cont'], key='Subtitle_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Lateral_est_subtitle_style'],key='Substyle')],
                        [sg.Text('Contenido del eje X: ',size=(30,1)), sg.InputText(memory['Lateral_est_xlabel_cont'], key='xlabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Lateral_est_xlabel_style'],key='Xstyle')],
                        [sg.Text('Contenido del eje Y: ',size=(30,1)), sg.InputText(memory['Lateral_est_ylabel_cont'], key='ylabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Lateral_est_ylabel_style'],key='Ystyle')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=memory['Lateral_est_title_size'],key='Title_size')],
                        [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=memory['Lateral_est_subtitle_size'],key='Subtitle_size')],
                        [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=memory['Lateral_est_label_size'],key='Label_size')],
                        [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value=memory['Lateral_est_marker'],key='Marker')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tamaño de marcador: ',size=(30,1)), sg.Combo([30, 35, 40, 45, 50, 55],default_value=memory['Lateral_est_marker_size'],key='MarkerSize')],
                        [sg.Text('Color del marcador: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value=memory['Lateral_est_marker_color'],key='MarkerColor')], 
                        [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value=memory['Lateral_est_line_style'],key='LineStyle')],
                        [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=memory['Lateral_est_line_size'],key='LineSize')],
                        [sg.Text('Color de linea: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value=memory['Lateral_est_line_color'],key='LineColor')],
                        [sg.Text('Posición de la leyenda: ',size=(30,1)), sg.Combo(['best','upper right','upper left','lower right','lower left','upper center','lower center','center right','center left'],default_value=memory['Lateral_est_legend'],key='Legend')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tipo de interpolación:',size=(30,1)), sg.Combo(['Cuadrática', 'Lineal'],default_value=memory['Lateral_est_interp'], key='Interp')],
                        [sg.Text('Tipo de fecha a visualizar: ',size=(30,1)), sg.Combo(['UTC', 'Local'], default_value=memory['Lateral_est_date'], key='DateType')],
                        [sg.Text('Nombre de la imagen resultante: ',size=(30,1)), sg.Input(memory['Lateral_est_filename'], key='Name', size=(30,1))],
                        [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(memory['Lateral_est_folder'],key='Lateral_folder',size=(30,1)),sg.FolderBrowse()],
                        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]

            else:
                frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                        [sg.Text('Modifica el formato de la gráfica lateral.',size=(30,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo'), sg.Checkbox('Recorrer el eje x: ', default=False, key='Recorrer')],
                        [sg.Text('Tipo de fuente: ', size=(30,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value='Times New Roman',key='Font'), sg.Checkbox('Bold title',default=False,key='Bold')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Contenido del titulo: ',size=(30,1)), sg.InputText(f'Concentración {pm}', key='Title_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Titlestyle')],
                        [sg.Text('Contenido del subtitulo: ',size=(30,1)), sg.InputText('Promedio desde XX hasta YY', key='Subtitle_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Substyle')],
                        [sg.Text('Contenido del eje X: ',size=(30,1)), sg.InputText('profundidad (m)', key='xlabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Xstyle')],
                        [sg.Text('Contenido del eje Y: ',size=(30,1)), sg.InputText('Valor promedio (ug/m3)', key='ylabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Ystyle')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=16,key='Title_size')],
                        [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=14,key='Subtitle_size')],
                        [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=12,key='Label_size')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                        [sg.Text('Tamaño de marcador: ',size=(30,1)), sg.Combo([30, 35, 40, 45, 50, 55],default_value=40,key='MarkerSize')],
                        [sg.Text('Color del marcador: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Rojo',key='MarkerColor')], 
                        [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value='Dashed --',key='LineStyle')],
                        [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=2,key='LineSize')],
                        [sg.Text('Color de linea: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Azul',key='LineColor')], 
                        [sg.Text('Posición de la leyenda: ',size=(30,1)), sg.Combo(['best','upper right','upper left','lower right','lower left','upper center','lower center','center right','center left'],default_value='upper right',key='Legend')],
                        [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                        [sg.Text('Tipo de interpolación:',size=(30,1)), sg.Combo(['Cuadrática', 'Lineal'],default_value='Cuadrática', key='Interp')],
                        [sg.Text('Tipo de fecha a visualizar: ',size=(30,1)), sg.Combo(['UTC', 'Local'], default_value='UTC', key='DateType')],
                        [sg.Text('Nombre de la imagen resultante: ',size=(30,1)), sg.Input('Lateral.png', key='Name', size=(30,1))],
                        [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(key='Lateral_folder',size=(30,1)),sg.FolderBrowse()],
                        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]

            layout = [[sg.Text('Promedio lateral', font = font3, justification='center', expand_x=True)],
                    [sg.Column(frame, expand_y=True, scrollable=True, vertical_scroll_only=True)]]

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
            event, lateral_avg = window.read()

            if event in ('Exit', sg.WIN_CLOSED):
                shutdown(window)
            elif event != 'Average':
                window, event, animation3d, lateral_avg, historico, memory

            # Guardamos en memoria
            memory['Lateral_est_Fondo'] = lateral_avg['Fondo'];                     memory['Lateral_est_recorrer'] = lateral_avg['Recorrer']
            memory['Lateral_est_font'] = lateral_avg['Font'];                       memory['Lateral_est_Bold'] = lateral_avg['Bold']

            memory['Lateral_est_title_cont'] = lateral_avg['Title_content'];        memory['Lateral_est_title_style'] = lateral_avg['Titlestyle']
            memory['Lateral_est_subtitle_cont'] = lateral_avg['Subtitle_content'];  memory['Lateral_est_subtitle_style'] = lateral_avg['Substyle']
            memory['Lateral_est_xlabel_cont'] = lateral_avg['xlabel_content'];      memory['Lateral_est_xlabel_style'] = lateral_avg['Xstyle']
            memory['Lateral_est_ylabel_cont'] = lateral_avg['ylabel_content'];      memory['Lateral_est_ylabel_style'] = lateral_avg['Ystyle']

            memory['Lateral_est_title_size'] = lateral_avg['Title_size'];           memory['Lateral_est_subtitle_size'] = lateral_avg['Subtitle_size']
            memory['Lateral_est_label_size'] = lateral_avg['Label_size'];           memory['Lateral_est_marker'] = lateral_avg['Marker']
            memory['Lateral_est_marker_size']= lateral_avg['MarkerSize'];           memory['Lateral_est_marker_color'] = lateral_avg['MarkerColor']

            memory['Lateral_est_line_style'] = lateral_avg['LineStyle'];            memory['Lateral_est_line_size'] = lateral_avg['LineSize']
            memory['Lateral_est_line_color'] = lateral_avg['LineColor'];            memory['Lateral_est_legend'] = lateral_avg['Legend']
            memory['Lateral_est_filename'] = lateral_avg['Name'];                   memory['Lateral_est_folder'] = lateral_avg['Lateral_folder']
            memory['Lateral_est_date'] = lateral_avg['DateType'];                   typedate = lateral_avg['DateType']
            memory['Lateral_est_interp'] = lateral_avg['Interp']

            # Pasamos los datos a simbolos que entienda matplotlib
            lateral_avg['Marker'] = marker[lateral_avg['Marker']]
            lateral_avg['MarkerColor'] = color[lateral_avg['MarkerColor']]
            lateral_avg['LineStyle'] = lines[lateral_avg['LineStyle']]
            lateral_avg['LineColor'] = color[lateral_avg['LineColor']]
    
    if value['Historico']:
        # Para una figura estatica
        if 'Historico_est_title_cont' in memory:
            frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Modifica el formato del histórico.',size=(30,1)), sg.Checkbox('Fondo transparente: ', default=memory['Historico_est_Fondo'], key='Fondo')],
                    [sg.Text('Tipo de fuente: ', size=(30,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value=memory['Historico_est_font'],key='Font'), sg.Checkbox('Bold title',default=memory['Historico_est_Bold'],key='Bold')],
                    [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                    [sg.Text('Contenido del titulo: ',size=(30,1)), sg.InputText(memory['Historico_est_title_cont'], key='Title_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Historico_est_title_style'],key='Titlestyle')],
                    [sg.Text('Contenido del subtitulo: ',size=(30,1)), sg.InputText(f'Promedios de {d*60} minutos', key='Subtitle_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Historico_est_subtitle_style'],key='Substyle')],
                    [sg.Text('Contenido del eje X: ',size=(30,1)), sg.InputText(memory['Historico_est_xlabel_cont'], key='xlabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Historico_est_xlabel_style'],key='Xstyle')],
                    [sg.Text('Contenido del eje Y: ',size=(30,1)), sg.InputText(memory['Historico_est_ylabel_cont'], key='ylabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value=memory['Historico_est_ylabel_style'],key='Ystyle')],
                    [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                    [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=memory['Historico_est_title_size'],key='Title_size')],
                    [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=memory['Historico_est_subtitle_size'],key='Subtitle_size')],
                    [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=memory['Historico_est_label_size'],key='Label_size')],
                    [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                    [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value=memory['Historico_est_marker'],key='Marker')],
                    [sg.Text('Tamaño de marcador: ',size=(30,1)), sg.Combo([30, 35, 40, 45, 50, 55],default_value=memory['Historico_est_marker_size'],key='MarkerSize')], 
                    [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value=memory['Historico_est_line_style'],key='LineStyle')],
                    [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=memory['Historico_est_line_size'],key='LineSize')],
                    [sg.Text('Posición de la leyenda: ',size=(30,1)), sg.Combo(['best','upper right','upper left','lower right','lower left','upper center','lower center','center right','center left'],default_value=memory['Historico_est_legend'],key='Legend')],
                    [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                    [sg.Text('Tipo de interpolación:',size=(30,1)), sg.Combo(['Cuadrática', 'Lineal'],default_value=memory['Historico_est_interp'], key='Interp')],
                    [sg.Text('Tipo de fecha a visualizar: ',size=(30,1)), sg.Combo(['UTC', 'Local'], default_value=memory['Historico_est_date'], key='DateType')],
                    [sg.Text('Nombre de la imagen resultante: ',size=(30,1)), sg.Input(memory['Historico_est_filename'], key='Name', size=(30,1))],
                    [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(memory['Historico_est_folder'],key='Historico_folder',size=(30,1)),sg.FolderBrowse()],
                    [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]

        else:
            frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Modifica el formato del histórico.',size=(30,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo')],
                    [sg.Text('Tipo de fuente: ', size=(30,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value='Times New Roman',key='Font'), sg.Checkbox('Bold title',default=False,key='Bold')],
                    [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                    [sg.Text('Contenido del titulo: ',size=(30,1)), sg.InputText(f'Concentración {pm}', key='Title_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Titlestyle')],
                    [sg.Text('Contenido del subtitulo: ',size=(30,1)), sg.InputText(f'Promedios de {d*60} minutos', key='Subtitle_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Substyle')],
                    [sg.Text('Contenido del eje X: ',size=(30,1)), sg.InputText('Tiempo', key='xlabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Xstyle')],
                    [sg.Text('Contenido del eje Y: ',size=(30,1)), sg.InputText('Valor promedio (ug/m3)', key='ylabel_content',size=(27,1)), sg.Combo(['normal', 'italic', 'oblique'], default_value='normal',key='Ystyle')],
                    [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                    [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=16,key='Title_size')],
                    [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=14,key='Subtitle_size')],
                    [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=12,key='Label_size')],
                    [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                    [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                    [sg.Text('Tamaño de marcador: ',size=(30,1)), sg.Combo([40, 45, 50, 55, 60, 65],default_value=50,key='MarkerSize')],
                    [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value='Dashed --',key='LineStyle')],
                    [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=2,key='LineSize')],
                    [sg.Text('Posición de la leyenda: ',size=(30,1)), sg.Combo(['best','upper right','upper left','lower right','lower left','upper center','lower center','center right','center left'],default_value='upper right',key='Legend')],
                    [sg.Text('',size=(1,1),font=('Times New Roman',1))],

                    [sg.Text('Tipo de interpolación:',size=(30,1)), sg.Combo(['Cuadrática', 'Lineal'],default_value='Cuadrática', key='Interp')],
                    [sg.Text('Tipo de fecha a visualizar: ',size=(30,1)), sg.Combo(['UTC', 'Local'], default_value='UTC', key='DateType')],
                    [sg.Text('Nombre de la imagen resultante: ',size=(30,1)), sg.Input('Historic.png', key='Name', size=(30,1))],
                    [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(key='Historico_folder',size=(30,1)),sg.FolderBrowse()],
                    [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]

        layout = [[sg.Text('Promedios históricos', font = font3, justification='center', expand_x=True)],
                [sg.Column(frame, expand_y=True, scrollable=True, vertical_scroll_only=True)]]

        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
        event, historico = window.read()

        if event in ('Exit', sg.WIN_CLOSED):
            shutdown(window)
        elif event != 'Average':
            window, event, animation3d, lateral_avg, historico, memory

        # Guardamos en memoria
        memory['Historico_est_Fondo'] = historico['Fondo']
        memory['Historico_est_font'] = historico['Font'];                       memory['Historico_est_Bold'] = historico['Bold']

        memory['Historico_est_title_cont'] = historico['Title_content'];        memory['Historico_est_title_style'] = historico['Titlestyle']
        memory['Historico_est_subtitle_cont'] = historico['Subtitle_content'];  memory['Historico_est_subtitle_style'] = historico['Substyle']
        memory['Historico_est_xlabel_cont'] = historico['xlabel_content'];      memory['Historico_est_xlabel_style'] = historico['Xstyle']
        memory['Historico_est_ylabel_cont'] = historico['ylabel_content'];      memory['Historico_est_ylabel_style'] = historico['Ystyle']

        memory['Historico_est_title_size'] = historico['Title_size'];           memory['Historico_est_subtitle_size'] = historico['Subtitle_size']
        memory['Historico_est_label_size'] = historico['Label_size'];           memory['Historico_est_marker'] = historico['Marker']
        memory['Historico_est_marker_size']= historico['MarkerSize'];           memory['Historico_est_legend'] = historico['Legend']

        memory['Historico_est_line_style'] = historico['LineStyle'];            memory['Historico_est_line_size'] = historico['LineSize']
        memory['Historico_est_filename'] = historico['Name'];                   memory['Historico_est_folder'] = historico['Historico_folder']
        memory['Historico_est_date'] = historico['DateType'];                   typedate = historico['DateType']
        memory['Historico_est_interp'] = historico['Interp']

        # Pasamos los datos a simbolos que entienda matplotlib
        historico['Marker'] = marker[historico['Marker']]
        historico['LineStyle'] = lines[historico['LineStyle']]

    return window, event, animation3d, lateral_avg, historico, memory, typedate

def data_average(data, minimum, maximum, anim, value, PMType, begin, final, type_date):
    begin = datetime.strptime(begin, '%Y-%m-%d %H:%M').replace(tzinfo=tz.tzutc())
    final = datetime.strptime(final, '%Y-%m-%d %H:%M').replace(tzinfo=tz.tzutc())

    PMType = PA_Onl[list(PMType.keys())[0]]
    first_start = max(minimum.values())
    final_end = min(maximum.values())

    if first_start < begin:
        first_start = begin
    
    if final_end > final:
        final_end = final

    dif = final_end - first_start
    seconds = dif.seconds + dif.days*24*60*60

    ### El usuario pudo pedir una animada y una estatica, por lo que pueden haber mas de dos grupos de datos finales..
    new_data_anim = limites_anim = new_data_est = limites_est = []

    if (value['Surface'] and value['An_superficie']) or (value['LateralAvg'] and value['An_lateral'] or value['Historico']):
        delta = float(anim['delta'])
        new_data_anim, limites_anim, PMType = average(data, delta, PMType, first_start, final_end, seconds, type_date)

    if (value['Surface'] and value['Es_superficie']) or (value['LateralAvg'] and value['Es_lateral']):
        delta = seconds/3600
        new_data_est, limites_est, PMType = average(data, delta, PMType, first_start, final_end, seconds, type_date)

    return new_data_anim, limites_anim, new_data_est, limites_est, PMType

def average(data, delta, PMType, first_start, final_end, seconds, type_date):
    new_data = {}
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
            if type_date == 'Local':
                prom = [start.astimezone(tz.tzlocal()).strftime("%Y/%m/%d, %H:%M") + ' (hora de inicio)']
            else:
                prom = [start.strftime("%Y/%m/%d, %H:%M") + ' (hora de inicio)']
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

def graph(window, x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, PMType, indx, limites, graph_selection, value_anim, styles, selection, carretera_lateral, rows_sen):
    PMType = [PMType]
    if selection == 'Surface':
        Func.surface(x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, graph_selection, value_anim, PMType, indx, limites, styles, carretera_lateral)
    
    if selection == 'LateralAvg':
        Func.lateral_avg(x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, graph_selection, value_anim, PMType, indx, limites, styles, rows_sen)

    if selection == 'Historico':
        Func.historico(y_axis, z_axis, columns, rows, row_dist, graph_selection, PMType, indx, limites, styles, rows_sen)
    
    window, event = gui_final(window)

    return window, event

def gui_final(window):
    # Preguntamos si queremos modificar algo de las graficas, regresamos al inicio de esta función.
    layout = [[sg.Text('Si requiere modificar algo de las graficas de nuevo.',font=font3)],
                [sg.Text('Favor de seleccionar "Repetir graficado"',font=font3)],
                [sg.Button('Repetir graficado'), sg.Button('Finalizar programa')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, value = window.read()

    if event == 'Repetir graficado':
        event = 'Tipo_de_grafico'

    return window, event

def error_grafica(window):
    # Se pide que ingrese datos validos
    # Indicar que existio un error, probable por que falto un dato en el formato de la grafica o en los datos.
    layout = [[sg.Text('Error al graficar!', font=font3)],
            [sg.Text('Probablemente fallo por un dato faltante en el formato o en los datos csv')],
            [sg.Button('Return',key='Tipo_de_grafico'), sg.Button('Exit')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
    event, value = window.read()
    if event in ('Exit', sg.WIN_CLOSED):
        window.close()
        sys.exit()
    
    return window, event

def shutdown(window):
    window.close()
    sys.exit()