from dateutil.rrule import rrule,SECONDLY
import datetime

def date_list(start, end):
    datestring =[]
    dates = [dt for dt in rrule(SECONDLY, dtstart=start, until=end)]
    for j in dates:
        datestring.append(j.strftime("%m-%d-%Y %H:%M:%S"))
    return datestring

x=date_list(datetime.datetime(2015,12,28,15,0,0), datetime.datetime(2015,12,28,15,1,0))
print(x)