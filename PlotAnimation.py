#importing libraries
from datetime import datetime
from dateutil import tz
import matplotlib.dates as dates
import  matplotlib.pyplot as plt
from TSclasses import *
import pytz
import numpy as np
from itertools import chain
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

P1_ATM_MULT_VECTOR = []
time = []
time_utc = []
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
columns = 3
rows = 3
animation_counter = 0
result_num = 20

keys = ['I6HHDN7MGBXGECUH', 'WD8JU2VCW5WLIGUM',"CPGRHJ0EEFFTFBX5", "LGKHV8ANQZFC1Q84","NCJQ0WH0K6A9FWRP",
        "TK0MF8MQ874GEOMD", "G7RGPVGM9XZG1KIJ", "TU6M4KIO9VGXMGSJ", "OFD7LYESIC6ORDAF"]
#primario y despues secundario
channel_ids =[1066387, 958808,1066274,870317, 871042,873018, 978296, 833190,893120]


x_axis=(list(range(0,rows))*columns)
x_axis = [element * 6 for element in x_axis]
column_with_interval = np.arange(0,columns*6,6)
y_axis = np.concatenate([([t]*rows) for t in column_with_interval], axis=0)

fig, ax = plt.subplots()
ax1 = plt.axes(projection='3d')
#creating a subplot 

def animate(i):
    global animation_counter,result_num
    z_axis = []
    shown_time = time[animation_counter]
    for k in range(len(keys)):
        z_axis.append(P1_ATM_MULT_VECTOR[k][animation_counter])
    animation_counter+=1
    if animation_counter==result_num:
        animation_counter=0
    
    ax1.clear()
    #ax2.scatter3D(x_axis, y_axis, P1_ATM_INDS, c=P1_ATM_INDS, cmap='Greens');
    #ax2.plot3D(x_axis, y_axis, P1_ATM_INDS, 'green');
    ax1.plot_trisurf(x_axis, y_axis, z_axis, cmap='viridis', edgecolor='none');
    plt.title(str(shown_time))	
	
for j in range(len(keys)):
    TSobject = Thingspeak(read_api_key=keys[j], channel_id=channel_ids[j])
    data,c= TSobject.read_one_sensor(result=result_num)
    P1_ATM_IND = []
    time = []
    time_utc = []
    #print(c)
    for i in data:
            P1_ATM_IND.append(float(i['field1']))
            utcstr = i['created_at'].strip('Z').replace('T', ' ')
            time_utc.append(utcstr)
            utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
            time.append(utc.astimezone(to_zone))
    #print(utcstr)
    P1_ATM_MULT_VECTOR.append(P1_ATM_IND)


ani = animation.FuncAnimation(fig, animate, interval=1000) 
plt.show()