import PySimpleGUI as sg
from matplotlib import projections
import pandas as pd
from scipy import interpolate
from scipy.interpolate import griddata
import numpy as np
import matplotlib.pyplot as plt
"""main_layout = [
[sg.Text('Archivo')], [sg.Input(key="file"), sg.FileBrowse(), sg.OK(key="OK"), 
sg.Button('Cancelar')],
[sg.Listbox(values=[], key='universidades', size=(60, 10))],
[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), 
background_color='red', key='graph')],
[sg.ReadButton('Ordenar', key='_Listo_', disabled=True)]
]"""
"""
main_layout = [[sg.Text('Sensores',justification='center', font=("Times New Roman", 18))],
                ]

window = sg.Window('',main_layout, size=(720,480), grab_anywhere=True)
while True:
    event, value = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
"""
fig,ax1=plt.subplots()
ax1=plt.axes(projection="3d")
y_axis = [0.0,4.0,8.0,12.0,16.0]
filas = [2,3.42435,3.34465,3.141,4]
z = [1,2,3,4,5]
#y_axis = [0.0,4.0,8.0]
#filas = [3.42435,3.34465,3.141]
#f = interpolate.interp1d(y_axis, filas, kind='cubic')
#x = np.arange(0, max(y_axis), 0.1)
ax1.plot(filas,y_axis,z)
ax1.set_xlim3d(2,3.5)
ax1.set_ylim3d(0,5)
ax1.set_zlim3d(1,3)
plt.show()


#df = pd.read_csv('D:\Descargas HDD\GIECC_UCMEXUS_02 (outside) (25.650697 -100.290968) Primary Real Time 04_06_2022 04_07_2022.csv')
#print(df)