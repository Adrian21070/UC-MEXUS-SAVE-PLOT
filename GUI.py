'''
----------------------------------------------------------
    @file: GUI.py
    @date: Oct 2021
    @date_modif: Dec 22, 2021
    @author: Raul Dominguez
    @e-mail: a01065986@itesm.mx
    @brief: Script to create a Graphic User Interface (GUI), call the functions from AvgFunctions.py and plot 
            the measurements of PurpleAir sensors.
----------------------------------------------------------
'''

#Librerias requeridas
import PySimpleGUI as sg
import AvgFunctions as AF
import functions as F
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import numpy as np

'''
Links interesantes sobre librerias utilizadas para hacer la GUI: 
    - https://stackoverflow.com/questions/59500558/how-to-display-different-layouts-based-on-button-clicks-in-pysimple-gui-persis
    - https://stackoverflow.com/questions/63725995/how-to-display-files-in-folder-when-using-pysimplegui-filebrowse-function
'''


#Linea para poder graficar en la interfaz de usuario
#matplotlib.use("TkAgg")

#Diccionario para seleccionar el tipo de mateiral particulado a graficar a partir de los archivos CSV
PM_Dict={"PM 1.0 CF": "pm1_0_cf_1",	
         "PM 2.5 CF": "pm2_5_cf_1",	
         "PM 10.0 CF": "pm10_0_cf_1",	
         "PM 1.0 ATM": "pm1_0_atm",	
         "PM 2.5 ATM": "pm2_5_atm",	
         "PM 10.0 ATM" : "pm10_0_atm"}

'''
Diccionario para seleccionar el tipo de mateiral particulado a graficar a partir de los datos en el canal
principal de thingspeak. 

Nota: Es importante que para obtener el resto de los datos tambien se debe obtener la info del canal secundario 
de thingspeak
'''
PA_Dict={"PM 1.0 CF": "field1",	
         "PM 2.5 CF": "field2",	
         "PM 10.0 CF": "field3",
         "PM 2.5 ATM": "field8"}

font = ('Times New Roman', 16)
font2 = ('Times New Roman', 12)
# Interfaz incial, donde se solicitan datos 
sg.theme('DarkAmber')
# Creacion de las diferentes paginas de la interfaz de usuario
# Interfaz Inicial
layout1 = [[sg.Text('Seleccione de donde desea sacar los datos', font = font)],
           [sg.Button('Online'),sg.Button('Archivo CSV'),
            sg.Button('Exit',key='Exit')]]

# Interfaz para seleccionar con los datos CSV
layout2 = [[sg.Text('Seleccione que desea hacer con el archivo CSV', font=font)],
           [sg.Button('Promedio'),sg.Button("Animación"),
            sg.Button('Exit',key='Exit')]]

# Interfaz para hacer graficas promedio a partir de un archivo CSV
layout3 = [[sg.Text('Datos para el promedio (Todos se deben llenar con numeros enteros!)',font=font)],
            [sg.Text('Num. de Sensores', size =(22, 1)), sg.InputText(key='NumSen')],
            [sg.Text('Num. Columnas de Sensores', size =(22, 1)), sg.InputText(key='Cols')],
            [sg.Text('Num. Filas de Sensores', size =(22, 1)), sg.InputText(key='Rows')],
            [sg.Text('Distancia entre Columnas', size =(22, 1)), sg.InputText(key='LC')],
            [sg.Text('Distancia entre Filas', size =(22, 1)), sg.InputText(key='LR')],
            [sg.Text('Hora de Inicio (24hrs)', size =(22, 1)), sg.InputText(key='Hora')],
            [sg.Text('Tiempo Monitoreo (Tiempo par en Min.)', size =(28, 1)), sg.InputText(key='Mins')],
            [sg.Text('Selecciona Folder con Datos'),sg.Input(), sg.FolderBrowse('Folder')],
            [sg.Text('Selecciona PM'),sg.Combo(['PM 1.0 CF', 'PM 2.5 CF', 'PM 10.0 CF', 'PM 1.0 ATM', 'PM 2.5 ATM', 'PM 10.0 ATM'], key='DDMPCSV')],
            [sg.Button("Graficar Promedio CSV"),sg.Button("Gráfica Lateral"),
             sg.Button('Exit', key='Exit')]]

