#importing libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from dateutil import tz
import matplotlib.dates as dates
from TSclasses import *
import pytz
import numpy as np
import time as tm
from mpl_toolkits.mplot3d import Axes3D

r_key = 'HZEGJA0LWH5HYCBW'
channel_id = 141675

time = []
time_utc = []
P1_ATM = []
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
MX = pytz.timezone('America/Monterrey')
formatter = dates.DateFormatter('%m/%d %H:%M ',tz=MX)
time_interval = 5
result_num = 20

font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }


fig, ax = plt.subplots()

def animate(i):
    global utcstr
    ob_inc = Thingspeak(read_api_key=r_key, channel_id=channel_id)
    data_inc,channel_inc = ob_inc.read_one_sensor(result=1)
    #print(data_inc)
    print(time_utc[len(time_utc)-1])
    print(data_inc[0]['created_at'])
    if (str(data_inc[0]['created_at'].strip('Z').replace('T',' '))!=str(time_utc[len(time_utc)-1])):
        P1_ATM.append(float(data_inc[0]['field1']))
        utcstr=data_inc[0]['created_at'].strip('Z').replace('T',' ')
        time_utc.append(utcstr)
        utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
        time.append(utc.astimezone(to_zone))
    
    #print(P1_ATM)
    ax.clear()
    plt_dates = dates.date2num(list(time))
    plt.plot(time,P1_ATM, label = "PM1.0 (ATM)")
    plt.legend()
    plt.xlabel("Tiempo",fontdict=font)
    plt.ylabel("ug/m3",fontdict=font)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=8)
    #ax.xaxis.set_major_locator(dates.MinuteLocator(interval=time_interval))
	
    
ob = Thingspeak(read_api_key=r_key, channel_id=channel_id)
data,channel = ob.read_one_sensor(result=result_num)

for i in data:
        P1_ATM.append(float(i['field1']))
        utcstr=i['created_at'].strip('Z').replace('T',' ')
        time_utc.append(utcstr)
        utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
        time.append(utc.astimezone(to_zone))

#P1_ATM.reverse()
ani = animation.FuncAnimation(fig, animate, interval=1000*60*2.1) 
plt.show()