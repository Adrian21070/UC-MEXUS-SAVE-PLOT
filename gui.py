import PySimpleGUI as sg
from pytz import utc
import functions as Func
from datetime import datetime
from dateutil import tz

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

font = ('Times New Roman', 16)
font2 = ('Times New Roman', 12)

# Zonas horarias
Local_H = tz.tzlocal()
Utc = tz.gettz('UTC')

# Espacios de memoria de los valores del usuario
events = []
values = {}

# Diseño de la interfaz. 
sg.theme('DarkAmber')

# Creacion de la interfaz
layout = [[sg.Text('Seleccione de donde desea sacar los datos', font = font)],
           [sg.Button('Online'),sg.Button('Archivo CSV'),
            sg.Button('Exit',key='Exit')]]

# Columnas reutilizables.
col1=[[sg.Text('Selecciona los datos a analizar.')]]
col2=[[sg.Checkbox('PM 1.0 CF', default=False, key="PM 1.0 CF")], 
        [sg.Checkbox('PM 2.5 CF', default=False, key ="PM 2.5 CF")],
        [sg.Checkbox('PM 10.0 CF', default=False, key ="PM 10.0 CF")],
        [sg.Checkbox('PM 2.5 ATM', default=False, key ="PM 2.5 ATM")]]

# Creación de GUI
window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
event, value = window.read()
events.append(event)
values.update(value)

