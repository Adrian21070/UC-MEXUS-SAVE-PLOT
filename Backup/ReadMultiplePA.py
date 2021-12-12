from datetime import datetime
from dateutil import tz
import matplotlib.dates as dates
import  matplotlib.pyplot as plt
from TSclasses import *
import pytz
import numpy as np
from itertools import chain
from mpl_toolkits.mplot3d import Axes3D

"""
    PURPLE AIR DOCUMENTATION: https://docs.google.com/document/d/15ijz94dXJ-YAZLi9iZ_RaBwrZ4KtYeCy08goGBwnbCU/edit
    PURPLE AIR SENSOR ID: 195,196
    LINK: https://www.purpleair.com/json?show=195
    ALL THE SENSORS: https://www.purpleair.com/data.json
    THINGSPEAK_SECONDARY_ID:141676
    THINGSPEAK_SECONDARY_ID_READ_KEY:9811MD4QCUF6I4SR
"""

P1_ATM_MULT = []
P25_ATM_MULT = []
P10_ATM_MULT = []
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
MX = pytz.timezone('America/Monterrey')
formatter = dates.DateFormatter('%m/%d %H:%M ',tz=MX)
time_interval = 30
result_num = 100

font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

keys = ['I6HHDN7MGBXGECUH', 'WD8JU2VCW5WLIGUM',"CPGRHJ0EEFFTFBX5"]
#primario y despues secundario
channel_ids =[1066387, 958808,1066274]

for j in range(len(keys)):
    TSobject = Thingspeak(read_api_key=keys[j], channel_id=channel_ids[j])
    data,c= TSobject.read_one_sensor(result=result_num)
    P1_ATM_IND = []
    P25_ATM_IND = []
    P10_ATM_IND = []
    time = []
    time_utc = []
    #print(c)
    for i in data:
            P1_ATM_IND.append(float(i['field1']))
            P25_ATM_IND.append(float(i['field2']))
            P10_ATM_IND.append(float(i['field3']))
            utcstr = i['created_at'].strip('Z').replace('T', ' ')
            time_utc.append(utcstr)
            utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
            time.append(utc.astimezone(to_zone))
    #print(utcstr)
    P1_ATM_MULT.append(P1_ATM_IND)
    P10_ATM_MULT.append(P10_ATM_IND)
    P25_ATM_MULT.append(P25_ATM_IND)

channel = c
plt_dates = dates.date2num(list(time))
fig, ax = plt.subplots()

for k in range(len(keys)):
    plt.plot(time,P1_ATM_MULT[k], label = "PM1.0 (ATM) "+str(k))
    plt.plot(time,P25_ATM_MULT[k], label = "PM2.5 (ATM) "+str(k))
    plt.plot(time,P10_ATM_MULT[k], label = "PM10 (ATM) "+str(k))
plt.legend()
#plt.yticks(np.arange(0, max(P10_ATM_MULT[0]), 4))
plt.xlabel("Tiempo",fontdict=font)
plt.ylabel("ug/m3",fontdict=font)
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_tick_params(rotation=30, labelsize=8)
ax.xaxis.set_major_locator(dates.MinuteLocator(interval=time_interval))
plt.show()

x_axis=(list(range(0,len(P1_ATM_IND)))*len(P10_ATM_MULT))
x_axis = [element * 6 for element in x_axis]
#print(x_axis)
columns = np.arange(0,len(P10_ATM_MULT)*6,6)
y_axis = np.concatenate([([t]*result_num) for t in columns], axis=0)
#print(y_axis)
P1_ATM_INDS = list(chain(*P1_ATM_MULT))
ax2 = plt.axes(projection='3d')
#ax2.scatter3D(x_axis, y_axis, P1_ATM_INDS, c=P1_ATM_INDS, cmap='Greens');
#ax2.plot3D(x_axis, y_axis, P1_ATM_INDS, 'green');
ax2.plot_trisurf(x_axis, y_axis, P1_ATM_INDS, cmap='viridis', edgecolor='none');
plt.show()
#print([s.strip('Z') for s in time])
#current_time = datetime.datetime.fromtimestamp(time)