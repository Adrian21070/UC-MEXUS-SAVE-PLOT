'''
----------------------------------------------------------
    @file: AvgFunctions.py
    @date: Nov 2021
    @date_modif: Dec 22, 2021
    @author: Raul Dominguez
    @e-mail: a01065986@itesm.mx
    @brief: Functions to graph the data obtained from measurements of an arrangement of PurpleAir sensors
    Open source
----------------------------------------------------------
'''

# Librerias requeridas
from datetime import datetime
from dateutil import tz
import matplotlib.dates as dates
import  matplotlib.pyplot as plt
# la funcion de abajo jala las funciones del script TSclasses.py para obtener los datos de los canales de thingspeak
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
import os

# Fuente utilizada en los graficos
font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

# Default path: SE TIENE QUE MODIFICAR DE ACUERDO A DONDE SE ENCUENTREN ARCHVOS CSV DE SENSORES
path = "D:\Instituto Tecnologico y de Estudios Superiores de Monterrey\Moisés Alejandro Leyva Sanjuan - UCMEXUS\Mediciones prueba\\20211028F"
'''
Nombre de Folders de campañas de monitoreo:
- 20211028
- 20210909
- 20211028F
- 20210909F
'''

#IDs y Llaves del canal prinicpal del sensor A los dispositivos  PurpleAir 
keys = ['TMTVNTYUXGGT7MK3', 'T5VPQSVT9BAE5ZI1',"F2K1DV64M1Z75VU4", "O94LWPUDGE645M0W","3DHCZRPJ1M6YIFV7",
        "LMP9I4DYO31RLQCM", "4YNO8GQDC5V4D8AH", "YR676V09QO1KX1Q7", "YTLP8VLPWKIJ9G4K", "ODM4VO7RDXCYWL2O",
        "0S1GMA57I3VO7TN8","W8HHP4TYIQSX5KTC", "4MGD149UTH64IKO1","D1EPGDRFWRLFDRWL", "3GOKID03X1ZQI7UO",
        "IO35IQWN7OD7QZRI", "KYOJ88GAQ573QZOG","D6NQDA4PSE9FDW9N","IO35IQWN7OD7QZRI", "KYOJ88GAQ573QZOG"]
channel_ids =[1367948, 1367997, 1336916, 1367985, 1369647, 
              1369624, 1379154, 1368013, 1369640, 1367969,
              1379214, 1367958, 1367952, 1336974, 1368009, 
              1453911, 1452796, 1451589, 1453911, 1452796]

def avg(lst):
    '''
        @name: avg
        @brief: Funcion para promediar una lista de numeros
        @param: lst: lista de numeros a promediar
        @return: promedio
    '''
    return round(sum(lst) / len(lst),2)

