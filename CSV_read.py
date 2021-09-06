from datetime import datetime
from dateutil import tz
import matplotlib.dates as dates
import  matplotlib.pyplot as plt
import numpy as np
import pytz
import csv
MX = pytz.timezone('America/Monterrey')
formatter = dates.DateFormatter('%m/%d %H:%M ',tz=MX)
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
time_interval = 45
font = {'family': 'Arial',
        'color':  'black',
        'weight': 'bold',
        'size': 14,
        }
time=[]
P1_ATM_IND = []
P10_ATM_IND = []
P25_ATM_IND = []
with open('Test.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        utcstr = (row.get('UTCDateTime').strip('z').replace('T', ' '))
        utc = datetime.strptime(utcstr, '%Y/%m/%d %H:%M:%S').replace(tzinfo=from_zone)
        time.append(utc.astimezone(to_zone))
        P1_ATM_IND.append(float(row.get('pm1_0_atm')))
        P10_ATM_IND.append(float(row.get('pm10_0_atm')))
        P25_ATM_IND.append(float(row.get('pm2_5_atm')))

plt_dates = dates.date2num(list(time))
#print(plt_dates)
fig, ax = plt.subplots()
plt.plot(time,P1_ATM_IND, label = "PM1.0 (ATM)")
plt.plot(time,P25_ATM_IND, label = "PM2.5 (ATM)")
plt.plot(time,P10_ATM_IND, label = "PM10 (ATM)")
plt.legend()
plt.yticks(np.arange(0, max(P10_ATM_IND), 20))
plt.xlabel("Tiempo",fontdict=font)
plt.ylabel("ug/m3",fontdict=font)
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_tick_params(rotation=30, labelsize=8)
ax.xaxis.set_major_locator(dates.MinuteLocator(interval=time_interval))
plt.show()
