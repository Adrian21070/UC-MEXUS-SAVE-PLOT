import functions as Func
import PySimpleGUI as sg
import sys
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

# Zonas horarias
Local_H = tz.tzlocal()
Utc = tz.gettz('UTC')

# Diseño de la interfaz. 
sg.theme('DarkAmber')

# Columnas de interfaz reutilizables.
col1=[[sg.Text('Selecciona los datos a analizar')],
        [sg.Checkbox('PM 1.0 CF', default=False, key="PM 1.0 CF")], 
        [sg.Checkbox('PM 2.5 CF', default=False, key ="PM 2.5 CF")],
        [sg.Checkbox('PM 10.0 CF', default=False, key ="PM 10.0 CF")],
        [sg.Checkbox('PM 2.5 ATM', default=False, key ="PM 2.5 ATM")]]

def gui_creation():
    # Creacion de la interfaz
    layout = [[sg.Text('Seleccione de donde desea sacar los datos', font = font)],
           [sg.Button('Online'),sg.Button('Archivo CSV'),
            sg.Button('Exit',key='Exit')]]

    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()
    
    return window, event

def data_type(window):
    # Se pregunta el tipo de dato que quiere analizar.
    layout = [col1, [sg.Button('Next', key='Sensor_info'), sg.Button('Return',key='GuiCreation'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
    return window, event, value

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

    return event, value

def date_hour(window):
    layout = [[sg.Text('Selección de fecha y hora de las mediciones',font=font)],
                [sg.CalendarButton('Dia de inicio de la medición',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='Start')],
                [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(key='Start_hour')],
                [sg.Text('')],
                [sg.CalendarButton('Dia del fin de la medición',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='End')],
                [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(key='End_hour')],
                [sg.Button("Next"), sg.Button('Return',key='SensorDistribution'),sg.Button('Exit')]]
    
                # No se puede escoger una fecha en el futuro, ya que no existen datos.

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
    return event, value


def shutdown(window):
    window.close()
    sys.exit()