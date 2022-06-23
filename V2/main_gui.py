

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

def shutdown(window):
    window.close()
    sys.exit()