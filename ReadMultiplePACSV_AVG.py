from datetime import datetime
from dateutil import tz
import matplotlib.dates as dates
import  matplotlib.pyplot as plt
from TSclasses import *
import pytz
import numpy as np
from itertools import chain
from mpl_toolkits.mplot3d import Axes3D
import csv

P1_ATM = []
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

columns = 5
rows = 4
lateral_length = 8
depth_length = 10
hora_de_estudio = 14
tiempo = 30

font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

path = "D:\Instituto Tecnologico y de Estudios Superiores de Monterrey\Moisés Alejandro Leyva Sanjuan - UCMEXUS\Mediciones prueba\\20211028\S"

def avg(lst):
    return round(sum(lst) / len(lst),2)

for i in range (1,21):
    time = tiempo
    #Borrar if y else cuando ya no sea necesario
    if i == 11 or i > 17:
         P1_ATM_IND = [0]
    else:     
        with open(path+str(i)+".csv", 'r') as csv_file:
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
                    P1_ATM_IND.append(float(row.get('pm2_5_atm')))
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
                    
    print(P1_ATM_IND)
    P1_ATM.append(avg(P1_ATM_IND))
    #Borrar cuando se añadan mas sensores
    #if i == 6 or i == 8:
    #    P1_ATM.append(0)
    '''
    if i == 7:
        P1_ATM.append(avg(P1_ATM_IND))
        P1_ATM.append(avg(P1_ATM_IND))
    if i == 8:
        P1_ATM.append(avg(P1_ATM_IND))
        P1_ATM.append(avg(P1_ATM_IND))'''
    #print(P1_ATM)

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

ax2.scatter3D(x_axis, y_axis, P1_ATM, s=size_scatter, c=P1_ATM, cmap='Dark2')
#ax2.plot3D(x_axis, y_axis, P1_ATM, 'green')
ax2.plot_trisurf(x_axis, y_axis, P1_ATM, cmap='viridis', edgecolor='none')
ax2.set_xlabel('Carretera (m)')
ax2.set_ylabel('Profundidad (m)')
ax2.set_zlabel('ug/m3')
plt.title("Promedio de"+str(hora_de_estudio)+":00 a "+str(hora_de_estudio)+":59")	
plt.show()
#print([s.strip('Z') for s in time])
#current_time = datetime.datetime.fromtimestamp(time)