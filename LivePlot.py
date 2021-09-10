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
from matplotlib.offsetbox import AnchoredText

r_key = 'HZEGJA0LWH5HYCBW'
channel_id = 141675

'''
    Change Retrieved_Data accordingly:
        Primary Channel:
        PM1.0 (CF=1) ug/m3: "field1"
        PM2.5 (CF=1) ug/m3: "field2"
        PM10.0 (CF=1) ug/m3: "field3"
        PM2.5 (CF=ATM) ug/m3: "field8"

        Secondary Channel:
        PM1.0 (CF=ATM) ug/m3: "field15"
        PM10.0 (CF=ATM) ug/m3: "field16"
'''
Retrieved_Data = "field8"

time = []
time_utc = []
P1_ATM = []
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
MX = pytz.timezone('America/Monterrey')
formatter = dates.DateFormatter('%m/%d %H:%M ',tz=MX)
time_interval = 5
result_num = 100

font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }


fig, ax = plt.subplots()

def avg(lst):
    return round(sum(lst) / len(lst),2)

def animate(i):
    global utcstr
    ob_inc = Thingspeak(read_api_key=r_key, channel_id=channel_id)
    data_inc,channel_inc = ob_inc.read_one_sensor(result=1)
    #print(data_inc)
    print(time_utc[len(time_utc)-1])
    print(data_inc[0]['created_at'])
    if (str(data_inc[0]['created_at'].strip('Z').replace('T',' '))!=str(time_utc[len(time_utc)-1])):
        P1_ATM.append(float(data_inc[0][Retrieved_Data]))
        utcstr=data_inc[0]['created_at'].strip('Z').replace('T',' ')
        time_utc.append(utcstr)
        utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
        time.append(utc.astimezone(to_zone))
    
    minimum = min(P1_ATM)
    maximum = max(P1_ATM)
    average = avg(P1_ATM)

    anchored_text = AnchoredText("Max: "+str(maximum)+" ug/m3\nMin: "+str(minimum)+" ug/m3\nPromedio: "
                                +str(average)+" ug/m3", loc="upper right")

    #print(P1_ATM)
    ax.clear()
    ax.add_artist(anchored_text)
    plt_dates = dates.date2num(list(time))
    plt.plot(time,P1_ATM, label = "PM1.0 (ATM)")
    plt.legend(loc="upper left")
    plt.xlabel("Tiempo",fontdict=font)
    plt.ylabel("ug/m3",fontdict=font)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=8)
    #ax.xaxis.set_major_locator(dates.MinuteLocator(interval=time_interval))
	
    
ob = Thingspeak(read_api_key=r_key, channel_id=channel_id)
data,channel = ob.read_one_sensor(result=result_num)

for i in data:
        P1_ATM.append(float(i[Retrieved_Data]))
        utcstr=i['created_at'].strip('Z').replace('T',' ')
        time_utc.append(utcstr)
        utc = datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
        time.append(utc.astimezone(to_zone))

#P1_ATM.reverse()
ani = animation.FuncAnimation(fig, animate, interval=1000*60*2.1) 
plt.show()