def GraphAvg(columns, rows, lateral_length, depth_length, hora_de_estudio, tiempo, SenNum,pth,PMType):
    '''
        @name: GraphAvg
        @brief: Funcion para generar la grafica de promedios a traves de una cantidad definida de tiempo 
                utilizando archivos CSV
        @param: 
            - columns: numero de columnas en el arreglos de sensores
            - rows: numero de filas en el arreglo de sensores
            - lateral_length: longitud entre columnas
            - depth_length: longitud entre filas
            - hora_de estudio: hora inicial de recoleccion de datos
            - tiempo: tiempo que duro el estudio
            - SenNum: numero de sensores
            - pth: ruta donde al folder donde se encuentran los archivos CSV
            - PMType: tipo de material particulado
        @return: Nada, unicamente hace una grafica y genera un archivo de texto con información general
    '''
    path=pth
    P1_ATM = []
    Data_Length =[]
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    for i in range (1,SenNum+1):
        time = tiempo
        try:     
            with open(path+'\S'+str(i)+".csv", 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                P1_ATM_IND = []
                mxtime=[]
                lower_time_limit = str(hora_de_estudio)+":00"
                upper_time_limit = str(hora_de_estudio)+":01"
                #mismo valor que el limite inferior
                for row in reader:
                    utcstr = (row.get('UTCDateTime').strip('z').replace('T', ' '))
                    utc = datetime.strptime(utcstr, '%Y/%m/%d %H:%M:%S').replace(tzinfo=from_zone)
                    mx_time = (utc.astimezone(to_zone)).strftime("%H:%M")
                    #print(mx_time)
                    if time<tiempo and time > 0:
                        P1_ATM_IND.append(float(row.get(PMType)))
                        #print(mx_time)
                        mxtime.append(mx_time)
                        time = time -1
                    elif (mx_time == lower_time_limit) or (mx_time==upper_time_limit):
                        P1_ATM_IND.append(float(row.get(PMType)))
                        time = time -1
            Data_Length.append(len(P1_ATM_IND))
        except:
            P1_ATM_IND = [0]    
            Data_Length.append(0)           
        #print(P1_ATM_IND)
        P1_ATM.append(avg(P1_ATM_IND))
 
    fils = open("CSV.txt", "w")
    fils.write(str(Data_Length) + os.linesep)
    fils.write(mxtime[0]+ os.linesep)
    fils.write(mxtime[len(mxtime)-1]+ os.linesep)
    fils.close()
    minimum = min(P1_ATM)
    maximum = max(P1_ATM)
    average = avg(P1_ATM)
    textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3  Promedio: "+str(average)+" ug/m3"

    fig, ax = plt.subplots()

    #creation of list with the components for the x axis of the plot
    x_axis=(list(range(0,rows))*columns)
    x_axis = [element * lateral_length for element in x_axis]

    #creation of a list with the component for the y axis of the plot
    column_with_interval = np.arange(0,columns*depth_length,depth_length)
    y_axis = np.concatenate([([t]*rows) for t in column_with_interval], axis=0)

    size_scatter = [100 for n in range(len(x_axis))]
    
    #print(y_axis)
    ax2 = plt.axes(projection='3d')

    ax2.annotate(textstr,
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=10, ha='center', va='bottom')
    scamap = plt.cm.ScalarMappable(cmap='inferno')
    fcolors = scamap.to_rgba(maximum)
    ax2.scatter3D(x_axis, y_axis, P1_ATM, s=size_scatter, c=P1_ATM, facecolors=fcolors, cmap='inferno')
    #ax2.plot3D(x_axis, y_axis, P1_ATM, 'green')
    x_axis = np.reshape(x_axis,(columns,rows))
    y_axis = np.reshape(y_axis,(columns,rows))
    z_axis = np.reshape(P1_ATM,(columns,rows))
    x_final = int((rows-1)*lateral_length)
    y_final = int((columns-1)*depth_length)
    #el parametro j establece que tantos puntos se interpolaran entre el inicio y final -- añadir a parametro a escoger en el GUI
    xnew, ynew = np.mgrid[0:x_final:40j, 0:y_final:40j]
    #si son muy poquitos datos se tiene que agregar dentro del parentesis de "bisplrep" kx=2 y ky=1, se pueden cambiar sus valores para mejorar la interpolación
    tck = interpolate.bisplrep(x_axis, y_axis, z_axis, s=0)
    znew = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)
    ax2.plot_surface(xnew, ynew, znew,cmap=cm.inferno, linewidth=0, antialiased=False, rcount=500, ccount=500)
    ax2.set_xlabel('Carretera (m)')
    ax2.set_ylabel('Profundidad (m)')
    ax2.set_zlabel('ug/m3')
    plt.title("Promedio de "+ str((tiempo-1)*2) + " mins a partir de las "+ str(hora_de_estudio)+" hrs")
    m = cm.ScalarMappable(cmap=cm.inferno)
    m.set_array(znew)	
    plt.colorbar(m, ax=ax2)
    plt.show()
    #return fig