# Interfaz para hacer animaciones a partir de un archivo CSV
layout4 = [[sg.Text('Datos para la animación (Todos se deben llenar con numeros enteros!)',font=font)],
            [sg.Text('Num. de Sensores', size =(22, 1)), sg.InputText(key='NumSenACSV')],
            [sg.Text('Num. Columnas de Sensores', size =(22, 1)), sg.InputText(key='ColsACSV')],
            [sg.Text('Num. Filas de Sensores', size =(22, 1)), sg.InputText(key='RowsACSV')],
            [sg.Text('Distancia entre Columnas', size =(22, 1)), sg.InputText(key='LCACSV')],
            [sg.Text('Distancia entre Filas', size =(22, 1)), sg.InputText(key='LRACSV')],
            [sg.Text('Hora de Inicio (24hrs)', size =(22, 1)), sg.InputText(key='HoraACSV')],
            [sg.Text('Tiempo Monitoreo (Tiempo par en Min.)', size =(28, 1)), sg.InputText(key='MinsACSV')],
            [sg.Text('Tiempo Duración Animación (Min.)', size =(28, 1)), sg.InputText(key='AniTime')],
            [sg.Text('Concentración de Material Particulado')],
            [sg.Text('Selecciona Folder con Datos'),sg.Input(), sg.FolderBrowse('Carpeta')],
            [sg.Text('Selecciona PM'),sg.Combo(['PM 1.0 CF', 'PM 2.5 CF', 'PM 10.0 CF', 'PM 1.0 ATM', 'PM 2.5 ATM', 'PM 10.0 ATM'], key='DDMACSV')],
            [sg.Button("Gráficar Animación CSV"),sg.Button('Exit', key='Exit',font=font2)]]

# Interfaz para seleccionar que hacer con los datos de PurpleAir
layout5 = [[sg.Text('Seleccione que desea hacer los datos de PurpleAir',font=font)],
           [sg.Button('Promedio Online'),sg.Button("Animación Online"),sg.Button('Exit', key='Exit')]]

# Interfaz para hacer una animacion a partir de los datos de PurpleAir
layout6_exp = [[sg.Text('Datos acerca del número de sensores y su disposición',font=font)],
            [sg.Text('Num. de Sensores', size =(25, 1)), sg.InputText(key='NumSenAPA')],
            [sg.Text('Num. Columnas de Sensores', size =(25, 1)), sg.InputText(key='ColsAPA')],
            [sg.Text('Num. Filas de Sensores', size =(25, 1)), sg.InputText(key='RowsAPA')],
            [sg.Text('Distancia entre Columnas', size =(25, 1)), sg.InputText(key='LCAPA')],
            [sg.Text('Distancia entre Filas', size =(25, 1)), sg.InputText(key='LRAPA')],
            [sg.Text('Tiempo de duración animación (Min.)', size =(25, 1)), sg.InputText(key='AniTimePA')],
            [sg.Text('Concentración de Material Particulado')],
            [sg.Text('Selecciona PM'),sg.Combo(['PM 1.0 CF', 'PM 2.5 CF', 'PM 10.0 CF', 'PM 2.5 ATM'], key='DDMAPA')],
            [sg.Button("Next"), sg.Button('Exit', key='Exit')]]

# Interfaz para hacer graficas promedio a partir de PurpleAir
layout7 = [[sg.Text('Datos para el promedio (Todos se deben llenar con numeros enteros!)',font=font)],
            [sg.Text('Num. de Sensores', size =(22, 1)), sg.InputText(key='NumSenPPA')],
            [sg.Text('Num. Columnas de Sensores', size =(22, 1)), sg.InputText(key='ColsPPA')],
            [sg.Text('Num. Filas de Sensores', size =(22, 1)), sg.InputText(key='RowsPPA')],
            [sg.Text('Distancia entre Columnas', size =(22, 1)), sg.InputText(key='LCPPA')],
            [sg.Text('Distancia entre Filas', size =(22, 1)), sg.InputText(key='LRPPA')],
            [sg.Text('Tiempo Monitoreo (Tiempo par en Min.)', size =(28, 1)), sg.InputText(key='MinsPasadosP')],
            [sg.Text('Selecciona PM'),sg.Combo(['PM 1.0 CF', 'PM 2.5 CF', 'PM 10.0 CF', 'PM 2.5 ATM'], key='DDMPPA')],
            [sg.Button("Gráfica Promedio PurpleAir"),sg.Button("Gráfica Lateral"),sg.Button('Exit', key='Exit')]]

layout9 = [[sg.Text('Selección de fecha y hora de las mediciones',font=font)],
            [sg.CalendarButton('Dia de inicio de la medición',target='-IN-', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='-IN-')],
            [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(key='Start_data')],
            [sg.CalendarButton('Dia del fin de la medición',target='-IN2-', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='-IN2-')],
            [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(key='End_data')],
            [sg.Button("Next"), sg.Button('Exit', key='Exit')]]

