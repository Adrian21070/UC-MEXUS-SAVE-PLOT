import functions as Func
import PySimpleGUI as sg
import sys
import os
from pytz import utc
from datetime import datetime
from dateutil import tz



# Diccionarios utiles para los nombres de columnas y datos

# Diccionario para seleccionar el tipo de material
# particulado a graficar a partir de los archivos CSV
PM_Dict={"PM 1.0 CF": "pm1_0_cf_1",	
         "PM 2.5 CF": "pm2_5_cf_1",	
         "PM 10.0 CF": "pm10_0_cf_1",	
         "PM 1.0 ATM": "pm1_0_atm",	
         "PM 2.5 ATM": "pm2_5_atm",	
         "PM 10.0 ATM" : "pm10_0_atm"}

# Diccionario para seleccionar el tipo de material 
# particulado a graficar a partir de los datos en el canal
# principal de thingspeak. 
PA_Dict={"PM 1.0 CF": "field1",	
         "PM 2.5 CF": "field2",	
         "PM 10.0 CF": "field3",
         "PM 2.5 ATM": "field8"}

# Sirve para la identificación en pandas
PA_Onl = {"PM 1.0 ATM": "PM1.0_ATM_ug/m3", "PM 2.5 ATM": "PM2.5_ATM_ug/m3",
        "PM 10.0 ATM": "PM10.0_ATM_ug/m3", "PM 1.0 CF": "PM1.0_CF1_ug/m3",
        "PM 2.5 CF": "PM2.5_CF1_ug/m3", "PM 10.0 CF": "PM10.0_CF1_ug/m3",
        "PM 1.0 ATM B": "PM1.0_ATM_B_ug/m3", "PM 2.5 ATM B": "PM2.5_ATM_B_ug/m3",
        "PM 10.0 ATM B": "PM10.0_ATM_B_ug/m3", "PM 1.0 CF B": "PM1.0_CF1_B_ug/m3",
        "PM 2.5 CF B": "PM2.5_CF1_B_ug/m3", "PM 10.0 CF B": "PM10.0_CF1_B_ug/m3"}

# Fuentes para la interfaz
font = ('Times New Roman', 16)
font2 = ('Times New Roman', 12)
font3 = ('Times New Roman', 14)

# Zonas horarias
Local_H = tz.tzlocal()
Utc = tz.gettz('UTC')

# Diseño de la interfaz. 
sg.theme('DarkAmber')

# Columnas de interfaz reutilizables.
col1=[[sg.Text('Selecciona los datos a analizar')],
        [sg.Radio('Canal A', "Canal", default=True, key='Channel_A'), sg.Radio('Canal B', "Canal", default=False, key='Channel_B')],
        [sg.Radio('PM 1.0 ATM', 'PM', default=False, key="PM 1.0 ATM"), sg.Radio('PM 2.5 ATM', 'PM', default=False, key="PM 2.5 ATM")],
        [sg.Radio('PM 10.0 ATM', 'PM', default=False, key="PM 10.0 ATM"), sg.Radio('PM 1.0 CF', 'PM', default=False, key="PM 1.0 CF")],
        [sg.Radio('PM 2.5 CF', 'PM', default=False, key="PM 2.5 CF"), sg.Radio('PM 10.0 CF', 'PM', default=False, key="PM 10.0 CF")]]

def save_or_graph():
    layout = [[sg.Text('Favor de seleccionar lo que desea realizar:')],
                [sg.Button('Guardar datos',key='Save_data'), sg.Button('Graficar',key='Plot'), sg.Button('Exit')]]
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
    return window, event
    
