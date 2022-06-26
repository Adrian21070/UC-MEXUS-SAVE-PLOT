# Librerias
import os, sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import PySimpleGUI as sg
import pandas as pd
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm, style
from datetime import datetime, timedelta
from dateutil import tz
from scipy import interpolate
from scipy.interpolate import griddata
from purple_air import *

#IDs y Llaves del canal prinicpal del sensor A los dispositivos  PurpleAir 
keys = ['TMTVNTYUXGGT7MK3', 'T5VPQSVT9BAE5ZI1',"F2K1DV64M1Z75VU4", "O94LWPUDGE645M0W","3DHCZRPJ1M6YIFV7",
        "LMP9I4DYO31RLQCM", "4YNO8GQDC5V4D8AH", "YR676V09QO1KX1Q7", "YTLP8VLPWKIJ9G4K", "ODM4VO7RDXCYWL2O",
        "0S1GMA57I3VO7TN8","IJ44H5T0VGAPOM1X", "4MGD149UTH64IKO1","D1EPGDRFWRLFDRWL", "3GOKID03X1ZQI7UO",
        "IO35IQWN7OD7QZRI", "KYOJ88GAQ573QZOG","D6NQDA4PSE9FDW9N","KR2E9MGDRAR8U4FI", "TV45OPQDRKXEOYF3",
        "WXQHTF7MVPTGUV3H", "HWHD61TYPRC08IJ0", "TEQLCBVA8W53X6MQ", "LYE31WD6M75Z3J8E", "CF8HVDROSC9N04O7",
        "BCJV79PNCBA20CEI", "ITO12LYZ84AXMSB1", "LAU5S4Y8NY6F9FNK", "9WAVRBGJHR27Q9SB", "FP815UH9YRZ77MY1"]
        
channel_ids =[1367948, 1367997, 1336916, 1367985, 1369647, 
              1369624, 1379154, 1368013, 1369640, 1367969,
              1379214, 1367956, 1367952, 1336974, 1368009, 
              1453911, 1452796, 1451589, 1450382, 1452792,
              1452813, 1450481, 1447356, 1452808, 1451577,
              1451621, 1452812, 1452804, 1450358, 1450485]

# Se crea un diccionario para los sensores
sensors = {}
for ii in range(0,len(keys)):
    sensors[f'Sensor {ii+1}'] = [keys[ii],channel_ids[ii]]

# Fuente utilizada en los graficos
font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

# Diccionario para seleccionar el tipo de material
# particulado a graficar a partir de los archivos CSV
PM_Dict={"PM 1.0 CF": "pm1_0_cf_1",	
         "PM 2.5 CF": "pm2_5_cf_1",	
         "PM 10.0 CF": "pm10_0_cf_1",	
         "PM 1.0 ATM": "pm1_0_atm",	
         "PM 2.5 ATM": "pm2_5_atm",	
         "PM 10.0 ATM" : "pm10_0_atm"}

# Simple formato para transformar de csv a online.
CSV_dict = {"UTCDateTime":"created_at",
            "pm1_0_atm":"PM1.0_ATM_ug/m3",
            "pm2_5_atm":"PM2.5_ATM_ug/m3", 
            "pm10_0_atm":"PM10.0_ATM_ug/m3",
            "uptime":"UptimeMinutes", 
            "rssi":"RSSI_dbm",
            "current_temp_f":"Temperature_F", 
            "current_humidity":"Humidity_%",
            "pm1_0_cf_1":"PM1.0_CF1_ug/m3", 
            "pm2_5_cf_1":"PM2.5_CF1_ug/m3",
            "pm10_0_cf_1":"PM10.0_CF1_ug/m3", 
            "p_0_3_um":">=0.3um/dl", "p_0_5_um":">=0.5um/dl", 
            "p_1_0_um":">=1.0um/dl", "p_2_5_um":">=2.5um/dl", 
            "p_5_0_um":">=5.0um/dl", "p_10_0_um":">=10.0um/dl",
            "pm1_0_atm_b":"PM1.0_ATM_B_ug/m3",
            "pm2_5_atm_b":"PM2.5_ATM_B_ug/m3", 
            "pm10_0_atm_b":"PM10.0_ATM_B_ug/m3",
            "mem":"UptimeMinutes_B", "adc":"ADC", 
            "pressure":"Pressure_hpa",
            "pm1_0_cf_1_b":"PM1.0_CF1_B_ug/m3", 
            "pm2_5_cf_1_b":"PM2.5_CF1_B_ug/m3",
            "pm10_0_cf_1_b":"PM10.0_CF1_B_ug/m3", 
            "p_0_3_um_b":">=0.3_B_um/dl", "p_0_5_um_b":">=0.5_B_um/dl", 
            "p_1_0_um_b":">=1.0_B_um/dl", "p_2_5_um_b":">=2.5_B_um/dl", 
            "p_5_0_um_b":">=5.0_B_um/dl", "p_10_0_um_b":">=10.0_B_um/dl"}

