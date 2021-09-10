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

columns = 4
rows = 3
lower_time_limit = "10:30"
upper_time_limit = "10:31"

font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

path = "D:\Instituto Tecnologico y de Estudios Superiores de Monterrey\Moisés Alejandro Leyva Sanjuan - UCMEXUS\Mediciones prueba\S"

def avg(lst):
    return round(sum(lst) / len(lst),2)

for i in range (1,9):
    with open(path+str(i)+"\\20210904.csv", 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            utcstr = (row.get('UTCDateTime').strip('z').replace('T', ' '))
            utc = datetime.strptime(utcstr, '%Y/%m/%d %H:%M:%S').replace(tzinfo=from_zone)
            mx_time = (utc.astimezone(to_zone)).strftime("%H:%M")
            if (mx_time == lower_time_limit) or (mx_time==upper_time_limit):
                P1_ATM.append(float(row.get('pm1_0_atm')))
    #Borrar cuando se añadan mas sensores
    if i == 6 or i == 8:
        P1_ATM.append(0)
    elif i == 7:
        P1_ATM.append(0)
        P1_ATM.append(0)
    #print(P1_ATM)

minimum = min(P1_ATM)
maximum = max(P1_ATM)
average = avg(P1_ATM)
textstr = "Max: "+str(maximum)+" ug/m3  Min: "+str(minimum)+" ug/m3  Promedio: "+str(average)+" ug/m3"

fig, ax = plt.subplots()

#creation of list with the components for the x axis of the plot
x_axis=(list(range(0,rows))*columns)
x_axis = [element * 6 for element in x_axis]

#creation of a list with the component for the y axis of the plot
column_with_interval = np.arange(0,columns*6,6)
y_axis = np.concatenate([([t]*rows) for t in column_with_interval], axis=0)

#print(y_axis)
ax2 = plt.axes(projection='3d')

ax2.annotate(textstr,
        xy=(0.5, 0), xytext=(0, 10),
        xycoords=('axes fraction', 'figure fraction'),
        textcoords='offset points',
        size=10, ha='center', va='bottom')

#ax2.scatter3D(x_axis, y_axis, P1_ATM, c=P1_ATM, cmap='Greens')
#ax2.plot3D(x_axis, y_axis, P1_ATM, 'green')
ax2.plot_trisurf(x_axis, y_axis, P1_ATM, cmap='viridis', edgecolor='none')
plt.title(lower_time_limit)	
plt.show()
#print([s.strip('Z') for s in time])
#current_time = datetime.datetime.fromtimestamp(time)