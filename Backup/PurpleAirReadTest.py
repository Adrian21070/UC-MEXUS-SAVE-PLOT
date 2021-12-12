from datetime import datetime
from dateutil import tz
import matplotlib.dates as dates
import  matplotlib.pyplot as plt
from TSclasses import *
import pytz
import numpy as np
import time as tm
from mpl_toolkits.mplot3d import Axes3D

r_key = 'HZEGJA0LWH5HYCBW'
channel_id = 141675
"""
    PURPLE AIR SENSOR ID: 195
    LINK: https://www.purpleair.com/json?show=195
    ALL THE SENSORS: https://www.purpleair.com/data.json
    THINGSPEAK_SECONDARY_ID:141676
    THINGSPEAK_SECONDARY_ID_READ_KEY:9811MD4QCUF6I4SR
"""
time = []
time_utc = []
P1_ATM = []
P25_ATM = []
P10_ATM = []
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
MX = pytz.timezone('America/Monterrey')
formatter = dates.DateFormatter('%m/%d %H:%M ',tz=MX)
time_interval = 30
result_num = 50

font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }

ob = Thingspeak(read_api_key=r_key, channel_id=channel_id)
data,channel = ob.read_one_sensor(result=result_num)

for i in data:
        P1_ATM.append(float(i['field1']))
        P25_ATM.append(float(i['field2']))
        P10_ATM.append(float(i['field3']))
        utcstr=i['created_at'].strip('Z').replace('T',' ')
        time_utc.append(utcstr)
        utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
        time.append(utc.astimezone(to_zone))

print(channel)
#print(time)
#print(time_utc)
plt_dates = dates.date2num(list(time))
#print(plt_dates)
fig, ax = plt.subplots()
plt.plot(time,P1_ATM, label = "PM1.0 (ATM)")
plt.plot(time,P25_ATM, label = "PM2.5 (ATM)")
plt.plot(time,P10_ATM, label = "PM10 (ATM)")
plt.legend()
plt.yticks(np.arange(0, max(P10_ATM), 4))
plt.xlabel("Tiempo",fontdict=font)
plt.ylabel("ug/m3",fontdict=font)
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_tick_params(rotation=30, labelsize=8)
ax.xaxis.set_major_locator(dates.MinuteLocator(interval=time_interval))
plt.show()

axis_length=np.arange(len(P1_ATM))
x_axis = [*axis_length,*axis_length,*axis_length]
y_axis = [0]*len(P1_ATM)+[1]*len(P1_ATM)+[2]*len(P1_ATM)
P1_ATMS= [*P1_ATM,*P25_ATM,*P10_ATM]
ax2 = plt.axes(projection='3d')
#ax2.scatter3D(x_axis, y_axis, P1_ATMS, c=P1_ATMS, cmap='Greens');
#ax2.plot3D(x_axis, y_axis, P1_ATMS, 'green');
ax2.plot_trisurf(x_axis, y_axis, P1_ATMS, cmap='viridis', edgecolor='none');
plt.show()
#print([s.strip('Z') for s in time])
#current_time = datetime.datetime.fromtimestamp(time)