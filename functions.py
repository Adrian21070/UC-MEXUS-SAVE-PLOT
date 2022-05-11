# Librerias
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import PySimpleGUI as sg
import pandas as pd
import math

from matplotlib import cm
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

Utc = tz.gettz('UTC')
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

    """
    Por el momento el ajuste de la matriz, se dejara para posterior, ya que esto sera lo ultimo a
    verificar. Primero debemos observar si existen huecos.
    """
    # Se compatibiliza la data, ahora si es matriz rectangular/cuadrada, podemos graficar ya.
    #z_axis = Matrix_adjustment(dict_of_dates_minimum, dict_of_dates_maximum, z_axis, indx)
    return x_axis, y_axis, z_axis, dict_of_dates_minimum, dict_of_dates_maximum

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
            prom = [start.astimezone(Local_H).strftime("%Y/%m/%d, %H:%M:%S")+' -> '+end.astimezone(Local_H).strftime("%Y/%m/%d, %H:%M:%S")]

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
    # Buscando huecos, los extremos y la cantidad de datos del sensor x
    # No interesa en este momento, solo comprueba si existen huecos.
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
        """
        df = pd.read_csv(ii)
        # Ahora, solo nos quedaremos con los mismos datos que otorga el online
        df = df[col_name]
        # Cambiamos los nombres de las columnas.
        df.columns = new_col_name

        # Arreglamos las fechas para hacerlas más sencillas de tratar.
        date = list(df['created_at'])
        date_new = []
        
        if key == 1:
            for temp in date:
                temp = temp.replace('/','-')
                temp = temp.replace('T',' ')
                #temp = temp.replace('z',' UTC')
                temp = temp.strip('z')
                early = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
                if early.second >= 30:
                    early = early + timedelta(seconds=60-early.second)
                else:
                    early = datetime(early.year, early.month, early.day, early.hour, early.minute, 0, tzinfo=from_zone)
                
                date_new.append(early)
        else:
            for temp in date:
                temp = temp.replace('/','-')
                temp = temp.replace('T',' ')
                temp = temp.replace('z',' UTC')
                date_new.append(temp)
        
        date = [] #Limpio la variable

        df['created_at'] = date_new #Asigno mi fecha corregida

        # Ahora solo queda almacenar el dataframe en el diccionario
        data_frames[ii] = df
        """
    return data_frames

