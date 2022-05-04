import PySimpleGUI as sg
from pytz import utc
import functions as Func
from datetime import datetime
from dateutil import tz

### Urgente.
"""
Puntos importantes.
Arregla la selección de SX, solo sirve para sensores con denominación menor a 10
S1, S2,... esto viene en fix_data y holes

Tambien es importante realizar cosas con los NaN ocasionales que puedan venir (poco probable para
el tipo de dato que tomamos para completar online, pero si es necesario para generar csv con este codigo,
esto para un futuro...)

"""

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
                    PMType.append(PA_Onl[ii])
                    #PMType.append(PM_Dict[ii])
                    #PMType.append(PA_Dict[ii])

                    # Primero, mi función de redondeo de fechas, me asigna aquí
                    # a todos los sensores con las mismas fechas, si quiero hacerlo
                    # a prueba de huecos(falta de datos) no debo hacer esto.
                    x_axis, y_axis, z_axis, minimum_dates, maximum_dates = Func.Data_extraction(rows, columns, lateral_length, depth_length, PA_Dict[ii], indx, start, end)
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
                if holes[ii]: # Si no esta vacio, entra al if
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
            layout = [[sg.Text('Introduce los archivos solicitados con el nombre del tipo SX_YYYYMMDD:')]]
            # Solicito la ubicación de archivos
            for ii in holes.keys():
                if holes[ii]:
                    days = []
                    for jj in range(len(k)):
                        day = k[jj].day  # Esto esta bien???
                        day2 = v[jj].day # Esta bien???
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
            
            
            """
            Por el momento solo podre solucionar 1 hueco por sensor
            esto es debido a que aun no pienso como hacer para solicitar 2 ubicaciones de archivo
            por sensor, y como guardarlas en un array o un diccionario o en que cosa...
            """




            layout.append([[sg.Button('Fix data'), sg.Button('Exit')]])
            window.close()
            window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
            event, value = window.read()

            # Selecciono unicamente las direcciones no repetidas.
            value = [value[a] for a in value.keys() if ('Browse' in str(a))]
            
            if event == 'Fix data':
                # Llama a una función que arreglara los huecos.
                # z_axis tiene sus datos de fecha en local, no esta en UTC recuerdalo.
                csv_data = Func.csv_extraction(value, key=1)

                z_axis = Func.Fix_data(z_axis, csv_data, PMType, holes)

                """
                Ya une dataframes aparentemente sin problemas, falta actualizar df_online con los nuevos df ya unidos,
                revisa los comentarios, quiza exista algo que falta corregir, detalles pequeños.

                Dale orden a las secuencias de la interfaz, y toca trabajar en las graficas.

                Limpia el codigo, hay mucho comentario no util.
                """

                # Se ajusta la data para que inicien y terminen igual los sensores, adecua la función.
                delta = 1
                z_axis, limites = Func.Matrix_adjustment(minimum_dates, maximum_dates, z_axis, indx, delta)
                #z_axis = Func.Matrix_adjust(minimum_dates, maximum_dates, z_axis, indx)
                
                # Notificar al usuario si existieron problemas o todo bien???
                # if exito == true
                layout = [[sg.Text('Se completo exitosamente el arreglo de datos')],[sg.Button('Next')]]
                
                # else
                # layout = [sg.Text('Ocurrio un error al rellenar datos')]
                window.close()
                window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
                event, value = window.read()
            

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
                Func.graphs(x_axis, y_axis, z_axis, columns, rows, depth_length, lateral_length, value, PMType, indx, limites)
                

        elif event == 'CUT':
            # Utiliza pandas u otra cosa para simplemente borrar el intervalo de datos perdidos
            # En todos los sensores.
            pass

    elif 'Archivo CSV' in events:
        """
        Parte de esto se resolvio con Fix data, pero lo dificil ahora,
        sera limpiar la data del csv, ya que contiene muchos errores en ciertas columnas...
        """
        pass