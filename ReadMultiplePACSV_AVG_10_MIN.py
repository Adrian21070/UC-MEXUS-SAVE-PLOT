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
P1_ATM_TM = []
mxtm =[]
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

columns = 4
rows = 3

font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

#Cambiar Path de acuerdo a donde se tenga los datos
path = "D:\Instituto Tecnologico y de Estudios Superiores de Monterrey\Moisés Alejandro Leyva Sanjuan - UCMEXUS\Mediciones prueba\S"

def avg(lst):
    return round(sum(lst) / len(lst),2)

#Cambiar numero de sensores
for i in range (1,9):
    #Cambiar fecha del CSV
    with open(path+str(i)+"\\20210904.csv", 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        P1_ATM_IND = []
        mxtm = []
        time_counter=5
        for row in reader:
            utcstr = (row.get('UTCDateTime').strip('z').replace('T', ' '))
            utc = datetime.strptime(utcstr, '%Y/%m/%d %H:%M:%S').replace(tzinfo=from_zone)
            mxtm.append((utc.astimezone(to_zone)).strftime("%H:%M"))
            '''
            PM 1.0 CF: pm1_0_cf_1	
            PM 2.5 CF: pm2_5_cf_1	
            PM 10.0 CF: pm10_0_cf_1	
            PM 1.0 ATM: pm1_0_atm	
            PM 2.5 ATM: pm2_5_atm	
            PM 10 ATM: pm10_0_atm
            '''
            P1_ATM_IND.append(float(row.get('pm2_5_atm')))
    #print(P1_ATM_IND)
    P1_ATM_TM.append(mxtm)
    #print(len(P1_ATM_TM))
    P1_ATM.append(P1_ATM_IND)
    #print(len(P1_ATM))
    #Borrar cuando se añadan mas sensores
    #if i == 6 or i == 8:
    #    P1_ATM.append(0)
    if i == 7:
        P1_ATM.append(P1_ATM_IND)
        P1_ATM.append(P1_ATM_IND)
        P1_ATM_TM.append(mxtm)
        P1_ATM_TM.append(mxtm)
    if i == 8:
        P1_ATM.append(P1_ATM_IND)
        P1_ATM.append(P1_ATM_IND)
        P1_ATM_TM.append(mxtm)
        P1_ATM_TM.append(mxtm)
    #print(P1_ATM)
PLOT_ATM = []
for l in range (len(P1_ATM)):
    lower_time_limit = "10:05"
    upper_time_limit = "10:06"
    for k in range(len(P1_ATM[l])):
        if (P1_ATM_TM[l][k] == lower_time_limit) or (P1_ATM_TM[l][k]==upper_time_limit):
            PLOT_ATM.append(avg(P1_ATM[l][k:k+5]))
            #print(P1_ATM[l][k:k+5])
print((PLOT_ATM))
minimum = min(PLOT_ATM)
maximum = max(PLOT_ATM)
average = avg(PLOT_ATM)
textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3  Promedio: "+str(average)+" ug/m3"

fig, ax = plt.subplots()

#creation of list with the components for the x axis of the plot
x_axis=(list(range(0,rows))*columns)
x_axis = [element * 6 for element in x_axis]

#creation of a list with the component for the y axis of the plot
column_with_interval = np.arange(0,columns*6,6)
y_axis = np.concatenate([([t]*rows) for t in column_with_interval], axis=0)

size_scatter = [100 for n in range(len(x_axis))]

#print(y_axis)
ax2 = plt.axes(projection='3d')

ax2.annotate(textstr,
        xy=(0.5, 0), xytext=(0, 10),
        xycoords=('axes fraction', 'figure fraction'),
        textcoords='offset points',
        size=10, ha='center', va='bottom')

ax2.scatter3D(x_axis, y_axis, PLOT_ATM, s=size_scatter, c=PLOT_ATM, cmap='Dark2')
#ax2.plot3D(x_axis, y_axis, P1_ATM, 'green')
ax2.plot_trisurf(x_axis, y_axis, PLOT_ATM, cmap='viridis', edgecolor='none')
ax2.set_xlabel('Carretera (m)')
ax2.set_ylabel('Profundidad (m)')
ax2.set_zlabel('ug/m3')
plt.title("Promedio de PM2.5 en 10 minutos (" +lower_time_limit+")")	
plt.show()
#print([s.strip('Z') for s in time])
#current_time = datetime.datetime.fromtimestamp(time)