# Diccionario para seleccionar el tipo de material 
# particulado a graficar a partir de los datos en el canal
# principal de thingspeak. 
PA_Dict={"PM 1.0 CF": "field1",	
         "PM 2.5 CF": "field2",	
         "PM 10.0 CF": "field3",
         "PM 2.5 ATM": "field8"}

# Todos los datos que puede pedir el usuario de online.
Column_labels = ['PM1.0_ATM_ug/m3', 'PM2.5_ATM_ug/m3', 'PM10.0_ATM_ug/m3',
                'PM1.0_CF1_ug/m3', 'PM2.5_CF1_ug/m3', 'PM10.0_CF1_ug/m3',
                'PM1.0_ATM_B_ug/m3', 'PM2.5_ATM_B_ug/m3', 'PM10.0_ATM_B_ug/m3',
                'PM1.0_CF1_B_ug/m3', 'PM2.5_CF1_B_ug/m3', 'PM10.0_CF1_B_ug/m3']

PA_Onl = {"PM 1.0 ATM": "PM1.0_ATM_ug/m3", "PM 2.5 ATM": "PM2.5_ATM_ug/m3",
        "PM 10.0 ATM": "PM10.0_ATM_ug/m3", "PM 1.0 CF": "PM1.0_CF1_ug/m3",
        "PM 2.5 CF": "PM2.5_CF1_ug/m3", "PM 10.0 CF": "PM10.0_CF1_ug/m3",
        "PM 1.0 ATM B": "PM1.0_ATM_B_ug/m3", "PM 2.5 ATM B": "PM2.5_ATM_B_ug/m3",
        "PM 10.0 ATM B": "PM10.0_ATM_B_ug/m3", "PM 1.0 CF B": "PM1.0_CF1_B_ug/m3",
        "PM 2.5 CF B": "PM2.5_CF1_B_ug/m3", "PM 10.0 CF B": "PM10.0_CF1_B_ug/m3"}

Utc = tz.tzutc()
Local_H = tz.tzlocal()

def Data_extraction(rows, columns, lateral_length, depth_length, PMType, indx, start, end):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    z_axis = {}
    x_axis = np.array([list(range(0,columns))*rows])*lateral_length 

    column_with_interval = np.arange(0,rows*depth_length,depth_length)
    y_axis = np.array([np.concatenate([([t]*columns) for t in column_with_interval], axis=0)])

    # This dictionaries, helps us to store the minimum and maximum date of each sensor.
    dict_of_dates_minimum = {}
    dict_of_dates_maximum = {}
    
    for j in indx.values():
        # Lectura de datos
        sensor_id = sensors[f'Sensor {j}']
        TSobject = Thingspeak(read_api_key=sensor_id[0], channel_id=sensor_id[1])

        data,c = TSobject.read_one_sensor(start=start, end=end)
        if len(data) == 0:
            return [j, 0]

        #Redondeo de tiempo y cambio a zona horaria actual, y se extrae el vector de datos PM
        data, P1_ATM_IND = redondeo_fecha_y_datos_de_interes(data, from_zone, to_zone, PMType)

        # Se almacena el primer y ultimo valor de todos disponible del sensor
        dict_of_dates_minimum[f'Sensor {j}'] = data[0]['created_at']
        dict_of_dates_maximum[f'Sensor {j}'] = data[len(data)-1]['created_at']

        z_axis[f'Sensor {j}'] = P1_ATM_IND

    return x_axis, y_axis, z_axis, dict_of_dates_minimum, dict_of_dates_maximum

