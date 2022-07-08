import PySimpleGUI as sg
import sys
import os
from pytz import utc
from datetime import datetime
from dateutil import tz

# Fuentes para la interfaz
font = ('Times New Roman', 14)
font2 = ('Times New Roman', 12)
font3 = ('Times New Roman', 18)

# Zonas horarias
Local_H = tz.tzlocal()
Utc = tz.gettz('UTC')

# Diseño de la interfaz. 
sg.theme('DarkAmber')

def save_or_graph():
    layout = [[sg.Text('Favor de seleccionar lo que desea realizar:',font=font3, justification='center', expand_x=True)],
                [sg.Text('',size=(1,1),font=('Times New Roman',1))],
                [sg.Button('Guardar datos',key='Save_data',), sg.Button('Graficar',key='Plot'), sg.Button('Exit')]]
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480), element_justification='center')
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
    return window, event

def holes_warning(window,holes,num_csv):
    # Notificar con una ventana que existen huecos
    layout = []
    for ii in num_csv.keys():
        k = list(holes[ii].keys())
        v = list(holes[ii].values())

        k = [m.replace(tzinfo=Local_H) for m in k] #Lo pongo en local, no utc
        v = [m.replace(tzinfo=Local_H) for m in v] #Lo pongo en local, no utc

        # Transformo a string los elementos de tiempo.
        holes_text = []

        for jj in range(len(k)):
            utc_k = k[jj].astimezone(Utc).strftime('%Y-%m-%d, %X')
            utc_v = v[jj].astimezone(Utc).strftime('%Y-%m-%d, %X')
            k2 = k[jj].strftime('%Y-%m-%d, %X')
            v2 = v[jj].strftime('%Y-%m-%d, %X')

            holes_text.append([sg.Text(f'{k2}  hasta  {v2}, timezone: Local.')])
            holes_text.append([sg.Text(f'{utc_k}  hasta  {utc_v}, timezone: UTC')])
            holes_text.append([sg.Text('',size=(1,1),font=('Times New Roman',1))])
        layout.append([sg.Frame(f'{ii} presenta un hueco desde',holes_text),sg.Text('')])
        layout.append([sg.Text('',size=(1,1),font=('Times New Roman',1))])

    frame = [[sg.Frame('', layout, element_justification='center')]]

    lay = [[sg.Column([[sg.Frame('',[[sg.Text('Existen sensores con huecos de información',font=font), sg.Text(f'(YYYY-MM-DD HH-MM-SS)')],
            [sg.Text('Los sensores son:', font = font)],
            [sg.Text('',size=(1,1), font=('Times New Roman',1))],
            [sg.Column(frame, scrollable=True, vertical_scroll_only=True, expand_y=False)]
            ])]], element_justification='c', scrollable=True, vertical_scroll_only=True, expand_y=True)],
            [sg.Button('Solucionar errores',key='Fix_errors'), sg.Button('No arreglar'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', lay, font = font2, size=(720,480), element_justification='c')
    event, value = window.read()
    if event == None:
        event = 'Fix_errors'
    return window, event

def csv_online2(window, num_holes_per_sensor, holes):
    # Solicitar un folder con los archivos del dia tal.
    layout = [[sg.Text('Seleccione la carpeta donde se encuentran los archivos csv', font=font3)],
                [sg.Text('El nombre de las carpetas es irrelevante, pero asegurate de que los archivos tengan')],
                [sg.Text('este formato (SXXX_YYYY_MM_DD_sd.csv)')]]
    dates = {}
    fechas = {}

    for ii in num_holes_per_sensor.keys():
        k = list(holes[ii].keys())
        v = list(holes[ii].values())
        fechas[ii] = []
        days = []
        for jj in range(len(k)): # Para revisar todos los huecos que tenga el sensor
            day = k[jj].day
            day2 = v[jj].day
            if (day in days):
                pass
            else:
                days.append(day)
                fechas[ii].append(k[jj].strftime("%Y_%m_%d"))
            if (day2 in days):
                pass
            else:
                days.append(day2)
                fechas[ii].append(k[jj].strftime("%Y_%m_%d"))
        # days termina teniendo los dias que existieron huecos por parte del sensor
        for jj in days:
            if jj in dates:
                dates[jj].append(ii)
            else:
                dates.update({jj:[]})
                dates[jj].append(ii)

    # Ordeno el diccionario
    dates = dict(sorted(dates.items(), key=lambda x: x[0]))
    dates = dict(sorted(dates.items(), key=lambda x: x[1]))

    for ii in dates.keys():
        lay = []
        lay.append([sg.Text(f'Carpeta con los archivos del dia {ii} (UTC) para los sensores:')])
        num = 5
        n = len(dates[ii])//num

        start = 0
        if n > 0:
            end = num
        else:
            end = len(dates[ii])

        if len(dates[ii]) % num == 0:
            # No hace salto de linea extra
            for jj in range(n):
                lay.append([sg.Text(' '.join(dates[ii][start:end]))])
                start = end
                if end+num > len(dates[ii]):
                    end = len(dates[ii])
                else:
                    end += num

        else:
            for jj in range(n+1):
                lay.append([sg.Text(', '.join(dates[ii][start:end]))])
                start = end
                if end+num > len(dates[ii]):
                    end = len(dates[ii])
                else:
                    end += num

        lay.append([sg.Text('Ubicación de la carpeta: '),sg.Input(), sg.FolderBrowse()])

        layout.append([sg.Frame('', lay)])
        layout.append([sg.Text('\n', size=(1,1), font=('Times New Roman', 1))])
    
    layout.append([sg.Button('Fix data'), sg.Button('Exit')])
    lay = [[sg.Column(layout, scrollable=True, vertical_scroll_only=True,expand_y=True, expand_x=True)]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', lay, font=font2, size=(720,480))
    event, value = window.read()

    if event in ('Exit', sg.WIN_CLOSED):
        shutdown(window)

    try:
        for ii in value.keys():
            if not value[ii]:
                raise ValueError('Faltan carpetas')
    except:
        layout = [[sg.Text('Favor de llenar todos los campos requeridos', font=font3)],
                    [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', lay, font=font, size=(720,480))
        event, value = window.read()
        
        if event in ('Exit', sg.WIN_CLOSED):
            shutdown(window)
        
        return window, event

    # Quito los repetidos.
    val = [value[a] for a in value.keys() if ('Browse' in str(a))]
    # Ordenado de menor a mayor en cuestión de dias.

    # Asignar esos directorios a su lugar correspondiente
    # Lo transformo en un diccionario, para facilitar ciertas cosas posteriores
    value = {}
    it = 0
    for ii in num_holes_per_sensor.keys():
        value[ii] = []
        cont = 0
        for jj in dates.keys():
            if ii in dates[jj]:
                try:
                    # Entro al folder y busco el archivo correspondiente al sensor X
                    with os.scandir(val[cont]) as ficheros:
                        # ficheros tiene los archivos csv del dia x
                        try:
                            for fichero in ficheros:
                                for fecha in fechas[ii]:
                                    if fichero.name == 'S'+ii[-3:] + '_' + fecha + '_sd.csv':
                                        dir = val[cont] + '/' + fichero.name
                                        value[ii].append(dir)
                                        it += 1
                                        break
                                if it>0:
                                    break
                            if not value[ii]:
                                raise ValueError("No CSV")
                        except:
                            # Avisar que no se encontro el archivo del sensor tal...
                            layout = [[sg.Text(f'No se encontro el archivo del sensor S{ii[-3:]}', font=font3)],
                                    [sg.Button('Return'), sg.Button('Exit')]]
                            window.close()
                            window = sg.Window('Proyecto UC-MEXUS', lay, font=font, size=(720,480))
                            event, value = window.read()
                            
                            if event in ('Exit', sg.WIN_CLOSED):
                                shutdown(window)

                            return window, event
                            
                except:
                    # Problemas al abrir el folder
                    a = val[cont]
                    layout = [[sg.Text(f'No se logro abrir el folder {a}', font=font3)],
                                    [sg.Button('Return'), sg.Button('Exit')]]
                    window.close()
                    window = sg.Window('Proyecto UC-MEXUS', lay, font=font, size=(720,480))
                    event, value = window.read()
                    
                    if event in ('Exit', sg.WIN_CLOSED):
                        shutdown(window)

                    return window, event

            cont += 1
            it = 0

    return window, value

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
            if jj == num_holes_per_sensor[ii]: #Comprueba que no se haya sobrepasado el numero de archivos que debe tener.
                break
            value[ii].append(val[iter])
            iter += 1
    val = []

    return window, value

def shutdown(window):
    window.close()
    sys.exit()