import PySimpleGUI as sg
import AvgFunctions as AF
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

PM_Dict={"PM 1.0 CF": "pm1_0_cf_1",	
         "PM 2.5 CF": "pm2_5_cf_1",	
         "PM 10.0 CF": "pm10_0_cf_1",	
         "PM 1.0 ATM": "pm1_0_atm",	
         "PM 2.5 ATM": "pm2_5_atm",	
         "PM 10.0 ATM" : "pm10_0_atm"}

PA_Dict={"PM 1.0 CF": "field1",	
         "PM 2.5 CF": "field2",	
         "PM 10.0 CF": "field3",
         "PM 2.5 ATM": "field8"}

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

'''
Links relevantes: 
    - https://stackoverflow.com/questions/59500558/how-to-display-different-layouts-based-on-button-clicks-in-pysimple-gui-persis
    - https://stackoverflow.com/questions/63725995/how-to-display-files-in-folder-when-using-pysimplegui-filebrowse-function
'''
# ----------- Create the 3 layouts this Window will display -----------
layout1 = [[sg.Text('Seleccione de donde desea sacar los datos')],
           [sg.Button('Online'),sg.Button("Archivo CSV"),sg.Button("Exit")]]

layout2 = [[sg.Text('Seleccione que desea hacer con el archivo CSV')],
           [sg.Button('Promedio'),sg.Button("Animación"),sg.Button("Exit")]]

layout3 = [[sg.Text('Datos para el promedio (Todos se deben llenar con numeros enteros!)')],
            [sg.Text('Num. de Sensores', size =(22, 1)), sg.InputText(key='NumSen')],
            [sg.Text('Num. Columnas de Sensores', size =(22, 1)), sg.InputText(key='Cols')],
            [sg.Text('Num. Filas de Sensores', size =(22, 1)), sg.InputText(key='Rows')],
            [sg.Text('Distancia entre Columnas', size =(22, 1)), sg.InputText(key='LC')],
            [sg.Text('Distancia entre Filas', size =(22, 1)), sg.InputText(key='LR')],
            [sg.Text('Hora de Inicio (24hrs)', size =(22, 1)), sg.InputText(key='Hora')],
            [sg.Text('Tiempo Monitoreo (Tiempo par en Min.)', size =(28, 1)), sg.InputText(key='Mins')],
            [sg.Text('Selecciona Folder con Datos'),sg.Input(), sg.FolderBrowse('Folder')],
            [sg.Text('Selecciona PM'),sg.Combo(['PM 1.0 CF', 'PM 2.5 CF', 'PM 10.0 CF', 'PM 1.0 ATM', 'PM 2.5 ATM', 'PM 10.0 ATM'], enable_events=True, key='DDMPCSV')],
            [sg.Button("Graficar Promedio CSV"),sg.Button("Gráfica Lateral"),sg.Button("Exit")]]

layout4 = [[sg.Text('Datos para la animación (Todos se deben llenar con numeros enteros!)')],
            [sg.Text('Num. de Sensores', size =(22, 1)), sg.InputText(key='NumSenACSV')],
            [sg.Text('Num. Columnas de Sensores', size =(22, 1)), sg.InputText(key='ColsACSV')],
            [sg.Text('Num. Filas de Sensores', size =(22, 1)), sg.InputText(key='RowsACSV')],
            [sg.Text('Distancia entre Columnas', size =(22, 1)), sg.InputText(key='LCACSV')],
            [sg.Text('Distancia entre Filas', size =(22, 1)), sg.InputText(key='LRACSV')],
            [sg.Text('Hora de Inicio (24hrs)', size =(22, 1)), sg.InputText(key='HoraACSV')],
            [sg.Text('Tiempo Monitoreo (Tiempo par en Min.)', size =(28, 1)), sg.InputText(key='MinsACSV')],
            [sg.Text('Tiempo Duración Animación (Min.)', size =(28, 1)), sg.InputText(key='AniTime')],
            [sg.Text('Concentración de Material Particulado')],
            [sg.Text('Selecciona Folder con Datos'),sg.Input(), sg.FolderBrowse('Carpeta')],
            [sg.Text('Selecciona PM'),sg.Combo(['PM 1.0 CF', 'PM 2.5 CF', 'PM 10.0 CF', 'PM 1.0 ATM', 'PM 2.5 ATM', 'PM 10.0 ATM'], enable_events=True, key='DDMACSV')],
            [sg.Button("Gráficar Animación CSV"),sg.Button("Exit")]]

layout5 = [[sg.Text('Seleccione que desea hacer los datos de PurpleAir')],
           [sg.Button('Promedio Online'),sg.Button("Animación Online"),sg.Button("Exit")]]