def open_csv(window, value):
    # Leo los archivos dentro de la carpeta.
    data = {}
    it = 1
    minimum = {}
    maximum = {}

    try:
        with os.scandir(value['Browse']) as ficheros:
            # Ficheros right now has directories with csv inside
            for fichero in ficheros:
                dir = value['Browse'] + '/' + fichero.name
                if it == 1:
                    with os.scandir(dir) as files:
                        
                        try:
                            for file in files:
                                #file should have the name as SXXX_YYYY_MM_DD
                                name = file.name
                                # Abro el archivo
                                df = pd.read_csv(dir + '/' + name)
                                # Paso a datetime las fechas.
                                df['created_at'] = conversor_datetime_string(df['created_at'], key=0)

                                data[f'Sensor {name[1:4]}'] = df
                        except:
                            layout = [[sg.Text('Error al leer un archivo', font=('Times New Roman',18))],
                                    [sg.Text(f'Se tuvo problemas al leer el archivo {name}')],
                                    [sg.Button('Return'), sg.Button('Exit')]]
                            window.close()
                            window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
                            event, value = window.read()

                            if event in ('Exit', sg.WIN_CLOSED):
                                window.close()
                                sys.exit()
        
                            return True, 0, 0, window

                    it += 1
                else:
                    with os.scandir(dir) as files:

                        try:
                            for file in files:
                                # file should have the name as SXXX_YYYY_MM_DD
                                name = file.name
                                # Abro el archivo
                                df = pd.read_csv(dir + '/' + name)
                                # Paso a datetime las fechas
                                df['created_at'] = conversor_datetime_string(df['created_at'], key=0)

                                data[f'Sensor {name[1:4]}'] = pd.concat([data[f'Sensor {name[1:4]}'], df])

                                # Sort the data
                                data[f'Sensor {name[1:4]}'] = data[f'Sensor {name[1:4]}'].sort_values(by=['created_at'])

                                # Reset the index
                                data[f'Sensor {name[1:4]}'].reset_index(inplace=True, drop=True)
                        except:
                            layout = [[sg.Text('Error al leer un archivo', font=('Times New Roman',18))],
                                    [sg.Text(f'Se tuvo problemas al leer el archivo {name}')],
                                    [sg.Button('Return'), sg.Button('Exit')]]
                            window.close()
                            window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
                            event, value = window.read()

                            if event in ('Exit', sg.WIN_CLOSED):
                                window.close()
                                sys.exit()
        
                            return True, 0, 0, window
    except:
        layout = [[sg.Text('Carpeta no encontrada', font=('Times New Roman',18))],
                [sg.Text(f'Favor de introducir una carpeta valida.')],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()

        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        
        return True, 0, 0, window

    # Obtengo los minimos y maximos de cada sensor.
    for ii in data.keys():
        df = data[ii]
        date = df['created_at']

        # En formato datetime utc.
        maximum[ii] = date.iloc[-1]
        minimum[ii] = date.iloc[0]

    return data, minimum, maximum, window

def redondeo_fecha_y_datos_de_interes(data, from_zone, to_zone, PMType):
    """
        @name: Data processing
        @brief: Funcion para tratar los datos de los sensores.
                Esta funcion utiliza datos obtenidos de los canales de thingspeak
        @param: 
            - data: data recibida del API
            - from_zone: zona a transformar el tiempo (UTC)
            - to_zone: zona a convertir (actual)
            - PMType: tipo de material particulado
        @return: data procesado en tags de tiempo y un vector con los datos del material particulado
    """
    P1_ATM_IND = {}
    for ii in range(len(data)):
        # Quita Z y una T para tratar mejor el tiempo
        earliest = data[ii]['created_at'].strip('Z').replace('T', ' ')

        # Pasa de utc a local.
        time_utc = datetime.strptime(earliest, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
        early = time_utc.astimezone(to_zone)

        # Lo transforma a formato datetime para operacionar con el
        # compruebo que si los segundos son mayores a 30, pase al siguiente minuto
        if early.second >= 30:
            #start = datetime(early.year, early.month, early.day, early.hour, early.minute+1, 0, tzinfo=to_zone)
            start = early + timedelta(seconds=60-early.second)
        else:
            start = datetime(early.year, early.month, early.day, early.hour, early.minute, 0, tzinfo=to_zone)

        # Lo sobreescribe
        data[ii]['created_at'] = start

        # Guarda con un index de fecha los valores de PM
        P1_ATM_IND[start] = data[ii][PMType]

    return data, P1_ATM_IND

def Matrix_adjustment(minimum, maximum, z, delta):
    z_adjusted = {}
    first_start = max(minimum.values()).astimezone(tz.tzutc())
    final_end = min(maximum.values()).astimezone(tz.tzutc())
    dif = final_end - first_start

    seconds = dif.seconds + dif.days*24*60*60
    cycles = math.ceil(seconds/(delta*60*60))

    maximum = []
    minimum = []

    for ii in z.keys():
        df = z[ii]
        columns = df.columns.tolist()
        date = df['created_at']
        z_adjusted[ii] = pd.DataFrame(columns=columns)
        
        start = first_start
        end = first_start + timedelta(hours=delta)
        for jj in range(cycles):
            # Se tomaran pedazos de datos en intervalos de tiempo para sacarles su promedio
            rows = df.loc[((date >= start) & (date < end))]

            # Calculamos promedios
            prom = [start.astimezone(Local_H).strftime("%Y/%m/%d, %H:%M")+' -> '+end.astimezone(Local_H).strftime("%Y/%m/%d, %H:%M")]

            for kk in columns[1:]: # Para revisar si PMType es mas de 1
                data = rows[kk]
                prom.append(round(np.mean(data),4))

            z_adjusted[ii].loc[jj] = prom

            if jj != cycles-2:
                start = end
                end = start + timedelta(hours=delta)
            else:
                start = end
                end = final_end + timedelta(seconds=1)

        maximum.append(max(z_adjusted[ii][kk])) # Para revisar si PMType es mas de 1
        minimum.append(min(z_adjusted[ii][kk]))
    
    limites = [min(minimum), max(maximum)]
    return z_adjusted, limites

def huecos(raw_data, indx):
    # Comprobación de datos
    # Se comprueban los datos internos de cada sensor
    sizes = {}
    num_holes_per_sensor = {}
    """
    # Quiza con loc de pandas se realice más eficientemente.
    # Para esto, hay que transformar en dataframe desde antes de entrar aquí.
    # Y modificar este codigo.
    """
    # Fuerza bruta, quiza exista otro metodo de comprobar los huecos...
    for ii in indx.values():
        # Fechas de las mediciones
        time = list(raw_data[f'Sensor {ii}'].keys())
        sizes[f'Sensor {ii}'] = {}
        temp = 0

        for jj in range(len(time)-1):
            delta = time[jj+1] - time[jj]

            if delta.seconds > 250:
                day = (time[jj].astimezone(Utc)).day
                day2 = (time[jj+1].astimezone(Utc)).day
                # Existe un hueco
                # sizes tiene como llave el inicio del hueco y como value el final.
                sizes[f'Sensor {ii}'].update({time[jj]:time[jj+1]})

                if temp == 0:
                    temp += 1
                    num_holes_per_sensor[f'Sensor {ii}'] = temp
                    day3 = day
                    day4 = day2
                else:
                    if day != day3 or day2 != day4:
                        temp += 1
                        num_holes_per_sensor[f'Sensor {ii}'] = temp
                        day3 = day
                        day4 = day2
            
    return sizes, num_holes_per_sensor

def csv_extraction(dir, key=0):
    """
        Si key = 1, dara un dataframe con la fecha en formato datetime,
        si no se da el parametros key, otorgara la fecha en string.

        Regresa un diccionario de dataframes, 1 por cada archivo que se le de.
    """
    from_zone = tz.tzutc()

    col_name = list(CSV_dict.keys())
    new_col_name = list(CSV_dict.values())
    data_frames = {}

    for ii in dir:
        # df = pd.read_csv(dir[f'Sensor {ii}'])
        df = pd.DataFrame()
        for jj in dir[ii]: # Lee todos los archivos del sensor XX, ya que puede tener mas de 1
            # Ahora, solo nos quedaremos con los mismos datos que otorga el online
            df2 = pd.read_csv(jj)
            df2 = df2[col_name]
            # Cambiamos los nombres de las columnas.
            df2.columns = new_col_name

            # Arreglamos las fechas para hacerlas más sencillas de tratar.
            date = list(df2['created_at'])
            date_new = []
        
            if key == 1:
                for temp in date:
                    temp = temp.replace('/','-')
                    temp = temp.replace('T',' ')
                    temp = temp.strip('z')
                    early = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
                    if early.second >= 30:
                        early = early + timedelta(seconds=60-early.second)
                    else:
                        early = datetime(early.year, early.month, early.day, early.hour, early.minute, 0, tzinfo=from_zone)
                
                    date_new.append(early)
            else: #Quiza esto en otra funcion separada, no le veo utilidad aqui.
                for temp in date:
                    temp = temp.replace('/','-')
                    temp = temp.replace('T',' ')
                    temp = temp.replace('z',' UTC')
                    date_new.append(temp)
        
            date = [] #Limpio la variable

            df2['created_at'] = date_new #Asigno mi fecha corregida

            # Unimos
            df = pd.concat([df, df2])

        # Sort the data
        df = df.sort_values(by=['created_at'])

        # Reset the index
        df.reset_index(inplace=True, drop=True)

        # Ahora solo queda almacenar el dataframe en el diccionario
        data_frames[ii] = df
        
    return data_frames

def conversor_datetime_string(date, key):
    """
        Si key = 0, tomara a date como string en formato utc,
        regresara una lista con las fechas en formato datetime utc.

        Si key = 1, tomara a date como string en formato local,
        regresara una lista con las fechas en formato datetime local.

        Si key = 2, tomara a date como datetime, y cambiara de utc a local,
        o de local a utc.

        Si key = 3, tomara a date como datetime, y regresara
        una lista de strings.
    """
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    new_date = []
    if key == 0:
        for ii in range(len(date)):
            temp = date[ii].strip(' UTC')
            # Transformo de string a datetime utc
            time_utc = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
            new_date.append(time_utc)

    elif key == 1:
        for ii in range(len(date)):
            temp = date[ii]
            # Transformo de string a datetime local
            time_local = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=to_zone)
            new_date.append(time_local)

    elif key == 2:
        if str(date[0].tzinfo) == 'tzutc()':
            for ii in range(len(date)):
                temp = date[ii]
                time = temp.astimezone(to_zone)
                new_date.append(time)

        elif str(date[0].tzinfo) == 'tzlocal()':
            for ii in range(len(date)):
                temp = date[ii]
                time = temp.astimezone(from_zone)
                new_date.append(time)
    
    elif key == 3:
        if str(date.iloc[-1].tzinfo) == 'tzutc()':
            for ii in date:
                # Transformo de datetime a string
                time_local = ii.strftime('%Y-%m-%d %H:%M:%S UTC')
                new_date.append(time_local)
                
        elif str(date.iloc[-1].tzinfo) == 'tzlocal()':
            for ii in date:
                # Transformo de datetime a string
                time_local = ii.strftime('%Y-%m-%d %H:%M:%S')
                new_date.append(time_local)

    return new_date
        
def Fix_data(data_online, csv_data, PMType, holes, key):
    # Como un sensor puede presentar diversos huecos, debemos usar todos los csv designados a dicho sensor
    # este pedazo de codigo solo ordenara los csv acorde a su sensor.

    if key == 'Online':
        col = []
        # Por el momento solo solucionara 1 hueco por sensor.
        for ii in range(len(Column_labels)):
            if Column_labels[ii] in PMType:
                col.append(Column_labels[ii])


        for kk in csv_data.keys():
            a = csv_data[kk] # se extrae el dataframe
            a = a[['created_at']+col] # se filtra a solo los datos necesarios dados por el usuario.
            csv_data[kk] = a

        # Creo el dataframe de online
        df_online = {}
        # Se creara un diccionario de dataframes, para facilitar su acceso.
        for jj in data_online.keys():
            # Prepara data
            val = list(data_online[jj].keys()) # Lista de todas las fechas
            # data online tiene sus fechas en formato datetime local
            # Paso a UTC
            val = conversor_datetime_string(val, key = 2)

            num = list(data_online[jj].values()) # Obtiene los datos numericos, en este caso son listas.
            if isinstance(num[0], list): # Compruebo que sea una matriz
                num = [[float(b) for b in i] for i in num] # Convierto todo a numerico
            else: # Si no es matriz, aplico esta formula.
                num = [float(b) for b in num]

            df_online[jj] = pd.DataFrame(num,columns=col)
            df_online[jj].insert(0,"created_at",val)
    else:
        for ii in data_online.keys():
            val = data_online[ii]['created_at']
            val = conversor_datetime_string(val, key = 2)
            data_online[ii]['created_at'] = val
        df_online = data_online

    # Una vez con toda la data de online y csv puesta en dataframes
    # Se realizara el rellenado de los huecos.

    # Solo se realizara en los sensores que tengan huecos, no en todos.
    for ii in csv_data.keys():
        df = df_online[ii]
        
        df_c = csv_data[ii]
        sensor_holes = holes[ii]

        for kk in sensor_holes.keys():
            start = conversor_datetime_string([kk, sensor_holes[kk]], key=2) #Convierto a utc
            init = start[0]
            end = start[1]

            date = df_c['created_at'] 

            # Encuentra en csv, donde esta init y end.
            row = df_c.index[(((date-init) < timedelta(seconds=120)) & ((init-date) < timedelta(seconds=120)))].tolist()

            row_end = df_c.index[(((date-end) < timedelta(seconds=120)) & ((end-date) < timedelta(seconds=120)))].tolist()

            # Seleccionar el trozo de información entre row y row_end, no se incluyen
            chunk = df_c.loc[row[-1]+1:row_end[0]-1]

            # Unimos
            df = pd.concat([df, chunk])

            # Sort the data
            df = df.sort_values(by=['created_at'])

            # Reset the index
            df.reset_index(inplace=True, drop=True)

        # Se actualizan los datos de online ya corregidos.
        df_online[ii] = df

    return df_online

def animate(i,measurements,x_axis,y_axis,ax1,columns,rows,lateral_length,depth_length,PMType,indx,limites,fig,prom, styles):
    """
    Realiza la superficie.
    """

    z_axis = []

    # Se obtiene la lista de las fechas de cada medición
    #time = list(measurements[f'S{indx[0]}']['created_at'].keys())
    for k in range(len(measurements)):
        jj = indx[k] #Numero del sensor actual.
        #Accede al dato del sensor jj, en el tiempo i.
        df = measurements[f'Sensor {jj}']
        dato = df[PMType[0]][i]
        #dato = measurements[f'Sensor {jj}'][time[i]]
        z_axis.append(float(dato))
    
    minimum = round(min(z_axis),2)
    maximum = round(max(z_axis),2)
    average = round(np.mean(z_axis),2)
    #textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3  Promedio: "+str(average)+" ug/m3"
    #textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3"
    textstr = "Min: "+str(minimum)+" ug/m3   Max: "+str(maximum)+" ug/m3"

    ax1.clear()
    ax1.annotate(textstr,
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=styles['Label_size'], ha='center', va='bottom')
    
    #ax1.annotate(df['created_at'][i],
    #        xy=(0.5, 0.8), xytext=(0, 10),
    #        xycoords=('axes fraction', 'figure fraction'),
    #        textcoords='offset points',
    #        size=10, ha='center', va='bottom')

    if styles['Marker'] != 'No marker':
        scamap = plt.cm.ScalarMappable(cmap='inferno')
        fcolors = scamap.to_rgba(maximum)
        size_scatter = [100 for n in range(len(x_axis))]
        ax1.scatter3D(x_axis, y_axis, z_axis, marker=styles['Marker'], s=size_scatter, c=z_axis, facecolors=fcolors, cmap='inferno')

    x_final = max(max(x_axis))
    y_final = max(max(y_axis))
    x_min = min(min(x_axis))
    y_min = min(min(y_axis))

    gridx,gridy,gridz0 = Interpol(x_axis,y_axis,z_axis,x_final,y_final,x_min,y_min)
    ax1.plot_surface(gridx, gridy, gridz0,cmap=cm.inferno, linewidth=0, antialiased=False)

    # Plot style
    ax1.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax1.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax1.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    #axis labels
    ax1.set_ylabel(styles['ylabel_content'],
                fontsize=styles['Label_size'],
                fontfamily=styles['Font'])

    ax1.set_xlabel(styles['xlabel_content'],
                fontsize=styles['Label_size'],
                fontfamily=styles['Font'])

    ax1.set_zlabel(styles['zlabel_content'],
                fontsize=styles['Label_size'],
                rotation = 180,
                fontfamily=styles['Font'])

    ax1.set_xlim3d(x_min, x_final)
    ax1.set_xticks(np.arange(x_min, x_final+lateral_length, lateral_length))
    ax1.invert_xaxis()

    ax1.set_ylim3d(y_min, y_final)
    ax1.set_yticks(np.arange(y_min, y_final+depth_length, depth_length))

    ax1.set_zlim3d(0, limites[1])

    ax1.tick_params(axis='both',
                labelsize=styles['Label_size']-2)

    if prom == 0:
        #subtitle
        ax1.set_title(styles['Subtitle_content'],
             x=0.5,
             y=0.87,
             transform=fig.transFigure,
             fontsize=styles['Subtitle_size'],
             fontfamily=styles['Font'])
        
        if styles['Bold']:
            #superior title
            plt.suptitle(styles['Title_content'],
                 x=0.5,
                 y=0.92,
                 transform=fig.transFigure,
                 fontsize=styles['Title_size'],
                 fontweight="bold",
                 fontfamily=styles['Font'])
        else:
            #superior title
            plt.suptitle(styles['Title_content'],
                 x=0.5,
                 y=0.92,
                 transform=fig.transFigure,
                 fontsize=styles['Title_size'],
                 fontweight="regular",
                 fontfamily=styles['Font'])
        
    else:
        #subtitle
        ax1.set_title(f'Promedio cada {round(prom*60)} minutos\n'+df['created_at'][i],
             x=0.5,
             y=0.87,
             transform=fig.transFigure,
             fontsize=styles['Subtitle_size'],
             fontfamily=styles['Font'])

        if styles['Bold']:
            #superior title
            plt.suptitle('Concentración ' + 'PM2.5_ATM_ug/m3'.replace('_','').replace('ATM','').strip('ug/m3'),
                 x=0.5,
                 y=0.92,
                 transform=fig.transFigure,
                 fontsize=styles['Title_size'],
                 fontweight="bold",
                 fontfamily=styles['Font'])
        else:
            #superior title
            plt.suptitle('Concentración ' + 'PM2.5_ATM_ug/m3'.replace('_','').replace('ATM','').strip('ug/m3'),
                 x=0.5,
                 y=0.92,
                 transform=fig.transFigure,
                 fontsize=styles['Title_size'],
                 fontweight="regular",
                 fontfamily=styles['Font'])

    #ax1.set_facecolor('w')
    #ax1.set_xlabel('Carretera (m)')
    #ax1.set_ylabel('Profundidad (m)')
    #ax1.zaxis.set_rotate_label(False)

    ax1.view_init(styles['Polar'], styles['Azimutal'])

def Interpol(x,y,z,xfinal,yfinal,xmin,ymin):
    points = np.concatenate((x.T, y.T), axis=1)
    grid_x, grid_y = np.mgrid[xmin:xfinal:200j, ymin:yfinal:200j]
    grid_z0 = griddata(points, z, (grid_x, grid_y), method='cubic')
    return grid_x, grid_y, grid_z0

def animate_1D(i, measurements, y_axis, PMType, depth, ax1, columns, rows, indx, limites, alpha, prom, fig, styles):
    """
    Realiza la grafica del promedio lateral.
    """
    # Solo importa y_axis, profundidad
    z_axis = []
    y_axis = np.arange(min(min(y_axis)), max(max(y_axis))+depth, depth)
    #y_axis = [value*depth for value in range(rows)]
    # Creando lista con los datos ii
    for jj in indx:
        df = measurements[f'Sensor {jj}']
        s = df[PMType[0]][i]
        z_axis.append(float(s))

    # Promedio por filas.
    filas = []
    kk = 0
    col = columns
    #No = list(prom.values())
    for ii in range(rows):
        sum = z_axis[kk:col]
        kk = col
        col = kk + columns

        filas.append(np.mean(sum))
        # Aquí ya se obtuvo el promedio por filas en el tiempo ii, se obtendra una cantidad n de promedio de filas a lo largo
        # de todo el for principal, se piensa mandar a animar esto para obtener una animación del cambio de promedio de filas.
    
    # Realiza el plot
    ax1.clear()
    if styles['Marker'] != 'No marker':
        ax1.scatter(y_axis, filas, s=styles['MarkerSize'], marker=styles['Marker'], c=styles['MarkerColor'])

    # Interpolación
    #f = interpolate.interp1d(y_axis, filas, kind='cubic')
    f = interpolate.interp1d(y_axis, filas, kind='quadratic')
    x = np.arange(min(y_axis), max(y_axis), 0.1)
    ax1.plot(x, f(x), styles['LineStyle'], linewidth=styles['LineSize'], c=styles['LineColor'])

    #ax1.annotate(df['created_at'][i],
    #    xy=(0.5, 0), xytext=(0, 10),
    #    xycoords=('axes fraction', 'figure fraction'),
    #    textcoords='offset points',
    #    size=10, ha='center', va='bottom')

    #axis labels
    ax1.set_xlabel(styles['xlabel_content'],
                  fontsize=styles['Label_size'],
                  fontfamily=styles['Font'],
                  fontstyle=styles['Xstyle'])

    ax1.set_ylabel(styles['ylabel_content'],
                  fontsize=styles['Label_size'],
                  fontfamily=styles['Font'],
                  fontstyle=styles['Ystyle'])

    ax1.set_xticks(y_axis, axis = 0)

    #ax1.set_xticks(np.concatenate([[0], y_axis], axis = 0))

    ax1.tick_params(axis='both',
                   labelsize=styles['Label_size']-2)

    if prom == 0:
        #subtitle
        ax1.set_title(styles['Subtitle_content'],
                     x=0.5,
                     y=0.83,
                     transform=fig.transFigure,
                     fontsize=styles['Subtitle_size'],
                     fontfamily=styles['Font'],
                     fontstyle=styles['Substyle'])
        
        if styles['Bold']:
            #superior title
            plt.suptitle(styles['Title_content'],
                         x=0.5,
                         y=0.95,
                         transform=fig.transFigure,
                         fontsize=styles['Title_size'],
                         fontweight="bold",
                         fontfamily=styles['Font'],
                         fontstyle=styles['Titlestyle'])
        else:    
            #superior title
            plt.suptitle(styles['Title_content'],
                         x=0.5,
                         y=0.95,
                         transform=fig.transFigure,
                         fontsize=styles['Title_size'],
                         fontweight="regular",
                         fontfamily=styles['Font'],
                         fontstyle=styles['Titlestyle'])

    else:
        #subtitle
        ax1.set_title(f'Promedio cada {round(prom*60)} minutos\n'+df['created_at'][i],
                     x=0.5,
                     y=0.83,
                     transform=fig.transFigure,
                     fontsize=styles['Subtitle_size'],
                     fontfamily=styles['Font'],
                     fontstyle=styles['Substyle'])
        
        if styles['Bold']:
            #superior title
            plt.suptitle('Concentración ' + PMType[0].replace('_','').replace('ATM','').strip('ug/m3'),
                         x=0.5,
                         y=0.95,
                         transform=fig.transFigure,
                         fontsize=styles['Title_size'],
                         fontweight="bold",
                         fontfamily=styles['Font'],
                         fontstyle=styles['Titlestyle'])
        else:
            #superior title
            plt.suptitle('Concentración ' + PMType[0].replace('_','').replace('ATM','').strip('ug/m3'),
                         x=0.5,
                         y=0.95,
                         transform=fig.transFigure,
                         fontsize=styles['Title_size'],
                         fontweight="regular",
                         fontfamily=styles['Font'],
                         fontstyle=styles['Titlestyle'])

    #ax1.set_xlabel('Profundidad (m)')
    #ax1.set_ylabel('Valor promedio (ug/m3)')
    if (styles['Marker'] != 'No marker') and (styles['LineStyle'] != 'No line'):
        # Incluye el promedio y interpolación en la leyenda.
        ax1.legend(['Promedio', 'Interpolación cuadrática'], loc='upper right', framealpha=alpha, fontsize=styles['Label_size']-2, prop={'family': styles['Font']})
    elif (styles['Marker'] != 'No marker') and (styles['LineStyle'] == 'No line'):
        # Incluye promedio, no interpolación
        ax1.legend(['Promedio'], loc='upper right', framealpha=alpha, fontsize=styles['Label_size']-2, prop={'family': styles['Font']})
    elif (styles['Marker'] == 'No marker') and (styles['LineStyle'] != 'No line'):
        # Incluye interpolación, no promedio
        ax1.legend(['Interpolación cuadrática'], loc='upper right', framealpha=alpha, fontsize=styles['Label_size']-2, prop={'family': styles['Font']})
    
    #Si no entra en ninguna, no habra leyenda.

    #ax1.set_xticks(np.concatenate([[0], y_axis], axis = 0), fontsize=11)
    #ax1.yticks(fontsize=11)

    if styles['Recorrer']:
        ax1.axis([min(y_axis)-0.1, max(y_axis)+0.5, 0, limites[1]])
    else:
        ax1.axis([0, max(y_axis)+0.5, 0, limites[1]])
    plt.subplots_adjust(top=0.8)
    #plt.title(PMType[0].replace('_','').replace('ATM','').strip('ug/m3'), 
    #      fontdict={'family': 'Times New Roman', 
    #                'size': 14})
    #plt.title(PMType[0])

def surface(x,y,z,columns, rows, row_dist, col_dist, graph_selection, value_anim, PMType, indx, limites, Surface):
    # Value_anim viene información sobre periodo, y duración de la animación
    # graph_selection viene información sobre el tipo de grafica deseada.
    # Styles viene toda la información de tipo de letra, markers, nombre del archivo, ruta, etc.

    indx = list(indx.values())

    if graph_selection['An_superficie']:
        # Esto genera un gif
        prom = float(value_anim['delta']) #Delta # Posible problema.
        length = float(value_anim['Length']) #Minutes

        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')

        frames = len(z[f'Sensor {indx[0]}']['created_at'])
        frame_rate = length*60000/frames

        ani = animation.FuncAnimation(fig,animate,interval=frame_rate,
                fargs=(z,x,y,ax1,columns,rows,col_dist,row_dist,PMType,indx,limites,fig,prom,Surface),
                frames=frames, repeat=True)
        
        # Ubicación principal
        if '.gif' in Surface['Name']:
            path = os.path.join(Surface['Surf_folder'], Surface['Name'])
            path2 = os.path.join(Surface['Surf_folder'], Surface['Name'][0:len(Surface['Name'])-4]+'_frames')
        else:
            path = os.path.join(Surface['Surf_folder'], Surface['Name']+'.gif')
            path2 = os.path.join(Surface['Surf_folder'], Surface['Name']+'_frames')

        ani.save(path, writer='imagemagick', fps=frames/(length*60))
        #plt.show()

        if True:
            os.makedirs(path2, exist_ok=True)

            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111, projection='3d')
            for ii in range(frames):
                path = os.path.join(path2,f'Frame{ii}.png')
                animate(ii,z,x,y,ax2,columns,rows,col_dist,row_dist, PMType, indx, limites, fig2, prom, Surface)
                if Surface['Fondo']:
                    plt.savefig(path, transparent=True)
                else:
                    plt.savefig(path, transparent=False)
    
    else:
        # Genera una estatica.
        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')
        animate(0, z, x, y, ax1, columns, rows, col_dist, row_dist, PMType, indx, limites, fig, 0, Surface)
        if '.png' in Surface['Name']:
            path = os.path.join(Surface['Surf_folder'], Surface['Name'])
        else:
            path = os.path.join(Surface['Surf_folder'], Surface['Name']+'.png')

        if Surface['Fondo']:
            plt.savefig(path, transparent=True)
        else:
            plt.savefig(path, transparent=False)