def LateralAvg(columns, rows, lateral_length, depth_length, hora_de_estudio, tiempo, SenNum,pth,PMType):
    '''
        @name: LateralAvg
        @brief: Funcion que hace un promedio de cada sensor para un tiempo definido y despues hace un promedio
                de cada fila, resultando en una grafica lateral. Esta funcion usa archivos CSV
        @param: 
            - columns: numero de columnas en el arreglos de sensores
            - rows: numero de filas en el arreglo de sensores
            - lateral_length: longitud entre columnas
            - depth_length: longitud entre filas
            - hora_de estudio: hora inicial de recoleccion de datos
            - tiempo: tiempo que duro el estudio
            - SenNum: numero de sensores
            - pth: ruta donde al folder donde se encuentran los archivos CSV
            - PMType: tipo de material particulado
        @return: Nada, unicamente hace una grafica
    '''
    path=pth
    P1_ATM = []
    Lateral = []
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    for i in range (1,SenNum+1):
        time = tiempo
        try:     
            with open(path+'\S'+str(i)+".csv", 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                P1_ATM_IND = []
                lower_time_limit = str(hora_de_estudio)+":00"
                upper_time_limit = str(hora_de_estudio)+":01"
                #mismo valor que el limite inferior
                for row in reader:
                    utcstr = (row.get('UTCDateTime').strip('z').replace('T', ' '))
                    utc = datetime.strptime(utcstr, '%Y/%m/%d %H:%M:%S').replace(tzinfo=from_zone)
                    mx_time = (utc.astimezone(to_zone)).strftime("%H:%M")
                    #print(mx_time)
                    if time<tiempo and time > 0:
                        P1_ATM_IND.append(float(row.get(PMType)))
                        time = time -1
                    elif (mx_time == lower_time_limit) or (mx_time==upper_time_limit):
                        '''
                        PM 1.0 CF: pm1_0_cf_1	
                        PM 2.5 CF: pm2_5_cf_1	
                        PM 10.0 CF: pm10_0_cf_1	
                        PM 1.0 ATM: pm1_0_atm	
                        PM 2.5 ATM: pm2_5_atm	
                        PM 10 ATM: pm10_0_atm
                        '''
                        P1_ATM_IND.append(float(row.get('pm2_5_atm')))
                        time = time -1
        except:
            P1_ATM_IND = [0]
                        
        #print(P1_ATM_IND)
        P1_ATM.append(avg(P1_ATM_IND))
    #print(P1_ATM)
    scamap = plt.cm.ScalarMappable(cmap='inferno')
    fcolors = scamap.to_rgba(max(P1_ATM))
    for h in range (columns):
        #print(columns)
        #print(P1_ATM[(h*rows):((h*rows)+rows)])
        Lateral.append(avg(P1_ATM[(h*rows):((h*rows)+rows)]))
    y_axis = np.arange(0,columns*depth_length,depth_length)
    size_scatter = [100 for n in range(len(y_axis))]
    #print(Lateral)
    #print(y_axis)
    plt.plot(y_axis, Lateral,color='black', alpha=0.5)
    sc=plt.scatter(y_axis, Lateral, s=size_scatter, c=Lateral,alpha=1,facecolors=fcolors, cmap='inferno')
    plt.colorbar(sc)
    plt.xlabel('Profundidad (m)')
    plt.ylabel('ug/m')
    plt.gca().invert_xaxis()
    plt.show()

def animate(i, measurements, x_axis, y_axis,ax1,columns,rows,lateral_length,depth_length):
    '''
        @name: animate
        @brief: Funcion para generar una animacion a partir de las mediciones de PM en una cantidad definidad 
                de tiempo.
        @param: 
            - i: Duracion de la animacion
            - measurements: medificiones de material particulado
            - x_axis: distribucion de datos en el eje x (lateral)
            - y_axis: distribucion de datos en el eje y (profundidad)
            - ax1: figura que se graficara
            - columns: numero de columnas en el arreglos de sensores
            - rows: numero de filas en el arreglo de sensores
            - lateral_length: longitud entre columnas
            - depth_length: longitud entre filas
        @return: Nada, unicamente genera una animación
    '''
    result_num = len(measurements[0])
    z_axis = []
    for k in range(len(measurements)):
        #print(k)
        #print(i)
        #print(measurements[k][i])
        z_axis.append(measurements[k][i])
    #print(z_axis)
    minimum = min(z_axis)
    maximum = max(z_axis)
    average = avg(z_axis)
    textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3  Promedio: "+str(average)+" ug/m3"

    ax1.clear()
    ax1.annotate(textstr,
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=10, ha='center', va='bottom')
    #ax2.scatter3D(x_axis, y_axis, P1_ATM_INDS, c=P1_ATM_INDS, cmap='Greens');
    #ax2.plot3D(x_axis, y_axis, P1_ATM_INDS, 'green');
    scamap = plt.cm.ScalarMappable(cmap='inferno')
    fcolors = scamap.to_rgba(maximum)
    size_scatter = [100 for n in range(len(x_axis))]
    ax1.scatter3D(x_axis, y_axis, z_axis, s=size_scatter, c=z_axis, facecolors=fcolors, cmap='inferno')
    x_axis = np.reshape(x_axis,(columns,rows))
    y_axis = np.reshape(y_axis,(columns,rows))
    z_axis = np.reshape(z_axis,(columns,rows))
    x_final = int((rows-1)*lateral_length)
    y_final = int((columns-1)*depth_length)
    #el parametro j establece que tantos puntos se interpolaran entre el inicio y final -- añadir a parametro a escoger en el GUI
    xnew, ynew = np.mgrid[0:x_final:40j, 0:y_final:40j]
    #si son muy poquitos datos se tiene que agregar dentro del parentesis de "bisplrep" kx=2 y ky=1, se pueden cambiar sus valores para mejorar la interpolación
    tck = interpolate.bisplrep(x_axis, y_axis, z_axis, s=0)
    znew = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)
    ax1.plot_surface(xnew, ynew, znew,cmap=cm.inferno, linewidth=0, antialiased=False, rcount=500, ccount=500)
    #ax1.plot_trisurf(x_axis, y_axis, z_axis, edgecolor='none',facecolors=fcolors, cmap='inferno')
    ax1.set_xlabel('Carretera (m)')
    ax1.set_ylabel('Profundidad (m)')
    ax1.set_zlabel('ug/m3')
    plt.title(str(i))	