def conversor_datetime_string(date, key):
    """
        Si key = 0, tomara a date como string en formato utc,
        regresara una lista con las fechas en formato datetime utc.

        Si key = 1, tomara a date como string en formato local,
        regresara una lista con las fechas en formato datetime local.

        Si key = 2, tomara a date como datetime, y regresara
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
    
    return new_date
        
def Fix_data(data_online, csv_data, PMType, holes):
    # Como un sensor puede presentar diversos huecos, debemos usar todos los csv designados a dicho sensor
    # este pedazo de codigo solo ordenara los csv acorde a su sensor.

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
        val = conversor_datetime_string(val, key = 2)

        num = list(data_online[jj].values()) # Obtiene los datos numericos, en este caso son listas.
        if isinstance(num[0], list): # Compruebo que sea una matriz
            num = [[float(b) for b in i] for i in num] # Convierto todo a numerico
        else: # Si no es matriz, aplico esta formula.
            num = [float(b) for b in num]

        df_online[jj] = pd.DataFrame(num,columns=col)
        df_online[jj].insert(0,"created_at",val)

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
            chunk = df_c.loc[row[0]+1:row_end[0]-1]

            # Unimos
            df = pd.concat([df, chunk])

            # Sort the data
            df = df.sort_values(by=['created_at'])

            # Reset the index
            df.reset_index(inplace=True, drop=True)

        # Se actualizan los datos de online ya corregidos.
        df_online[ii] = df

        """
        for jj in csv_data_dic[ii].keys():
            df_c = csv_data_dic[ii][jj] # Itera con los archivos csv del sensor x, diversos dias
            sensor_holes = holes[f'Sensor {ii[-1]}'] #Corregir lo de sensor ii, no aceptara sensores mayores al 9
            for kk in sensor_holes.keys():

                start = conversor_datetime_string([kk, sensor_holes[kk]], key=2)
                init = start[0]
                end = start[1]

                date = df_c['created_at'] 

                # Encuentra en csv, donde esta init y end.
                row = df_c.index[(((date-init) < timedelta(seconds=120)) & ((init-date) < timedelta(seconds=120)))].tolist()

                row_end = df_c.index[(((date-end) < timedelta(seconds=120)) & ((end-date) < timedelta(seconds=120)))].tolist()

                # Seleccionar el trozo de información entre row y row_end, no se incluyen
                chunk = df_c.loc[row[0]+1:row_end[0]-1]

                # Creo lista entre inicio y fin, con separación de dos minutos, esto corrige las fechas
                #seconds = (end-init).seconds + (end-init).days*24*60*60 - 2*60
                #dates = [init + timedelta(seconds=d) for d in range(seconds + 1) if((d%120 == 0) & (d!=0))]
                #chunk['created_at'] = dates

                # Que pasa si online tiene un hueco de 12:00 a 14:01?, chunck tendra los datos de 12:02
                # 12:04, ..., 13:58. Va a existir un problema...
                
                # Puedo modificar el 14:01 para que se redonde a 14:00 o 14:02, pero esto me obligara a modificar
                # todos los datos posteriores a este...

                # Limpiamos la data?

                # Unimos
                df = pd.concat([df, chunk])

                # Sort the data
                df = df.sort_values(by=['created_at'])

                # Reset the index
                df.reset_index(inplace=True, drop=True)

        # Se actualizan los datos de online ya corregidos.
        df_online[ii] = df
        """
    """

    Limpiar data, existen errores por esto...

    """

    return df_online

def animate(i,measurements,x_axis,y_axis,ax1,columns,rows,lateral_length,depth_length,PMType,indx,limites):
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
    textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3"

    ax1.clear()
    ax1.annotate(textstr,
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=10, ha='center', va='bottom')
    
    ax1.annotate(df['created_at'][i],
            xy=(0.5, 0.8), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=10, ha='center', va='bottom')

    scamap = plt.cm.ScalarMappable(cmap='inferno')
    fcolors = scamap.to_rgba(maximum)
    size_scatter = [100 for n in range(len(x_axis))]
    ax1.scatter3D(x_axis, y_axis, z_axis, s=size_scatter, c=z_axis, facecolors=fcolors, cmap='inferno')

    x_final = int((columns-1)*lateral_length)
    y_final = int((rows-1)*depth_length)
    gridx,gridy,gridz0 = Interpol(x_axis,y_axis,z_axis,x_final,y_final)
    ax1.plot_surface(gridx, gridy, gridz0,cmap=cm.inferno, linewidth=0, antialiased=False)

    ax1.set_xlabel('Carretera (m), (x)')
    ax1.set_ylabel('Profundidad|campo (m), (y)')
    ax1.zaxis.set_rotate_label(False)
    ax1.set_zlabel('ug/m3', rotation = 0)
    ax1.set_xlim3d(0, (columns-1)*lateral_length)
    ax1.set_xticks(np.arange(0, columns*lateral_length, lateral_length))
    ax1.set_ylim3d(0, (rows-1)*depth_length)
    ax1.set_yticks(np.arange(0, rows*depth_length, depth_length))
    #ax1.set_zlim3d(limites[0], limites[1])
    ax1.view_init(25, -130)
    #ax1.view_init(17, -176)
    #plt.title(df['created_at'][i])
    plt.title(PMType[0])

def Interpol(x,y,z,xfinal,yfinal):
    points = np.concatenate((x.T, y.T), axis=1)
    grid_x, grid_y = np.mgrid[0:xfinal:200j, 0:yfinal:200j]
    grid_z0 = griddata(points, z, (grid_x, grid_y), method='cubic')
    return grid_x, grid_y, grid_z0

def animate_1D(i, measurements, PMType, depth, ax1, columns, rows, indx, limites):
    # Solo importa y_axis, profundidad
    z_axis = []
    y_axis = [value*depth for value in range(rows)]
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
    ax1.scatter(y_axis, filas, s=40, c='r')

    # Interpolación
    #f = interpolate.interp1d(y_axis, filas, kind='cubic')
    f = interpolate.interp1d(y_axis, filas, kind='quadratic')
    x = np.arange(0, max(y_axis), 0.1)
    ax1.plot(x, f(x), '--', linewidth=2)

    ax1.annotate(df['created_at'][i],
        xy=(0.5, 0), xytext=(0, 10),
        xycoords=('axes fraction', 'figure fraction'),
        textcoords='offset points',
        size=10, ha='center', va='bottom')

    ax1.set_xlabel('Profundidad|campo (m), (y)')
    ax1.set_ylabel('Valor promedio (ug/m3)')
    ax1.legend(['Promedio', 'Interpolación cuadrática'])
    ax1.set_xticks(np.arange(0, rows*depth, depth))
    ax1.axis([-0.5, max(y_axis)+0.5, 0, limites[1]])
    plt.title(PMType[0])

def graphs(x, y, z, columns, rows, row_dist, col_dist, value, PMType, indx, limites):
    indx = list(indx.values())
    length = float(value['Length'])
    if value['Animation3D']:
        #fig,ax = plt.subplots()
        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')
        #ax1 = plt.axes(projection='3d')
        
        frames = len(z[f'Sensor {indx[0]}']['created_at'])
        frame_rate = length*60000/frames

        #animate(7,z,x,y,ax1,columns,rows,col_dist,row_dist, PMType, indx, limites)
        #plt.show()
        ani = animation.FuncAnimation(fig,animate,interval=frame_rate,
                fargs=(z,x,y,ax1,columns,rows,col_dist,row_dist,PMType,indx,limites),
                frames=frames, repeat=True)
        ani.save('3.gif',writer='imagemagick', fps=frames/(length*60))
        plt.show()
                
    if value['LateralAvg']:
        fig = plt.figure()
        ax1 = fig.add_axes((0.1, 0.17, 0.8, 0.72))
        #fig, ax1 = plt.subplots()
        frames = len(z[f'Sensor {indx[0]}']['created_at'])
        frame_rate = length*60000/frames
        #animate_1D(6, z, PMType, row_dist, ax1, columns, rows, indx, limites)
        #plt.show()
        anim = animation.FuncAnimation(fig, animate_1D, interval=frame_rate,
                fargs=(z,PMType,row_dist,ax1,columns,rows,indx,limites),
                frames=frames, repeat=True)
        anim.save('Lateral_avg.gif',writer='imagemagick', fps=frames/(length*60))
        plt.show()

    if value['Historico']:
        pass
    pass

    # Esto para tener un dataframe bonito una vez todos los sensores, tienen
    # la misma cantidad de datos.
    """df = pd.DataFrame([key for key in raw_data.keys()], columns=['Name'])

    df['id'] = [value['id'] for value in clients.values()]

    df['email'] = [value['email'] for value in clients.values()]

    df['gender'] = [value['gender'] for value in clients.values()]

    df['ip_address'] = [value['ip_address'] for value in clients.values()]

    df['money'] = [value['money'] for value in clients.values()]

    df"""