# Definicion de la GUI, estableciendo que pagina se mostrara y cuales estan desactivadas.
layout = [[sg.Column(layout1, key='-COL1-',justification='center'), sg.Column(layout2, visible=False, key='-COL2-',justification='center'), 
           sg.Column(layout3, visible=False, key='-COL3-',justification='center'),sg.Column(layout4, visible=False, key='-COL4-',justification='center'),
           sg.Column(layout5, visible=False, key='-COL5-',justification='center'),sg.Column(layout6_exp, visible=False, key='-COL6-',justification='center'),
           sg.Column(layout7, visible=False, key='-COL7-',justification='center'),sg.Column(layout9, visible=False, key='-COL9-',justification='center')]]

# Creacion de la ventana que contendra la GUI
window = sg.Window('Proyecto UCMEXUS', layout, font = font2)

"""
Notas para el futuro: 

Rediseña la interfaz, intenta hacerla modular,
es decir, online, csv generalos en dos ventanas separadas, no todo en una.
Esto optimiza los if, ya que habran dos principales y no entrara en los menores.
Tambien, si es posible, genera diversos window con cada cosa, promedio lateral, animación, etc
Todo esto lo hara más mantenible.

Pero cuidado... Los valores que obtengas con values deben ser guardados o añadirlos para evitar
perdida de información. Tambien intenta optimizar las funciones para solo tener las necesarias.


Ahora, solo falta observar cosas de la interpolación y las demas graficas fuera de la animación
ya que esta fue terminada. Pero falta adaptar las demas opciones para que puedan obtener los datos
con fecha, es casi un copia y pega. 

Si se pudiese crear una función que obtenga los datos para que
en las funciones principales no ocupen tanto codigo. Reutiliza codigo!!!

Mejora las graficas y animación esteticamente hablando.

Ya por extra, estaria bien modificar las apariciones de las ventanas y sus tamaños, esto no es forzoso
"""

 # Pagina visible inicialmente
