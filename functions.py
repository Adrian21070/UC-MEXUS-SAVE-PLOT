# Librerias
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import pandas as pd
from matplotlib import cm
from datetime import datetime, timedelta
from dateutil import tz
from scipy import interpolate
from scipy.interpolate import griddata
#from gui import PMType
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

# Diccionario para seleccionar el tipo de material 
# particulado a graficar a partir de los datos en el canal
# principal de thingspeak. 
PA_Dict={"PM 1.0 CF": "field1",	
         "PM 2.5 CF": "field2",	
         "PM 10.0 CF": "field3",
         "PM 2.5 ATM": "field8"}

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
    return x_axis, y_axis, z_axis

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
        start = datetime(early.year, early.month, early.day, early.hour, early.minute, 0)
        # Lo sobreescribe
        data[ii]['created_at'] = start

        # Guarda con un index de fecha los valores de PM
        P1_ATM_IND[start] = data[ii][PMType]

    return data, P1_ATM_IND

def Matrix_adjustment(minimum, maximum, z, indx):
    # Se obtiene el rango de las mediciones a partir de fechas que compartan todos.
    medicion_inicial_mas_reciente = max(minimum.values())
    primera_medicion_final = min(maximum.values())
    
    # Identificacion de caso del rango
    inicio = medicion_inicial_mas_reciente.minute%2
    fin = primera_medicion_final.minute%2

    # Comprobación de casos...
    if ((inicio==0 and fin==0) or (inicio==1 and fin==1)):
        caso = 0
    elif((inicio==1 and fin==0) or (inicio==0 and fin==1)):
        caso = 1

    # Clone the original dataframe
    z_adjusted = {}

    for ii in indx.values():
        z_adjusted[f'Sensor {ii}'] = {}
        aa = medicion_inicial_mas_reciente

        for jj in z[f'Sensor {ii}'].keys():
            # Calcula diferencias entre los extremos del intervalo de medicion inicial
            # y primera medicion final.
            delta = medicion_inicial_mas_reciente - jj
            delta2 = primera_medicion_final - jj

            # Se pasa a segundos
            seconds_delta = delta.days*24*60*60 + delta.seconds
            seconds_delta2 = delta2.days*24*60*60 + delta2.seconds

            # Se comprueba el caso en el que estamos y comparamos los deltas
            if caso == 0:
                if (seconds_delta <= 0) and (seconds_delta2 >= 0):
                    z_adjusted[f'Sensor {ii}'][aa] = z[f'Sensor {ii}'][jj]
                    aa = aa + timedelta(minutes=2)

                else:
                    if (seconds_delta <= 60) and (seconds_delta >= -60):
                        z_adjusted[f'Sensor {ii}'][aa] = z[f'Sensor {ii}'][jj]
                        aa = aa + timedelta(minutes=2)

            elif caso == 1:
                if (seconds_delta <= 0) and (seconds_delta2 >= 0):
                    z_adjusted[f'Sensor {ii}'][aa] = z[f'Sensor {ii}'][jj]
                    aa = aa + timedelta(minutes=2)

                else:
                    if (seconds_delta <= 60) and (seconds_delta >= -60):
                        z_adjusted[f'Sensor {ii}'][aa] = z[f'Sensor {ii}'][jj]
                        aa = aa + timedelta(minutes=2)
                    if (seconds_delta2 <= 60) and (seconds_delta2 >= -60):
                        z_adjusted[f'Sensor {ii}'][aa] = z[f'Sensor {ii}'][jj]
                        aa = aa + timedelta(minutes=2)
            
    return z_adjusted

def huecos(raw_data, indx):
    # Comprobación de datos
    # Se comprueban los datos internos de cada sensor
    # Buscando huecos, los extremos y la cantidad de datos del sensor x
    # No interesa en este momento, solo comprueba si existen huecos.
    sizes = {}
    it = 0

    # Fuerza bruta, quiza exista otro metodo de comprobar los huecos...
    for ii in indx.values():
        # Fechas de las mediciones
        time = list(raw_data[f'Sensor {ii}'].keys())
        sizes[f'Sensor {ii}'] = {}

        for jj in range(len(time)-1):
            delta = time[jj+1] - time[jj]

            if delta.seconds > 180:
                # Existe un hueco
                # sizes tiene como llave el inicio del hueco y como value el final.
                sizes[f'Sensor {ii}'].update({time[jj]:time[jj+1]})
            
    return sizes

def rellenado(data_online, dir, PMType):
    # Asegurate de que PMType tenga los nombres correctos de las columnas
    # de un csv de los sensores!!!
    # Agrega al inicio de PMType esto: UTCDateTime

    for ii in range(len(dir)):
        # Abre el archivo csv del sensor x
        df = pd.read_csv(f'{dir[ii]}')

        # Ahora depuramos el df, solo queremos en este caso
        # las columnas de los PM que selecciono el usuario.
        df = df.loc[:,PMType]


        #for jj in PMType:
        #    df_depurado[jj] = df.loc[:,jj]
        

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