while True:
    if events in (sg.WIN_CLOSED, "Exit"):
        window.close()
        break
    
    # Dos condiciones importantes
    elif 'Online' in events:
        window.close()
        # Selección de datos a analizar
        layout = [col1, col2, [sg.Button('Next'), sg.Button('Exit')]]

        window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
        event, value = window.read()
        events.append(event)
        values.update(value)

        """
        Quito los else?????
        """

        # Datos de la medición
        if events[-1] == 'Next':
            layout = [[sg.Text('Datos acerca del número de sensores y su disposición',font=font)],
                [sg.Text('Num. de Sensores', size =(25, 1)), sg.InputText(key='NumSen')],
                [sg.Text('Num. Columnas de Sensores', size =(25, 1)), sg.InputText(key='Columns')],
                [sg.Text('Num. Filas de Sensores', size =(25, 1)), sg.InputText(key='Rows')],
                [sg.Text('Distancia entre Columnas', size =(25, 1)), sg.InputText(key='Col_dis')],
                [sg.Text('Distancia entre Filas', size =(25, 1)), sg.InputText(key='Row_dis')],
                [sg.Text('Tiempo de duración animación (Min.)', size =(25, 1)), sg.InputText(key='Length')],
                [sg.Button("Next"), sg.Button('Exit')]]
            
            # Posible error, numero de cols y rows exceden la cantidad de sensores maximos
            # Numero de sensores puestos son mayores al numero de llaves que tiene este codigo registrado (30)
            
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
            event, value = window.read()
            events.append(event)
            values.update(value)
        else:
            continue

        # Fecha de la medición
        if events[-1] == 'Next':
            layout = [[sg.Text('Selección de fecha y hora de las mediciones',font=font)],
                [sg.CalendarButton('Dia de inicio de la medición',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='Start')],
                [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(key='Start_hour')],
                [sg.CalendarButton('Dia del fin de la medición',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='End')],
                [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(key='End_hour')],
                [sg.Button("Next"), sg.Button('Exit')]]

                # No se puede escoger una fecha en el futuro, ya que no existen datos.

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
            event, value = window.read()
            events.append(event)
            values.update(value)
        else:
            continue
        
        # Disposición de los sensores
        if events[-1] == 'Next':
            chain = list(range(1,int(values['NumSen'])+1))
            coordenadas = {}
            it = 0
            
            for i in range(int(values['Rows'])):
                for j in range(int(values['Columns'])):
                    coordenadas[f'{i},{j}'] = chain[it]
                    it += 1

            layout = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
                    [sg.Frame('Disposición de los sensores', [[sg.Input(coordenadas[f'{row},{col}'],
                    key=f'{row},{col}', size=(5,1)) for col in range(int(values['Columns']))]
                    for row in range(int(values['Rows']))],font=font2)],
                    [sg.Button('Next', font=('Times New Roman',12)),sg.Button('Exit', font=('Times New Roman',12))]]
            
            # No puede ingresar un numero mayor a 30, ni menor a 1, esto esta en base a la numeración de los sensores
            # Que contamos en disposición actualmente.

            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
            event, value = window.read()
            indx = value
            events.append(event)
            #values.update(value)
        else:
            continue

        # Procesamiento y extracción de datos a partir de los datos ingresados.
        if events[-1] == 'Next':
            # Inicio y fin de datos
            start = values['Start'] + '%20' + values['Start_hour'] + ':00'
            end = values['End'] + '%20' + values['End_hour'] + ':00'

            # Numero de columnas y columnas y su separación
            rows = int(values['Rows'])
            columns = int(values['Columns'])
            lateral_length = float(values['Col_dis']) # ahora mismo esta tomando a x como columnas
            depth_length = float(values['Row_dis'])

            # Tipos de datos a sacar
            holes = {}
            PMType = []
            for ii in PA_Dict.keys():
                if values[ii]:
                    # Para cada tipo de dato se sacara la data de todos los sensores
                    PMType.append(PA_Dict[ii])

                    # Primero, mi función de redondeo de fechas, me asigna aquí
                    # a todos los sensores con las mismas fechas, si quiero hacerlo
                    # a prueba de huecos(falta de datos) no debo hacer esto.
                    x_axis, y_axis, z_axis = Func.Data_extraction(rows, columns, lateral_length, depth_length, PA_Dict[ii], indx, start, end)
                    """
                    Esta data es cruda en este momento, no hay ajuste de datos ni nada
                    Puedo trabajar con ella para comprobar los huecos.
                    """
                    holes = Func.huecos(z_axis, indx)
                    #holes[ii] = Func.huecos(z_axis, indx)

            # Notificar con una ventana que existen huecos
            layout = [[sg.Text('Existen sensores con huecos de información',font=font), sg.Text(f'(YYYY-MM-DD HH-MM-SS)')],
                        [sg.Text('Los sensores son:')]]

            for ii in holes.keys():
                if holes[ii]:
                    k = list(holes[ii].keys())
                    v = list(holes[ii].values())
                    k2 = []
                    v2 = []
                    utc_k = []
                    utc_v = []
                    k = [m.replace(tzinfo=Local_H) for m in k]
                    v = [m.replace(tzinfo=Local_H) for m in v]

                    #zone = k[0].strftime('%Z')
                    # Transformo a string los elementos de tiempo.
                    for jj in range(len(k)):
                        utc_k.append(k[jj].astimezone(Utc).strftime('%Y-%m-%d %X'))
                        utc_v.append(v[jj].astimezone(Utc).strftime('%Y-%m-%d %X'))
                        k2.append(k[jj].strftime('%Y-%m-%d %X'))
                        v2.append(v[jj].strftime('%Y-%m-%d %X'))
                        layout.append([sg.Frame('',[[sg.Text(f'{ii} presenta un hueco desde')]
                                                ,[sg.Text(f'{k2[jj]} hasta {v2[jj]}, timezone: Local.')]
                                                ,[sg.Text(f'{utc_k[jj]} hasta {utc_v[jj]}, timezone: UTC')]])])

            layout.append([sg.Button('Solucionar errores')])
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
            event, value = window.read()

        # Solicitar CSV de los dias donde hay huecos de los sensores que tienen el error.
        layout = [[sg.Text('¿Cómo desea solucionar el problema?', font = font)],
                    [sg.Text('Rellenar data con archivos CSV: ',size=(50,1)), sg.Button('CSV')],
                    [sg.Text('Recortar este intervalo para todos los sensores (Perdida de información): ',size=(50,1)), sg.Button('CUT')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
        event, value = window.read()      

        if event == 'CSV':
            # Solicita la ubicación de los archivos, y utiliza pandas para rellenar info
            # Trabajo pesado!!!
            layout = []
            # Solicito la ubicación de archivos
            for ii in holes.keys():
                if holes[ii]:
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
                    layout.append([[sg.Text(f'{ii}, archivos de los dias {days}'), sg.Input(key=ii), sg.FileBrowse()]])
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
            event, value = window.read()

            

            #Func.Data_extraction(rows, columns, lateral_length, depth_length, PMType, indx, start, end)
        elif event == 'CUT':
            # Utiliza pandas u otra cosa para simplemente borrar el intervalo de datos perdidos
            # En todos los sensores.
            pass

    elif 'Archivo CSV' in events:
        pass