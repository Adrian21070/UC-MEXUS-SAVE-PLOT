import PySimpleGUI as sg
import matplotlib.pyplot as plt

"""
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

ax1.scatter(2,4,1, marker=None)

plt.show()
"""
sg.theme('DarkAmber')
font = ('Times New Roman', 14)
font2 = ('Times New Roman', 12)
font3 = ('Times New Roman', 18)
"""
layout = [[sg.Text('Favor de seleccionar que graficas desea obtener', font=font3)],
        [sg.Checkbox('Animación (superficie)', default=False, key='Animation3D')],
        [sg.Checkbox('Lateral average', default=False, key='LateralAvg')],
        [sg.Checkbox('Registro historico de filas', default=False, key='Historico')],
        [sg.Text('Tiempo de duración animación (Min.)', size =(30, 1)), sg.InputText(key='Length')],
        [sg.Text('Promedios de los datos en horas (1=60min)', size =(30, 1)), sg.InputText(key='delta')],
        [sg.Button('Graficar'), sg.Button('Return',key='Date_hour'), sg.Button('Exit')]]
"""

layout = [[sg.Text('Superficie', font = font3, justification='center', expand_x=True)],
                    [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Modifica el formato de la superficie.',size=(29,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo')],
                    [sg.Text('Contenido del titulo: ',size=(29,1)), sg.InputText('Concentración PM 2.5', key='Title_content')],
                    [sg.Text('Contenido del subtitulo: ',size=(29,1)), sg.InputText('Promedio desde XX hasta YY', key='Subtitle_content')],
                    [sg.Text('Tipo de fuente: ', size=(33,1)), sg.Combo(['Times New Roman', 'Calibri'],default_value='Times New Roman',key='Font')],
                    [sg.Text('Tamaño de letra para el titulo: ',size=(29,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=14,key='Title_size')],
                    [sg.Text('Tamaño de letra para el subtitulo: ',size=(29,1)), sg.Combo([11, 12, 13, 14, 15, 16],default_value=12,key='Subtitle_size')],
                    [sg.Text('Tamaño de letra para los ejes: ',size=(29,1)), sg.Combo([8, 9, 10, 11, 12],default_value=11,key='Label_size')],
                    [sg.Text('Tipo de marcador a mostrar: ',size=(29,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                    [sg.Text('Ángulo polar (grados)', size=(29,1)), sg.Text('Ángulo azimutal (grados)', size=(30,1))],
                    [sg.Slider(orientation ='horizontal', key='Polar', range=(0,90), default_value=15, size=(22.6,20)),sg.Slider(orientation ='horizontal', key='Azimutal', range=(-180,180), default_value=-135,size=(22.6,20))],
                    [sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Nombre de la imagen resultante: ',size=(29,1)), sg.Input('Superficie.png', key='Name')],
                    [sg.Text('Selecciona donde guardar',size=(29,1)),sg.Input(size=(30,1),key='Surf_folder'),sg.FolderBrowse()],
                    [sg.Button('Continue'), sg.Button('Exit')]]

frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
                    [sg.Text('Formato de la gráfica lateral animada.',size=(30,1)), sg.Checkbox('Fondo transparente: ', default=False, key='Fondo'), sg.Checkbox('Recorrer el eje x: ', default=False, key='Recorrer')],
                    [sg.Text('Tipo de fuente: ', size=(30,1)), sg.Combo(['Times New Roman', 'Calibri', 'sans-serif', 'serif'],default_value='Times New Roman',key='Font')],
                    [sg.Text('Contenido del eje x: ',size=(30,1)), sg.InputText('profundidad (m)', key='xlabel_content',size=(27,1)), sg.Combo(['normal', 'italics', 'bold'], default_value='normal',key='Xstyle')],
                    [sg.Text('Contenido del eje y: ',size=(30,1)), sg.InputText('Valor promedio (ug/m3)', key='ylabel_content',size=(27,1)), sg.Combo(['normal', 'italics', 'bold'], default_value='normal',key='Ystyle')],
                    [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=16,key='Title_size')],
                    [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=14,key='Subtitle_size')],
                    [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=12,key='Label_size')],
                    [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
                    [sg.Text('Tamaño de marcador: ',size=(30,1)), sg.Combo([30, 35, 40, 45, 50, 55],default_value=40,key='MarkerSize')],
                    [sg.Text('Color del marcador: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Rojo',key='MarkerColor')], 
                    [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value='Dashed --',key='LineStyle')],
                    [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=2,key='LineSize')],
                    [sg.Text('Color de linea: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Azul',key='LineColor')], 
                    [sg.Text('Nombre del gif resultante: ',size=(30,1)), sg.Input('Lateral.gif', key='Name')],
                    [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(key='Lateral_folder',size=(30,1)),sg.FolderBrowse()]]
                    

"""
frame = [[sg.Text('',size=(1,1),font=('Times New Roman', 1))],
        [sg.Text('Modifica el formato de la gráfica lateral.',size=(30,1))],
        [sg.Text('Tamaño de letra para el titulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 17, 18],default_value=16,key='Title_size')],
        [sg.Text('Tamaño de letra para el subtitulo: ',size=(30,1)), sg.Combo([13, 14, 15, 16, 18],default_value=14,key='Subtitle_size')],
        [sg.Text('Tamaño de letra para los ejes: ',size=(30,1)), sg.Combo([10, 11, 12, 13, 14],default_value=12,key='Label_size')],
        [sg.Text('Tipo de marcador a mostrar: ',size=(30,1)), sg.Combo(['Circle','Diamond','Triangle_up','Triangle_down','Star','X','No marker'],default_value='Circle',key='Marker')],
        [sg.Text('Color del marcador: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Rojo',key='MarkerColor')], 
        [sg.Text('Tipo de linea a mostrar: ',size=(30,1)), sg.Combo(['Solid -','Dashed --','Dashdot -.','Dotted :','No line'],default_value='Dashed --',key='LineStyle')],
        [sg.Text('Tamaño de linea: ',size=(30,1)), sg.Combo([0.5, 1, 1.5, 2, 2.5, 3],default_value=2,key='LineSize')],
        [sg.Text('Color de linea: ',size=(30,1)), sg.Combo(['Azul','Rojo','Verde','Cyan','Magenta','Amarillo','Negro'],default_value='Azul',key='LineColor')], 
        [sg.Text('Nombre del gif resultante: ',size=(30,1)), sg.Input('Lateral.gif', key='Name')],
        [sg.Text('Selecciona donde guardar',size=(30,1)),sg.Input(key='Lateral_folder',size=(30,1)),sg.FolderBrowse()],
        [sg.Button('Continue'), sg.Button('Exit')]]
"""
layout = [[sg.Text('Superficie', font = font3, justification='center', expand_x=True)],
        [sg.Column(frame, expand_y=True, scrollable=True, vertical_scroll_only=True)],
        [sg.Button('Continue', key='Average'), sg.Button('Return', key='Date_hour'), sg.Button('Exit')]]


window = sg.Window('Proyecto UC-MEXUS', layout, font = font, size=(720,480))
event, LateralAvg = window.read()

a = 1