layout = 1
while True:
    # Lectura de los componentes de la ventana
    event, values = window.read()
    # Ejecucion de evento en caso de que se oprima un boton en la GUI
    if event[-1].isnumeric():
        event = event[:-1]
    """if event == sg.WINDOW_CLOSED or event[0:4] == 'Exit':
        break"""
    if event in (sg.WIN_CLOSED, "Exit"):
       break

    if event == 'Promedio':
        # Se desactiva la pagina activa
        window[f'-COL{layout}-'].update(visible=False)
        '''Se define la nueva pagina que debe estar activa, el numero corresponde al orden en el que se 
        encuentran ordenadas las paginas en la definicion de layout en la linea 103'''
        layout = 3
        # Se activa una nueva ventana
        window[f'-COL{layout}-'].update(visible=True)

    elif event == 'Promedio Online':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 7
        window[f'-COL{layout}-'].update(visible=True)

    elif event == 'Animación':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 4
        window[f'-COL{layout}-'].update(visible=True)

    elif event == 'Archivo CSV':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 2
        window[f'-COL{layout}-'].update(visible=True)

    elif event == 'Online':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 5
        window[f'-COL{layout}-'].update(visible=True)

    elif event == 'Animación Online':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 6
        window[f'-COL{layout}-'].update(visible=True)

    elif event == 'Next':
        # Se crea un nuevo layout a partir de los datos dados por el usuario.
        
        chain = list(range(1,int(values['NumSenAPA'])+1))
        coordenadas = {}
        it = 0
        for i in range(int(values['RowsAPA'])):
            for j  in range(int(values['ColsAPA'])):
                coordenadas[f'{i},{j}'] = chain[it]
                it += 1  
        layout8 = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
                [sg.Frame('Disposición de los sensores', [[sg.Input(coordenadas[f'{row},{col}'],
                key=f'{row},{col}', size=(5,1)) for col in range(int(values['ColsAPA']))]
                for row in range(int(values['RowsAPA']))],font=font2)],
                [sg.Button('Submit', font=('Times New Roman',12)),sg.Button('Exit', font=('Times New Roman',12))]]

        window[f'-COL{layout}-'].update(visible=False)
        layout = 9
        window[f'-COL{layout}-'].update(visible=True)

        event, values = window.read()
        # Se copian los valores anteriores, para no perderlos
        init_values = values

        if event == sg.WINDOW_CLOSED or event[0:4] == 'Exit':
            break
        window.close()
        
        # Se crea una nueva ventana con el layout8 creado a partir de la anterior
        window = sg.Window('Proyecto UCMEXUS', layout8, font=font2)
    
    elif event == 'Submit':
        ### Se puede mandar a una función en otro archivo para tener un main más limpio...
        ### Se puede mandar a una función en otro archivo para tener un main más limpio...
        ### Se puede mandar a una función en otro archivo para tener un main más limpio...

        # Se dan los datos a la función que preparara los datos para graficar.
        # Checa que si los datos de hora dados en la interfaz, checa si
        # unicamente te dan una hora, ej: 14, en lugar de 14:00, rellene esto :00
        # para evitar problemas con el API
        start = init_values['-IN-'] + '%20' + init_values['Start_data'] + ':00'
        end = init_values['-IN2-'] + '%20' + init_values['End_data'] + ':00'
        rows = int(init_values['RowsAPA'])
        columns = int(init_values['ColsAPA'])
        lateral_length = float(init_values['LCAPA']) # ahora mismo esta tomando a x, como columnas, LRAPA seria como filas
        depth_length = float(init_values['LRAPA'])

        PMType=PA_Dict[init_values['DDMAPA']]
        #key = AF.AnimationPA2(columns, rows, lateral_length, 
                    #depth_length,int(init_values['NumSenAPA']),
                    #int(init_values['AniTimePA']),PMType, values, init_values, start, end)
        key = F.AnimationPA2(columns, rows, lateral_length, 
                    depth_length,int(init_values['NumSenAPA']),
                    int(init_values['AniTimePA']),PMType, values, init_values, start, end)
        if key[1] == 0:
            sg.Popup(f'No se encontraron datos en esta fecha del sensor {key[0]}', keep_on_top=True)
            break


    # Eventos que causan que se llame una funcion del script AvgFunciontions.py
    elif event == 'Graficar Promedio CSV':
        PMType=PA_Dict[values['DDMPCSV']]
        AF.GraphAvg(int(values['Rows']),int(values['Cols']),int(values['LC']), 
                    int(values['LR']),int(values['Hora']),
                    int(int(values['Mins'])/2)+1,int(values['NumSen']),values['Folder'],PMType)

    elif event == 'Gráfica Lateral':
        # Modificable
        chain = list(range(1,int(values['NumSenPPA'])+1))
        coordenadas = {}
        it = 0
        for i in range(int(values['RowsPPA'])):
            for j  in range(int(values['ColsPPA'])):
                coordenadas[f'{i},{j}'] = chain[it]
                it += 1  
        layout8 = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
                [sg.Frame('Disposición de los sensores', [[sg.Input(coordenadas[f'{row},{col}'],
                key=f'{row},{col}', size=(5,1)) for col in range(int(values['ColsPPA']))]
                for row in range(int(values['RowsPPA']))],font=font2)],
                [sg.Button('Submit', font=('Times New Roman',12)),sg.Button('Exit', font=('Times New Roman',12))]]
        #event, values = window.read()
        window.close()

        window = sg.Window('Proyecto UCMEXUS', layout8, font=font2)
        event, initvalues = window.read()

        #start = init_values['-IN-'] + '%20' + init_values['Start_data'] + ':00'
        start = '2022-03-14%2018:50:00'
        #end = init_values['-IN2-'] + '%20' + init_values['End_data'] + ':00'
        end = '2022-03-14%2023:50:00'
        PMType=PA_Dict[values['DDMPPA']]
        F.LateralAvg(int(values['RowsPPA']),int(values['ColsPPA']),int(values['LCPPA']), 
                    int(values['LRPPA']),PMType,initvalues,start,end, int(values['MinsPasadosP']))

    elif event == 'Gráficar Animación CSV':
        PMType=PA_Dict[values['DDMACSV']]
        AF.AnimationCSV(int(values['RowsACSV']),int(values['ColsACSV']),int(values['LCACSV']), 
                    int(values['LRACSV']),int(values['HoraACSV']),
                    int(int(values['MinsACSV'])/2)+1,int(values['NumSenACSV']),int(values['AniTime']),PMType,values['Carpeta'])

    elif event == 'Graficar Animación PurpleAir':
        PMType=PA_Dict[values['DDMAPA']]
        AF.AnimationPA(int(values['RowsAPA']),int(values['ColsAPA']),int(values['LCAPA']), 
                    int(values['LRAPA']),int(int(values['MinsPasados'])/2),int(values['NumSenAPA']),int(values['AniTimePA']),PMType)

    elif event == 'Gráfica Promedio PurpleAir':
        PMType=PA_Dict[values['DDMPPA']]
        AF.GraphAvgPA(int(values['RowsPPA']),int(values['ColsPPA']),int(values['LCPPA']), 
                    int(values['LRPPA']),int(int(values['MinsPasadosP'])/2),int(values['NumSenPPA']),PMType)
window.close()