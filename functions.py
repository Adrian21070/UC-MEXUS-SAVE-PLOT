# Librerias requeridas
from datetime import datetime, timedelta
from dateutil import tz
import matplotlib.dates as dates
import  matplotlib.pyplot as plt
from pyparsing import dict_of
# la funcion de abajo importa las funciones del script TSclasses.py para obtener los datos de los canales de thingspeak
from TSclasses import *
import pytz
import numpy as np
from itertools import chain
from mpl_toolkits.mplot3d import Axes3D
import csv
import matplotlib.animation as animation
from matplotlib.offsetbox import AnchoredText
from matplotlib import cm
from scipy import interpolate
from scipy.interpolate import griddata
import os

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

# Planos o superficies
def animate(i, measurements, x_axis, y_axis,ax1,columns,rows,lateral_length,depth_length,indx):
    '''
        @name: animate
        @brief: Funcion para generar una animacion a partir de las mediciones de PM en una cantidad definidad 
                de tiempo.
        @param: 
            - i: iteracion actual
            - measurements: medificiones de material particulado de cada sensor en un periodo de tiempo
            - x_axis: distribucion de datos en el eje x (lateral)
            - y_axis: distribucion de datos en el eje y (profundidad)
            - ax1: figura que se graficara
            - columns: numero de columnas en el arreglos de sensores
            - rows: numero de filas en el arreglo de sensores
            - lateral_length: longitud entre columnas
            - depth_length: longitud entre filas
        @return: Nada, unicamente genera una animación
    '''
    z_axis = []
    indx = list(indx.values())
    # Se obtiene la lista de las fechas de cada medición
    time = list(measurements[f'Sensor {indx[0]}'].keys())
    for k in range(len(measurements)):
        jj = indx[k] #Numero del sensor actual.
        #Accede al dato del sensor jj, en el tiempo i.
        dato = measurements[f'Sensor {jj}'][time[i]]
        z_axis.append(float(dato))
    
    minimum = min(z_axis)
    maximum = max(z_axis)
    average = round(np.mean(z_axis),2)
    textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3  Promedio: "+str(average)+" ug/m3"

    ax1.clear()
    ax1.annotate(textstr,
            xy=(0.5, 0), xytext=(0, 10),
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
    ax1.set_zlabel('ug/m3')
    plt.title(str(i))

def Interpol(x,y,z,xfinal,yfinal):
    points = np.concatenate((x.T, y.T), axis=1)
    grid_x, grid_y = np.mgrid[0:xfinal:200j, 0:yfinal:200j]
    grid_z0 = griddata(points, z, (grid_x, grid_y), method='cubic')
    return grid_x, grid_y, grid_z0

def animate_1D(i, measurements, y_axis, depth, ax1, columns, rows, indx, time, limites):
    # Solo importa y_axis, profundidad
    z_axis = []
    y_axis = [value*depth for value in range(rows)]
    # Creando lista con los datos ii
    for jj in indx.values():
        s = measurements[f'Sensor {jj}'][time[i]]
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
    f = interpolate.interp1d(y_axis, filas, kind='cubic')
    f2 = interpolate.interp1d(y_axis, filas, kind='quadratic')
    x = np.arange(0, max(y_axis), 0.1)
    ax1.plot(x, f(x), '--', x, f2(x), ':', linewidth=2)

    ax1.set_xlabel('Profundidad|campo (m), (x)')
    ax1.set_ylabel('Valor promedio (ug/m3)')
    ax1.legend(['Promedio', 'Interpolación cubica', 'Interpolación cuadrática'])
    ax1.axis([0, max(y_axis), limites[0], limites[1]])
    plt.title(str(i))

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

        data,c= TSobject.read_one_sensor(start=start, end=end)
        if len(data) == 0:
            return [j, 0]

        #Redondeo de tiempo y cambio a zona horaria actual, y se extrae el vector de datos PM
        data, P1_ATM_IND = redondeo_fecha_y_datos_de_interes(data, from_zone, to_zone, PMType)

        # Se almacena el primer y ultimo valor de todos disponible del sensor
        dict_of_dates_minimum[f'Sensor {j}'] = data[0]['created_at']
        dict_of_dates_maximum[f'Sensor {j}'] = data[len(data)-1]['created_at']

        z_axis[f'Sensor {j}'] = P1_ATM_IND

    # Se compatibiliza la data, ahora si es matriz rectangular/cuadrada, podemos graficar ya.
    z_axis = Matrix_adjustment(dict_of_dates_minimum, dict_of_dates_maximum, z_axis, indx)
    return x_axis, y_axis, z_axis

def AnimationPA2(columns, rows, lateral_length, depth_length, SenNum, AniTime,PMType, indx, init_values, start, end):
    '''
        @name: AnimationPA
        @brief: Funcion para generar proveer los componentes necesarios a animate() para generar la animación.
                Esta funcion utiliza datos obtenidos de los canales de thingspeak
        @param: 
            - columns: numero de columnas en el arreglos de sensores
            - rows: numero de filas en el arreglo de sensores
            - lateral_length: longitud entre columnas
            - depth_length: longitud entre filas
            - NumDatos: numero de datos recolectados de cada sensor (empezando por ultima medición)
            - SenNum: numero de sensores
            - AniTime: duracion de la animacion
            - PMType: tipo de material particulado
        @return: Nada, unicamente llama a la funcion animate
    '''
    fig, ax = plt.subplots()
    ax1 = plt.axes(projection='3d')
    x_axis, y_axis, z_axis = Data_extraction(rows, columns, lateral_length, depth_length, PMType, indx, start, end)

    a = list(indx.values())
    time = list(z_axis[f'Sensor {a[0]}'].keys())
    #function to animate the plot and update it (using the animate function) every certain amount of milliseconds
    frame_rate = AniTime*60000/len(time)

    #animate2(0,z_axis,x_axis,y_axis,ax1,columns,rows,lateral_length,depth_length,indx)

    # Modifica animate para poder extraer la data de z, ya que ahora es un diccionario de diccionarios.
    ani = animation.FuncAnimation(fig, animate, interval= frame_rate,fargs=(z_axis,x_axis,y_axis,ax1,columns,rows,lateral_length,depth_length,indx),
                                    frames=len(time), repeat=True)
                                    
    plt.show()
    return ['Logrado', 1]

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
        earliest = data[ii]['created_at'].strip('Z').replace('T', ' ')
        time_utc = datetime.strptime(earliest, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
        early = time_utc.astimezone(to_zone)
        start = datetime(early.year, early.month, early.day, early.hour, early.minute, 0)
        data[ii]['created_at'] = start
        P1_ATM_IND[start] = data[ii][PMType]

    return data, P1_ATM_IND

def Matrix_adjustment(minimum, maximum, z, indx):
    # Se obtiene el rango de las mediciones a partir de fechas que compartan todos.
    medicion_inicial_mas_reciente = max(minimum.values())
    primera_medicion_final = min(maximum.values())
    
    # Identificacion de caso del rango
    inicio = medicion_inicial_mas_reciente.minute%2
    fin = primera_medicion_final.minute%2

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
            delta = medicion_inicial_mas_reciente - jj
            delta2 = primera_medicion_final - jj

            seconds_delta = delta.days*24*60*60 + delta.seconds
            seconds_delta2 = delta2.days*24*60*60 + delta2.seconds

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

def LateralAvg(rows, columns, lateral_length, depth_length, PMType, indx, start, end, total_time):
    x_axis, y_axis, z_axis = Data_extraction(rows, columns, lateral_length, depth_length, PMType, indx, start, end)
    """
    prom = {}
    for ii in indx.values():
        # Accede al sensor y obtiene un promedio de todos sus datos.
        s = list(z_axis[f'Sensor {ii}'].values())
        s = [float(x) for x in s]
        m = np.mean(s)
        prom[f'Sensor {ii}'] = m
    """
    a = list(indx.values())
    time = list(z_axis[f'Sensor {a[0]}'].keys())
    frame_rate = total_time*60000/len(time)

    fig, ax1 = plt.subplots()
    
    #Maximos y mínimos globales
    minimos = []
    maximos = []
    for i in a:
        data = list(z_axis[f'Sensor {i}'].values())
        data = [float(value) for value in data]
        minimos.append(min(data))
        maximos.append(max(data))
    limites = [min(minimos), max(maximos)]

    #animate_1D(0, z_axis, y_axis, depth_length, ax1, columns, rows, indx, time)
    
    ani = animation.FuncAnimation(fig, animate_1D, interval= frame_rate,
            fargs=(z_axis, y_axis, depth_length, ax1, columns, rows, indx, time, limites),
                                    frames=len(time), repeat=True)
    plt.show()
    return 0
    """data = []
    for ii in len(z_axis[f'Sensor {list(indx.values())[0]}']): #Cantidad total de datos
        # Creando lista con los datos ii
        for jj in indx.values():
            s = z_axis[f'Sensor {jj}'][time[ii]]
            data.append(s)

        # Promedio por filas.
        filas = []
        kk = 0
        col = columns
        #No = list(prom.values())
        for ii in range(rows):
            sum = data[kk:col]
            kk = col
            col = kk + columns

            filas.append(np.mean(sum))
        # Aquí ya se obtuvo el promedio por filas en el tiempo ii, se obtendra una cantidad n de promedio de filas a lo largo
        # de todo el for principal, se piensa mandar a animar esto para obtener una animación del cambio de promedio de filas.
    """
    """
    Estan volteados los valores de columa y fila con respecto a la disposición de sensores.
    """

    # Grafico de promedio