layout6 = [[sg.Text('Datos para el promedio (Todos se deben llenar con numeros enteros!)')],
            [sg.Text('Num. de Sensores', size =(22, 1)), sg.InputText(key='NumSenAPA')],
            [sg.Text('Num. Columnas de Sensores', size =(22, 1)), sg.InputText(key='ColsAPA')],
            [sg.Text('Num. Filas de Sensores', size =(22, 1)), sg.InputText(key='RowsAPA')],
            [sg.Text('Distancia entre Columnas', size =(22, 1)), sg.InputText(key='LCAPA')],
            [sg.Text('Distancia entre Filas', size =(22, 1)), sg.InputText(key='LRAPA')],
            [sg.Text('Cuantos minutos en el pasado (pares)', size =(22, 1)), sg.InputText(key='MinsPasados')],
            [sg.Text('Tiempo Duración Animación (Min.)', size =(28, 1)), sg.InputText(key='AniTimePA')],
            [sg.Text('Concentración de Material Particulado')],
            [sg.Text('Selecciona PM'),sg.Combo(['PM 1.0 CF', 'PM 2.5 CF', 'PM 10.0 CF', 'PM 2.5 ATM'], enable_events=True, key='DDMAPA')],
            [sg.Button("Graficar Animación PurpleAir"),sg.Button("Exit")]]

layout7 = [[sg.Text('Datos para el promedio (Todos se deben llenar con numeros enteros!)')],
            [sg.Text('Num. de Sensores', size =(22, 1)), sg.InputText(key='NumSenPPA')],
            [sg.Text('Num. Columnas de Sensores', size =(22, 1)), sg.InputText(key='ColsPPA')],
            [sg.Text('Num. Filas de Sensores', size =(22, 1)), sg.InputText(key='RowsPPA')],
            [sg.Text('Distancia entre Columnas', size =(22, 1)), sg.InputText(key='LCPPA')],
            [sg.Text('Distancia entre Filas', size =(22, 1)), sg.InputText(key='LRPPA')],
            [sg.Text('Tiempo Monitoreo (Tiempo par en Min.)', size =(28, 1)), sg.InputText(key='MinsPasadosP')],
            [sg.Text('Selecciona PM'),sg.Combo(['PM 1.0 CF', 'PM 2.5 CF', 'PM 10.0 CF', 'PM 2.5 ATM'], enable_events=True, key='DDMPPA')],
            [sg.Button("Gráfica Promedio PurpleAir"),sg.Button("Gráfica Lateral"),sg.Button("Exit")]]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), 
           sg.Column(layout3, visible=False, key='-COL3-'),sg.Column(layout4, visible=False, key='-COL4-'),
           sg.Column(layout5, visible=False, key='-COL5-'),sg.Column(layout6, visible=False, key='-COL6-'),
           sg.Column(layout7, visible=False, key='-COL7-')]]

window = sg.Window('Swapping the contents of a window', layout)

layout = 1  # The currently visible layout
while True:
    event, values = window.read()
    #print(event, values)
    if event in (None, 'Exit','Exit0','Exit1','Exit2','Exit3','Exit4','Exit5','Exit6','Exit7','Exit8','Exit9'):
        break
    if event == 'Promedio':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 3
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Promedio Online':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 7
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Animación':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 4
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Archivo CSV':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 2
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Online':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 5
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Animación Online':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 6
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Graficar Promedio CSV':
        '''fig = AF.GraphAvg(int(values['Cols']),int(values['Rows']),int(values['LC']), 
                         int(values['LR']),int(values['Hora']),
                         int(values['Mins']),int(values['NumSen']))
        draw_figure(window["-CANVAS-"].TKCanvas, fig)
        window[f'-COL{layout}-'].update(visible=False)
        layout = 4
        window[f'-COL{layout}-'].update(visible=True)'''
        #print(values['Folder'])
        PMType=PM_Dict[values['DDMPCSV']]
        #print(PMType)
        AF.GraphAvg(int(values['Rows']),int(values['Cols']),int(values['LC']), 
                    int(values['LR']),int(values['Hora']),
                    int(int(values['Mins'])/2)+1,int(values['NumSen']),values['Folder'],PMType)
    elif event == 'Gráfica Lateral':
        PMType=PM_Dict[values['DDMPCSV']]
        AF.LateralAvg(int(values['Rows']),int(values['Cols']),int(values['LC']), 
                    int(values['LR']),int(values['Hora']),
                    int(int(values['Mins'])/2)+1,int(values['NumSen']),values['Folder'],PMType)
    elif event == 'Gráficar Animación CSV':
        PMType=PM_Dict[values['DDMACSV']]
        AF.AnimationCSV(int(values['RowsACSV']),int(values['ColsACSV']),int(values['LCACSV']), 
                    int(values['LRACSV']),int(values['HoraACSV']),
                    int(int(values['MinsACSV'])/2)+1,int(values['NumSenACSV']),int(values['AniTime']),PMType,values['Carpeta'])
    elif event == 'Graficar Animación PurpleAir':
        PMType=PA_Dict[values['DDMAPA']]
        AF.AnimationPA(int(values['RowsAPA']),int(values['ColsAPA']),int(values['LCAPA']), 
                    int(values['LRAPA']),int(int(values['MinsPasados'])/2),int(values['NumSenAPA']),int(values['AniTimePA']),PMType)
    elif event == 'Gráfica Promedio PurpleAir':
        PMType=PA_Dict[values['DDMPPA']]
        #print(PMType)
        AF.GraphAvgPA(int(values['RowsPPA']),int(values['ColsPPA']),int(values['LCPPA']), 
                    int(values['LRPPA']),int(int(values['MinsPasadosP'])/2),int(values['NumSenPPA']),PMType)
    elif event in '123':
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(event)
        window[f'-COL{layout}-'].update(visible=True)
window.close()