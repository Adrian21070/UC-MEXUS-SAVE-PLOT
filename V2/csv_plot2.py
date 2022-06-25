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

    layout = [[sg.Text('Seleccione la carpeta donde se encuentras los archivos csv', font=font3)],
            [sg.Text(f'Ubicación de la carpeta: '), sg.Input(), sg.FolderBrowse()],
            [sg.Button('Extraer',key='TypeData'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
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
    layout = [col1, [sg.Button('Next', key='Sensor_info'), sg.Button('Return',key='Extraction'), sg.Button('Exit')]]
    # Puedo hacerlo frame y poner todo en el centro mas estetico
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
                [sg.Text(f'Cuenta con {len(indx)} sensores a disposición.')],
                [sg.Text('Favor de seleccionar el número de columnas y filas utilizadas en el campo.\n')],
                [sg.Text('Num. Columnas de Sensores', size =(25, 1)), sg.InputText(key='Columns')],
                [sg.Text('Num. Filas de Sensores', size =(25, 1)), sg.InputText(key='Rows')],
                [sg.Text('Distancia entre Columnas', size =(25, 1)), sg.InputText(key='Col_dis')],
                [sg.Text('Distancia entre Filas', size =(25, 1)), sg.InputText(key='Row_dis')],
                [sg.Text('Distancia respecto a la carretera', size=(25,1)), sg.InputText(key='Y0')],
                [sg.Text('Distancia lateral a otras vias', size=(25,1)), sg.InputText(key='X0')],
                [sg.Button("Next",key='SensorDistribution'), sg.Button('Return',key='TypeData'), sg.Button('Exit')]]
            
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)

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
    lay = []
    layout = []
    it = 0
    
    try:
        for i in range(rows):
            for j in range(columns):
                lay.append(sg.Input(chain[it], key=f'{chain[it]}',size=(5,1)))
                #coordenadas[f'{i},{j}'] = chain[it]
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
        return window, event, value, indx, False

    if it < len(num_sen):
        event = 'Sensor_info'
        return window, event, num_sen, False

    frame = [[sg.Frame('Disposicion de los sensores', layout, element_justification='center', expand_x=True)]]
    
    del layout, lay

    layout = [[sg.Text('Carretera', justification='center', font=('Times New Roman', 24), expand_x=True)],
            [sg.Column(frame, scrollable=True, expand_y=True, justification='center')],
        #    [sg.Column(frame, scrollable=True, justification='center')],
            [sg.Text('Escribe el número de identificación de los sensores en los recuadros (Ejemplo: 1, 6, 23).')],
            [sg.Text('En el recuadro se despliegan todos los sensores disponibles, si no requiere verificar')],
            [sg.Text('alguno de ellos, deje en blanco su recuadro. Tambien puede cambiarlos de posición.')],
            [sg.Button('Continue',key='Coordenadas'),sg.Button('Return',key='Sensor_info'),sg.Button('Exit')],
            [sg.Text('\n')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, indx = window.read()

    if 'Exit' in event:
        shutdown(window)
    if event != 'Coordenadas':
        return window, event, indx, False

    # Extraigo los valores dados por el usuario y quito los repetidos.
    result = []
    indx = list(indx.values())

    # Quito los espacios vacios.
    if '' in indx:
        indx.remove('')

    for item in indx:
        if item not in result:
            result.append(item)

    indx = result
    del result
    
    # Hago una prueba para evitar que el usuario rompa el código.
    try:
        num = []
        # Los paso de string a enteros.
        for jj in range(len(indx)):
            num.append(int(indx[jj]))

        # Compruebo que los numeros esten dentro de los numeros dados por el usuario o del 1 a 30.
        llave = False

        for ii in indx:
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
            return window, event, num_sen, True

        return window, event, indx, False

    except:
        layout = [[sg.Text('Favor de introducir únicamente números enteros que estén')],
                [sg.Text('entre 1 y 30, o entre los números de los archivos csv cargados.')],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=('Times New Roman', 18), size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()

        return window, event, num_sen, True

def coordenadas(window, rows, row_dist, columns, col_dist, x0, y0, indx):
    # Calculo de X y Y
    x = np.array(list(range(0,columns)))*col_dist + x0
    y = np.array(list(range(0,rows)))*row_dist + y0
    x_axis = []
    y_axis = []

    # Matriz de coordenadas
    layout = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
                [sg.Frame('Coordenadas de los sensores', [[sg.Input(f'{col},{row}',
                key=(col,row), size=(6,1)) for col in x]
                for row in y])],
                [sg.Button('Continue',key='Date_hour'),sg.Button('Return',key='SensorDistribution'),sg.Button('Exit')]]
    
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    elif event != 'Date_hour':
        return window, event, indx, 0, 0

    try:
        for ii in value.values():
            ii = eval(ii)
            x_axis.append(ii[0])
            y_axis.append(ii[1])

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

    new_indx = dict(zip(list(value.values()), indx))

    """ Esta de mas al parecer
    for jj in new_indx.keys():
        num = int(new_indx[jj])
        if num > 99:
            continue
        elif num >= 10 and num <= 99:
            new_indx[jj] = f'0{new_indx[jj]}'
        else:
            new_indx[jj] = f'00{new_indx[jj]}'
    """

    return window, event, new_indx, x_axis, y_axis

def type_graph(window):
    # Se pregunta que graficas quiere realizar
    layout = [[sg.Text('Favor de seleccionar que graficas desea obtener', font=font3)],
            [sg.Checkbox('Superficie', default=False, key='Surface'), sg.Radio('Animación', "Superficie", default=True, key='An_superficie'), sg.Radio('Estática', "Superficie", default=False, key='Es_superficie')],
            [sg.Checkbox('Lateral average', default=False, key='LateralAvg'), sg.Radio('Animación', "Lateral", default=True, key='An_lateral'), sg.Radio('Estática', "Lateral", default=False, key='Es_lateral')],
            [sg.Checkbox('Registro historico de filas', default=False, key='Historico')],
            [sg.Button('Continue',key='Date_hour'), sg.Button('Return',key='Sensor_info'), sg.Button('Exit')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)


    if (value['Surface'] and value['An_superficie']) or (value['LateralAvg'] and value['An_lateral']):
        layout = [[sg.Text('Datos para la animación\n', font=font3, justification='center', expand_x=True)],
                [sg.Text('Tiempo de duración animación (Min.)', size =(35, 1)), sg.InputText(key='Length')],
                [sg.Text('Promedios de los datos en horas (1=60min)', size =(35, 1)), sg.InputText(key='delta')],
                [sg.Button('Continue',key='Date_hour'), sg.Button('Return', key='Tipo_de_grafico'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
        event, value_anim = window.read()

        if 'Exit' in event:
            shutdown(window)
        
        return window, value, event, value_anim

    if (value['Surface'] and value['Es_superficie']) or (value['LateralAvg'] and value['Es_lateral']) or (value['Historico']):
        
        pass

    return window, value, event, False


def date_hour(window, maximum, minimum, key=0):
    start = min(minimum.values()).strftime('%Y-%m-%d')
    end = max(maximum.values()).strftime('%Y-%m-%d')
    start_hr = min(minimum.values()).strftime('%H:%M')
    end_hr = max(maximum.values()).strftime('%H:%M')

    layout = [[sg.Text('Selección de fecha y hora de las mediciones a mostrar\n',font=font3, justification='center', expand_x=True)],
                [sg.CalendarButton('Dia de inicio',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(start,key='Start')],
                [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(start_hr,key='Start_hour')],
                [sg.Text('')],
                [sg.CalendarButton('Dia del final',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(end,key='End')],
                [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(end_hr,key='End_hour')],
                [sg.Button("Continue",key='Graph'), sg.Button('Return',key='Tipo_de_grafico'),sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    elif event != 'Graph':
        return window, event, value, 0

    if key == 1:
        # Paso las fechas a datetime y saco los dias entre ambas fechas en utc.
        start = datetime.strptime(value['Start'], '%Y-%m-%d').replace(tzinfo=tz.tzutc())
        end = datetime.strptime(value['End'], '%Y-%m-%d').replace(tzinfo=tz.tzutc())
        days = [ii for ii in range(start.day, end.day+1, 1)]
        return window, event, value, days

    else:
        return window, event, value, 0

def graph_domain(window, value, value_anim, PMType):
    ### Se realizan ventanas para preguntar cosas sobre el diseño de las imagenes.
    ### Tipo de linea, colores, titulos, ticks, tamaño ...

    marker = {'Circle':'o', 'Diamond':'D', 'Triangle_up':'^', 'Triangle_down':'v', 'Star':'*', 'X':'X', 'No marker':'No marker'}
    color = {'Azul':'b', 'Rojo':'r', 'Verde':'g', 'Cyan':'c', 'Magenta':'m', 'Amarillo':'y', 'Negro':'k'}
    lines = {'Solid -':'-', 'Dashed --':'--', 'Dashdot -.':'-.', 'Dotted :':':', 'No line':'No line'}

    animation3d = []
    lateral_avg = []
    historico = []

    if value['Surface']:

        if value['An_superficie']:
            # Para animación
            layout = [[sg.Text('Animación de la superficie', font = font3, justification='center', expand_x=True)],
                    [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Modifica el formato de la superficie animada.')],
                    [sg.Text('Tamaño de letra para el titulo: ',size=(33,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=14,key='Title_size')],
                    [sg.Text('Tamaño de letra para el subtitulo: ',size=(33,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=12,key='Subtitle_size')],
                    [sg.Text('Tamaño de letra para los ejes: ',size=(33,1)), sg.Combo([8, 9, 10, 11, 12],default_value=11,key='Label_size')],
                    [sg.Text('Tipo de marcador a mostrar: ',size=(33,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                    [sg.Text('Ángulo polar', size=(33,1)), sg.Text('Ángulo azimutal', size=(30,1))],
                    [sg.Slider(orientation ='horizontal', key='Polar', range=(0,90), default_value=15, size=(25.7,20)),sg.Slider(orientation ='horizontal', key='Azimutal', range=(-180,180), default_value=-135,size=(27,20))],
                    [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Nombre del gif resultante: ',size=(33,1)), sg.Input('Superficie.gif', key='Name')],
                    [sg.Text('Selecciona donde guardar',size=(33,1)),sg.Input(size=(30,1),key='Surf_folder'),sg.FolderBrowse()],
                    [sg.Button('Continue'), sg.Button('Exit')]]
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
            event, animation3d = window.read()

            if 'Exit' in event:
                shutdown(window)
            elif event != 'Graph':
                return 

            # Pasamos los datos a simbolos que entienda matplotlib
            animation3d['Marker'] = marker[animation3d['Marker']]

        else:
            # Para una figura estatica
            layout = [[sg.Text('Superficie', font = font3, justification='center', expand_x=True)],
                    [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Modifica el formato de la superficie.',size=(29,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo')],
                    [sg.Text('Contenido del titulo: ',size=(29,1)), sg.InputText('Concentración PM 2.5', key='Title_content')],
                    [sg.Text('Contenido del subtitulo: ',size=(29,1)), sg.InputText('Promedio desde XX hasta YY', key='Subtitle_content')],
                    [sg.Text('Tamaño de letra para el titulo: ',size=(29,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=14,key='Title_size')],
                    [sg.Text('Tamaño de letra para el subtitulo: ',size=(29,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=12,key='Subtitle_size')],
                    [sg.Text('Tamaño de letra para los ejes: ',size=(29,1)), sg.Combo([8, 9, 10, 11, 12],default_value=11,key='Label_size')],
                    [sg.Text('Tipo de marcador a mostrar: ',size=(29,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                    [sg.Text('Ángulo polar (grados)', size=(29,1)), sg.Text('Ángulo azimutal (grados)', size=(30,1))],
                    [sg.Slider(orientation ='horizontal', key='Polar', range=(0,90), default_value=15, size=(22.6,20)),sg.Slider(orientation ='horizontal', key='Azimutal', range=(-180,180), default_value=-135,size=(22.6,20))],
                    [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Nombre de la imagen resultante: ',size=(29,1)), sg.Input('Superficie.png', key='Name')],
                    [sg.Text('Selecciona donde guardar',size=(29,1)),sg.Input(size=(30,1),key='Surf_folder'),sg.FolderBrowse()],
                    [sg.Button('Continue'), sg.Button('Exit')]]

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
            event, animation3d = window.read()

            if 'Exit' in event:
                shutdown(window)
            elif event != 'Graph':
                return 

            # Pasamos los datos a simbolos que entienda matplotlib
            animation3d['Marker'] = marker[animation3d['Marker']]
    
    if value['LateralAvg']:

        if value['An_lateral']:
            # Para animación
            frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Modifica el formato de la gráfica lateral.',size=(30,1))],
                    [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=16,key='Title_size')],
                    [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=14,key='Subtitle_size')],
                    [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=12,key='Label_size')],
                    [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                    [sg.Text('Color del marcador: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Rojo',key='MarkerColor')], 
                    [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value='Dashed --',key='LineStyle')],
                    [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=2,key='LineSize')],
                    [sg.Text('Color de linea: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Azul',key='LineColor')], 
                    [sg.Text('Nombre del gif resultante: ',size=(30,1)), sg.Input('Lateral.gif', key='Name')],
                    [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(key='Lateral_folder',size=(30,1)),sg.FolderBrowse()],
                    [sg.Button('Continue'), sg.Button('Exit')]]

            layout = [[sg.Text('Promedio lateral', font = font3, justification='center', expand_x=True)],
                    [sg.Column(frame, expand_y=True)]]

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
            event, lateral_avg = window.read()

            if 'Exit' in event:
                shutdown(window)
            elif event != 'Graph':
                return 

            # Pasamos los datos a simbolos que entienda matplotlib
            lateral_avg['Marker'] = marker[lateral_avg['Marker']]
            lateral_avg['MarkerColor'] = color[lateral_avg['MarkerColor']]
            lateral_avg['LineStyle'] = lines[lateral_avg['LineStyle']]
            lateral_avg['LineColor'] = color[lateral_avg['LineColor']]

        else:
            # Para una figura estatica
            frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Modifica el formato de la gráfica lateral.',size=(30,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo')],
                    [sg.Text('Contenido del titulo: ',size=(30,1)), sg.InputText('Concentración PM 2.5', key='Title_content')],
                    [sg.Text('Contenido del subtitulo: ',size=(30,1)), sg.InputText('Promedio desde XX hasta YY', key='Subtitle_content')],
                    [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=16,key='Title_size')],
                    [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=14,key='Subtitle_size')],
                    [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=12,key='Label_size')],
                    [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                    [sg.Text('Color del marcador: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Rojo',key='MarkerColor')], 
                    [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value='Dashed --',key='LineStyle')],
                    [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=2,key='LineSize')],
                    [sg.Text('Color de linea: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Azul',key='LineColor')], 
                    [sg.Text('Nombre de la imagen resultante: ',size=(30,1)), sg.Input('Lateral.png', key='Name')],
                    [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(key='Lateral_folder',size=(30,1)),sg.FolderBrowse()],
                    [sg.Button('Continue'), sg.Button('Exit')]]

            layout = [[sg.Text('Promedio lateral', font = font3, justification='center', expand_x=True)],
                    [sg.Column(frame, expand_y=True, scrollable=True, vertical_scroll_only=True)]]

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
            event, lateral_avg = window.read()

            if 'Exit' in event:
                shutdown(window)
            elif event != 'Graph':
                return 

            # Pasamos los datos a simbolos que entienda matplotlib
            lateral_avg['Marker'] = marker[lateral_avg['Marker']]
            lateral_avg['MarkerColor'] = color[lateral_avg['MarkerColor']]
            lateral_avg['LineStyle'] = lines[lateral_avg['LineStyle']]
            lateral_avg['LineColor'] = color[lateral_avg['LineColor']]
    
    if value['Historico']:
        pass
    

    """
    Que debo regresar??? Sigo pensando esto.
    """

    return window, value, animation3d, lateral_avg, historico

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

def graph(window, x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, PMType, indx, limites, value, animation3d, lateral_avg, historico):
    
    PMType = [PMType]
    Func.graphs(x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, value, PMType, indx, limites, value['delta'], animation3d, lateral_avg, historico)
    
    # Preguntamos si queremos modificar algo de las graficas, regresamos al inicio de esta función.
    layout = [[sg.Text('Si requiere modificar algo de las graficas de nuevo.')],
                [sg.Text('Favor de seleccionar "Repetir graficado"')],
                [sg.Button('Repetir graficado'), sg.Button('Finalizar programa')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
    event, value = window.read()

    if event == 'Repetir graficado':
        event = 'Graph'
        return window, event, value

    else:
        shutdown(window)

def shutdown(window):
    window.close()
    sys.exit()