def AnimationCSV(columns, rows, lateral_length, depth_length, hora_de_estudio, tiempo, SenNum, AniTime,PMType,pth):
    '''
        @name: AnimationCSV
        @brief: Funcion para generar proveer los componentes necesarios a animate() para generar la animación.
                Esta funcion utiliza archivos CSV
        @param: 
            - columns: numero de columnas en el arreglos de sensores
            - rows: numero de filas en el arreglo de sensores
            - lateral_length: longitud entre columnas
            - depth_length: longitud entre filas
            - hora_de estudio: hora inicial de recoleccion de datos
            - tiempo: tiempo que duro el estudio
            - SenNum: numero de sensores
            - AniTime: duracion de la animacion
            - PMType: tipo de material particulado
            - pth: ruta donde al folder donde se encuentran los archivos CSV
        @return: Nada, unicamente llama a la funcion animate
    '''
    path=pth
    P1_ATM = []
    Lateral = []
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    fig, ax = plt.subplots()
    ax1 = plt.axes(projection='3d')
    for i in range (1,SenNum+1):
        time = tiempo
        try:     
            with open(path+'\S'+str(i)+".csv", 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                P1_ATM_IND = []
                lower_time_limit = str(hora_de_estudio)+":00"
                upper_time_limit = str(hora_de_estudio)+":01"
                #mismo valor que el limite inferior
                for row in reader:
                    utcstr = (row.get('UTCDateTime').strip('z').replace('T', ' '))
                    utc = datetime.strptime(utcstr, '%Y/%m/%d %H:%M:%S').replace(tzinfo=from_zone)
                    mx_time = (utc.astimezone(to_zone)).strftime("%H:%M")
                    #print(mx_time)
                    if time<tiempo and time > 0:
                        P1_ATM_IND.append(float(row.get(PMType)))
                        time = time -1
                    elif (mx_time == lower_time_limit) or (mx_time==upper_time_limit):
                        P1_ATM_IND.append(float(row.get(PMType)))
                        time = time -1
        except:
            P1_ATM_IND = []
            for i in range (tiempo):
                P1_ATM_IND.append(0)
                        
        #print(P1_ATM_IND)
        P1_ATM.append(P1_ATM_IND)
    #print(P1_ATM)
    x_axis=(list(range(0,rows))*columns)
    x_axis = [element * lateral_length for element in x_axis]
    column_with_interval = np.arange(0,columns*depth_length,depth_length)
    y_axis = np.concatenate([([t]*rows) for t in column_with_interval], axis=0)    
    ani = animation.FuncAnimation(fig, animate, interval=(int(AniTime*6000/(len(P1_ATM[0])))),fargs=(P1_ATM,x_axis,y_axis,ax1,columns,rows,lateral_length,depth_length),frames=len(P1_ATM[0]))
    #ani.save("demo2.gif", writer='imagemagick')
    plt.show()

def AnimationPA(columns, rows, lateral_length, depth_length, NumDatos, SenNum, AniTime,PMType):
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
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    P1_ATM_MULT_VECTOR = []
    x_axis=(list(range(0,rows))*columns)
    x_axis = [element * lateral_length for element in x_axis]
    column_with_interval = np.arange(0,columns*depth_length,depth_length)
    y_axis = np.concatenate([([t]*rows) for t in column_with_interval], axis=0)
    for j in range(SenNum):
        TSobject = Thingspeak(read_api_key=keys[j], channel_id=channel_ids[j])
        data,c= TSobject.read_one_sensor(result=NumDatos)
        P1_ATM_IND = []
        time = []
        time_utc = []
        #print(c)
        for i in data:
                P1_ATM_IND.append(float(i[PMType]))
                utcstr = i['created_at'].strip('Z').replace('T', ' ')
                time_utc.append(utcstr)
                utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
                time.append(utc.astimezone(to_zone))
        #print(utcstr)
        P1_ATM_MULT_VECTOR.append(P1_ATM_IND)
        z_axis = P1_ATM_MULT_VECTOR

    #function to animate the plot and update it (using the animate function) every certain amount of milliseconds
    ani = animation.FuncAnimation(fig, animate, interval=(int(AniTime*6000/(len(z_axis[0])))),fargs=(z_axis,x_axis,y_axis,ax1,columns,rows,lateral_length,depth_length),frames=len(z_axis[0]))
    #print plot
    plt.show()

def GraphAvgPA(columns, rows, lateral_length, depth_length, NumDatos, SenNum,PMType):
    '''
        @name: GraphAvgPA
        @brief: Funcion para generar la grafica de promedios a traves de una cantidad definida de tiempo 
                utilizando datos de canales de thingspeak
        @param: 
            - columns: numero de columnas en el arreglos de sensores
            - rows: numero de filas en el arreglo de sensores
            - lateral_length: longitud entre columnas
            - depth_length: longitud entre filas
            - NumDatos: numero de datos recolectados de cada sensor (empezando por ultima medición)
            - SenNum: numero de sensores
            - PMType: tipo de material particulado
        @return: Nada, unicamente hace una grafica y genera un archivo de texto con información general
    '''
    P1_ATM_MULT = []
    fig, ax = plt.subplots()
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    Data_Length=[]
    for j in range(SenNum):
        TSobject = Thingspeak(read_api_key=keys[j], channel_id=channel_ids[j])
        data,c= TSobject.read_one_sensor(result=NumDatos)
        Data_Length.append(len(data))
        P1_ATM_IND = []
        time = []
        time_utc = []
        #print(c)
        for i in data:
                P1_ATM_IND.append(float(i[PMType]))
                utcstr = i['created_at'].strip('Z').replace('T', ' ')
                time_utc.append(utcstr)
                utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
                time.append(utc.astimezone(to_zone))
        #print(time[0])
        #print(time[len(time)-1])
        P1_ATM_MULT.append(avg(P1_ATM_IND))

    plt_dates = dates.date2num(list(time))

    x_axis=(list(range(0,rows))*columns)
    x_axis = [element * lateral_length for element in x_axis]
    column_with_interval = np.arange(0,columns*depth_length,depth_length)
    y_axis = np.concatenate([([t]*rows) for t in column_with_interval], axis=0)
    z_axis = P1_ATM_MULT
    #P1_ATM_INDS = list(chain(*P1_ATM_MULT))
    ax2 = plt.axes(projection='3d')

    fils = open("PurpleAir.txt", "w")
    fils.write(str(Data_Length) + os.linesep)
    fils.write(str(time[0])+ os.linesep)
    fils.write(str(time[len(time)-1])+ os.linesep)
    fils.close()

    minimum = min(z_axis)
    maximum = max(z_axis)
    average = avg(z_axis)

    textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3  Promedio: "+str(average)+" ug/m3"


    ax2.annotate(textstr,
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=10, ha='center', va='bottom')
    scamap = plt.cm.ScalarMappable(cmap='inferno')
    fcolors = scamap.to_rgba(maximum)
    size_scatter = [100 for n in range(len(x_axis))]
    ax2.scatter3D(x_axis, y_axis, z_axis, s=size_scatter, c=z_axis, facecolors=fcolors, cmap='inferno')
    #ax2.plot3D(x_axis, y_axis, P1_ATM, 'green')
    x_axis = np.reshape(x_axis,(columns,rows))
    y_axis = np.reshape(y_axis,(columns,rows))
    z_axis = np.reshape(z_axis,(columns,rows))
    x_final = int((rows-1)*lateral_length)
    y_final = int((columns-1)*depth_length)
    #el parametro j establece que tantos puntos se interpolaran entre el inicio y final -- añadir a parametro a escoger en el GUI
    xnew, ynew = np.mgrid[0:x_final:40j, 0:y_final:40j]
    #si son muy poquitos datos se tiene que agregar dentro del parentesis de "bisplrep" kx=2 y ky=1, se pueden cambiar sus valores para mejorar la interpolación
    tck = interpolate.bisplrep(x_axis, y_axis, z_axis, s=0)
    znew = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)
    ax2.plot_surface(xnew, ynew, znew,cmap=cm.inferno, linewidth=0, antialiased=False, rcount=500, ccount=500)
    ax2.set_xlabel('Carretera (m)')
    ax2.set_ylabel('Profundidad (m)')
    ax2.set_zlabel('ug/m3')
    plt.title("Promedio de "+ str((NumDatos)*2) + " mins a partir de las "+ str(time[0])+" hrs")
    m = cm.ScalarMappable(cmap=cm.inferno)
    m.set_array(znew)	
    plt.colorbar(m, ax=ax2)
    plt.show()
    #print([s.strip('Z') for s in time])
    #current_time = datetime.datetime.fromtimestamp(time)