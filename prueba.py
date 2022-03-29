"""import csv
from datetime import datetime
from dateutil import tz
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.animation as animation"""
"""sg.theme("DarkTanBlue")
options = [[sg.Frame('Disposición', [[sg.Input(f'{row}, {col}', key=f'{row}, {col}') for col in range(4)] for row in range(4)])],
            [sg.Button('Submit', font=('Times New Roman',12))]]
taa = [sg.Button('OK')]
layout8 = [[sg.Input(f'{row}, {col}', key=f'{row}, {col}') for col in range(4)] for row in range(4)]

#layout = [[sg.Column(layout8)]]

layout = [[sg.Column(options)]]

window = sg.Window('Proyecto UCMEXUS', layout)

while True:
    event, values = window.read()"""
"""
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
"""
"""
from matplotlib import projections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

TWOPI = 2*np.pi

fig, ax = plt.subplots()

t = np.linspace(0, 10, 100)

#y = np.linspace(0, 10, 100)
#t = np.arange(0.0, TWOPI, 0.001)

x = np.sin(t)
y = np.cos(t)
z = np.sin(t)

x = [0, 4, 8, 12, 16]
y = [0, 2, 4, 6, 8]
z = [[12.1, 10.9, 5.1, 8, 10], [9.1, 7.9, 4.1, 12, 7]]

ax = plt.axes(projection = '3d')

def animate(i,x,y,z):
    ax.scatter3D(x,y,z[i])

# create animation using the animate() function
myAnimation = animation.FuncAnimation(fig, animate, frames=len(z), fargs = (x,y,z),
                                      interval=2000, repeat = False)

plt.show()
"""
import PySimpleGUI as sg

"""
    Simple test harness to demonstate how to use the CalendarButton and the get date popup
"""
# sg.theme('Dark Red')
layout = [[sg.Text('Date Chooser Test Harness', key='-TXT-')],
      [sg.Input(key='-IN-', size=(20,1)), sg.CalendarButton('Cal US No Buttons Location (0,0)', close_when_date_chosen=True,  target='-IN-', location=(0,0), no_titlebar=False, )],
      [sg.Input(key='-IN3-', size=(20,1)), sg.CalendarButton('Cal Monday', title='Pick a date any date', no_titlebar=True, close_when_date_chosen=False,  target='-IN3-', begin_at_sunday_plus=1, month_names=('студзень', 'люты', 'сакавік', 'красавік', 'май', 'чэрвень', 'ліпень', 'жнівень', 'верасень', 'кастрычнік', 'лістапад', 'снежань'), day_abbreviations=('Дш', 'Шш', 'Шр', 'Бш', 'Жм', 'Иш', 'Жш'))],
      [sg.Input(key='-IN2-', size=(20,1)), sg.CalendarButton('Cal German Feb 2020',  target='-IN2-',  default_date_m_d_y=(2,None,2020), locale='de_DE', begin_at_sunday_plus=1 )],
      [sg.Input(key='-IN4-', size=(20,1)), sg.CalendarButton('Cal Format %m-%d Jan 2020',  target='-IN4-', format='%y-%m-%d', default_date_m_d_y=(1,None,2020), )],
      [sg.Button('Read'), sg.Button('Date Popup'), sg.Exit()]]
sg.CalendarButton
window = sg.Window('window', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Date Popup':
        sg.popup('You chose:', sg.popup_get_date())
window.close()