import PySimpleGUI as sg
import pandas as pd

"""main_layout = [
[sg.Text('Archivo')], [sg.Input(key="file"), sg.FileBrowse(), sg.OK(key="OK"), 
sg.Button('Cancelar')],
[sg.Listbox(values=[], key='universidades', size=(60, 10))],
[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), 
background_color='red', key='graph')],
[sg.ReadButton('Ordenar', key='_Listo_', disabled=True)]
]"""

main_layout = [[sg.Text('Sensores',justification='center', font=("Times New Roman", 18))],
                ]

window = sg.Window('',main_layout, size=(720,480), grab_anywhere=True)
while True:
    event, value = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break

#df = pd.read_csv('D:\Descargas HDD\GIECC_UCMEXUS_02 (outside) (25.650697 -100.290968) Primary Real Time 04_06_2022 04_07_2022.csv')
#print(df)