def lateral_avg(x,y,z,columns, rows, row_dist, col_dist, graph_selection, value_anim, PMType, indx, limites, lateral):
    indx = list(indx.values())
    
    if graph_selection['An_lateral']:
        prom = float(value_anim['delta']) #Delta
        length = float(value_anim['Length']) #Minutes

        fig3, ax3 = plt.subplots(1,1,dpi=100)
        frames = len(z[f'Sensor {indx[0]}']['created_at'])
        frame_rate = length*60000/frames
        #animate_1D(6, z, y, PMType, row_dist, ax3, columns, rows, indx, limites,1.0, prom, fig3, lateral)
        #plt.show()
        
        anim = animation.FuncAnimation(fig3, animate_1D, interval=frame_rate,
                fargs=(z,y,PMType,row_dist,ax3,columns,rows,indx,limites,1.0, prom, fig3, lateral),
                frames=frames, repeat=True)

        # Ubicación principal
        if '.gif' in lateral['Name']:
            path = os.path.join(lateral['Lateral_folder'], lateral['Name'])
            path2 = os.path.join(lateral['Lateral_folder'], lateral['Name'][0:len(lateral['Name'])-4]+'_frames')
        else:
            path = os.path.join(lateral['Lateral_folder'], lateral['Name']+'.gif')
            path2 = os.path.join(lateral['Lateral_folder'], lateral['Name']+'_frames')
        
        anim.save(path, writer='imagemagick', fps=frames/(length*60))
        plt.show()

        if True:
            os.makedirs(path2, exist_ok=True)

            fig4, ax4 = plt.subplots(1,1,dpi=100)
            for ii in range(frames):
                path = os.path.join(path2,f'Frame{ii}.png')
                animate_1D(ii, z, y, PMType, row_dist, ax4, columns, rows, indx, limites,0.0, prom, fig4, lateral)
                if lateral['Fondo']:
                    plt.savefig(path, transparent=True)
                else:
                    plt.savefig(path, transparent=False)

    else:
        window = sg.Window(title='Frecuencia',
                       layout=[[sg.Canvas(key='canvas', size=(720,480))]],
                        finalize=True, size=(720,480))
        # Obtención del canvas
        canvas = window['canvas'].TKCanvas
        fig3, ax3 = plt.subplots(1, 1, dpi=100, figsize=(7,5))
        figure_canvas_agg = FigureCanvasTkAgg(fig3, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='right', expand=1)

        if '.png' in lateral['Name']:
            path = os.path.join(lateral['Lateral_folder'], lateral['Name'])
        else:
            path = os.path.join(lateral['Lateral_folder'], lateral['Name']+'.png')
        
        if lateral['Fondo']:
            animate_1D(0, z, y, PMType, row_dist, ax3, columns, rows, indx, limites, 0.0, 0, fig3, lateral)
            figure_canvas_agg.draw()
            fig3.savefig(path, transparent=True)
        else:
            animate_1D(0, z, y, PMType, row_dist, ax3, columns, rows, indx, limites, 1.0, 0, fig3, lateral)
            figure_canvas_agg.draw()
            fig3.savefig(path, transparent=False)

def historico():
    pass