def gui_graph_creation(window):
    # Creacion de la interfaz
    layout = [[sg.Text('Seleccione de donde desea sacar los datos', font = font)],
           [sg.Button('Online'),sg.Button('Archivo CSV', key='CSV'),
            sg.Button('Exit',key='Exit')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()
    
    return window, event

def saving_data(window):
    # Primero solicita el número de sensores a guardar e intervalo de tiempo
    # de la medición.
    layout = [[sg.Text('Datos acerca del número de sensores y el intervalo de medición')],
                [sg.Text('Numero de sensores:'), sg.Input(key='NumSen')],
                [sg.CalendarButton('Dia de inicio de la medición',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='Start')],
                [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(key='Start_hour')],
                [sg.CalendarButton('Dia del fin de la medición',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='End')],
                [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(key='End_hour')],
                [sg.Button('Continue'), sg.Button('Return'), sg.Button('Exit')]]
    
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()
    
    if 'Exit' in event:
        shutdown()

    elif 'Return' in event:
        event = 'init'
        return

    numsen = int(value['NumSen'])
    start = value['Start'] + '%20' + value['Start_hour'] + ':00'
    end = value['End'] + '%20' + value['End_hour'] + ':00'

    # Ahora, solicito los numeros de los sensores en campo.
    if event == 'Continue':
        chain = list(range(1,numsen+1))

        lay = []
        layout = []
        
        r = 0
        c = 0

        for ii in chain:
            if ii%9 == 0:
                r += 1
                c = 0
                layout.append(lay)
                lay = []
            lay.append(sg.Input(ii,key=f'{r},{c}', size=(5,1)))
            c += 1
        if lay:
            layout.append(lay)
            lay = []

        lay = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
                [sg.Frame('Disposición de los sensores', layout)],
                [sg.Button('Next',key='Next'),sg.Button('Return',key='Init'),sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', lay, font = font2, size=(720,480))
        event, indx = window.read()
        
    # Extrae los datos de online.
    if event == 'Next':
        x_axis, y_axis, z_axis, minimum_dates, maximum_dates = Func.Data_extraction(1, 1, 1, 1, PA_Dict[ii], indx, start, end)

        pass

def data_type(window):
    # Se pregunta el tipo de dato que quiere analizar.
    layout = [col1, [sg.Button('Next', key='Sensor_info'), sg.Button('Return',key='GuiCreation'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)

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
                [sg.Button("Next",key='SensorDistribution'), sg.Button('Return',key='TypeData'), sg.Button('Exit')]]
            
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
    return window, event, value

def distribution(window,num_sen,rows,columns):
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
                [sg.Button('Next',key='Date_hour'),sg.Button('Return',key='Sensor_info'),sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)

    return window, event, value

def date_hour(window, key=0):
    layout = [[sg.Text('Selección de fecha y hora de las mediciones',font=font)],
                [sg.CalendarButton('Dia de inicio de la medición',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='Start')],
                [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(key='Start_hour')],
                [sg.Text('')],
                [sg.CalendarButton('Dia del fin de la medición',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='End')],
                [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(key='End_hour')],
                [sg.Button("Next",key='Extraction'), sg.Button('Return',key='SensorDistribution'),sg.Button('Exit')]]
    
                # No se puede escoger una fecha en el futuro, ya que no existen datos.

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

def extraction(value,rows,columns,lateral_length,depth_length,indx,start,end):
    # Tipos de datos a sacar
    holes = {}
    PMType = []
    for ii in PA_Dict.keys():
        if value[ii]:
            # Para cada tipo de dato se sacara la data de todos los sensores
            PMType.append(PA_Onl[ii])

            x_axis, y_axis, z_axis, minimum_dates, maximum_dates = Func.Data_extraction(rows, columns, lateral_length, depth_length, PA_Dict[ii], indx, start, end)

            # Se comprueba si existen huecos
            # Probablemente esta sea la función más tardada e ineficiente de todas...
            holes, num_csv = Func.huecos(z_axis, indx)

    if num_csv:
        it = 1
    else:
        it = 0

    return x_axis, y_axis, z_axis, minimum_dates, maximum_dates, holes, num_csv, it, PMType

def holes_warning(window,holes,num_csv):
    
    # Notificar con una ventana que existen huecos
    layout = [[sg.Text('Existen sensores con huecos de información',font=font), sg.Text(f'(YYYY-MM-DD HH-MM-SS)')],
                [sg.Text('Los sensores son:', font = font3)]]
    for ii in num_csv.keys():
        k = list(holes[ii].keys())
        v = list(holes[ii].values())

        k = [m.replace(tzinfo=Local_H) for m in k] #Lo pongo en local, no utc
        v = [m.replace(tzinfo=Local_H) for m in v] #Lo pongo en local, no utc

        # Transformo a string los elementos de tiempo.
        #holes_text = [[sg.Text(f'{ii} presenta un hueco desde')]]
        holes_text = []

        for jj in range(len(k)):
            utc_k = k[jj].astimezone(Utc).strftime('%Y-%m-%d, %X')
            utc_v = v[jj].astimezone(Utc).strftime('%Y-%m-%d, %X')
            k2 = k[jj].strftime('%Y-%m-%d, %X')
            v2 = v[jj].strftime('%Y-%m-%d, %X')

            holes_text.append([sg.Text(f'{k2}  hasta  {v2}, timezone: Local.')])
            holes_text.append([sg.Text(f'{utc_k}  hasta  {utc_v}, timezone: UTC')])
        layout.append([sg.Frame(f'{ii} presenta un hueco desde',holes_text)])
    layout.append([sg.Button('Solucionar errores',key='Fix_errors')])
    lay = [[sg.Column(layout, scrollable=True, vertical_scroll_only=True,expand_y=True, expand_x=True)]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', lay, font = font2, size=(720,480))
    event, value = window.read()

    return window, event

def csv_online(window, num_holes_per_sensor, holes):
    # Solicita archivos csv
    layout = [[sg.Text('Introduce los archivos solicitados con el nombre del tipo SXX_YYYYMMDD:', font = font)]]
    for ii in num_holes_per_sensor.keys():
        k = list(holes[ii].keys())
        v = list(holes[ii].values())
        days = []
        for jj in range(len(k)):
            day = k[jj].day
            day2 = v[jj].day
            if (day in days):
                pass
            else:
                days.append(day)
            if (day2 in days):
                pass
            else:
                days.append(day2)
        lay = []
        for jj in days:
            lay.append([sg.Text(f'Archivo del dia {jj}'), sg.Input(), sg.FileBrowse()])
                    
        layout.append([sg.Frame(f'{ii}', lay)])
    
    layout.append([sg.Button('Fix data'), sg.Button('Exit')])
    lay = [[sg.Column(layout, scrollable=True, vertical_scroll_only=True,expand_y=True, expand_x=True)]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', lay, font=font2, size=(720,480))
    event, value = window.read()
    
    if 'Exit' in event:
        shutdown(window)

    # Selecciono unicamente las direcciones no repetidas.
    val = [value[a] for a in value.keys() if ('Browse' in str(a))]

    # Lo transformo en un diccionario, para facilitar ciertas cosas posteriores
    value = {}
    iter = 0
    for ii in num_holes_per_sensor.keys():
        value[ii] = []
        for jj in range(len(val)):
            if jj == num_holes_per_sensor[ii]:
                break
            value[ii].append(val[iter])
            iter += 1
    val = []

    return window, value

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

    data = Func.open_csv(value)
    data_sorted = {}
    indx_sort = sorted(data.items())

    for ii in indx_sort:
        data_sorted[ii[0]] = ii[1]
        
    return window, event, data_sorted

def fixing(value, z_axis, PMType, holes, minimum_dates, maximum_dates, key):
    csv_data = Func.csv_extraction(value, key=1)

    z_axis2 = Func.Fix_data(z_axis, csv_data, PMType, holes, key)
    # Se ajusta la data para que inicien y terminen igual los sensores, adecua la función.
    delta = 0.5
    z_axis2, limites = Func.Matrix_adjustment(minimum_dates, maximum_dates, z_axis2, delta)

    # Notificar al usuario si existieron problemas o todo bien???
    # Aquí comprueba si existen errores, como? no se...
    error = False
    
    if error == True:
        z_axis2 = []
        return z_axis, limites, error
    else:
        return z_axis2, limites, error

def graph_domain(window, x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, PMType, indx, limites):
    # Se pregunta que graficas quiere realizar
    layout = [[sg.Text('Favor de seleccionar que graficas desea obtener')],
            [sg.Checkbox('Animación 3D (superficie)', default=False, key='Animation3D')],
            [sg.Checkbox('Lateral average', default=False, key='LateralAvg')],
            [sg.Checkbox('Registro historico de filas', default=False, key='Historico')],
            [sg.Text('Tiempo de duración animación (Min.)', size =(25, 1)), sg.InputText(key='Length')],
            [sg.Button('Graficar'), sg.Button('Exit')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if event == 'Graficar':
        Func.graphs(x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, value, PMType, indx, limites)
        
        # Preguntamos si queremos modificar algo de las graficas, regresamos al inicio de esta función.
        layout = [[sg.Text('Si requiere modificar algo de las graficas de nuevo.')],
                    [sg.Text('Favor de seleccionar "Repetir graficado"')],
                    [sg.Button('Repetir graficado'), sg.Button('No volver a graficar')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
        event, value = window.read()
        if event == 'Repetir graficado':
            event = 'Graphs'

        return window, event, value

    elif event == 'Exit':
        shutdown(window)

def shutdown(window):
    window.close()
    sys.exit()