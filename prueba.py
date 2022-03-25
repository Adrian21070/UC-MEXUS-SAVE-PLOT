import csv
from datetime import datetime
from dateutil import tz

hora_de_estudio = 22
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
tiempo = 60
time = 60
PMType = 'field8'
with open('feeds.csv') as csv_file:
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