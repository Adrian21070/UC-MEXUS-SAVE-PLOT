import PySimpleGUI as sg
from matplotlib import axes
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def Canvas():
    window = sg.Window(title='Proyecto UC-MEXUS',
                       layout=[[sg.Canvas(key='canvas', size=(720,480))]],
                        finalize=True, size=(720,480))
    # Obtención del canvas
    canvas = window['canvas'].TKCanvas
    #figure = Figure(figsize=(5,3))
    figure, axes = plt.subplots(1,1,dpi=100,figsize=(7,5))
    
    #axes = figure.add_subplot()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='right', expand=1)
    def plot_frequency(frec=10):
        window['title'].update(f'Frecuencia { frec }')
        x = np.linspace(0, 2 * np.pi, 1000)
        y = np.sin(frec * x)

        axes.cla()
        axes.plot(x, y)
        figure_canvas_agg.draw()

    def normal(freq):
    
        axes.cla()
        x = np.linspace(0, 4*np.pi, 1000)
        y = (np.sin(freq*x)+np.cos(freq*x))**2
        axes.plot(x,y)
        axes.set_xlabel('Profundidad (m)',
                      fontsize=11,
                      fontfamily='Times New Roman')

        axes.set_ylabel('Valor promedio (ug/m3)',
                      fontsize=11,
                      fontfamily='Times New Roman')

        axes.tick_params(axis='both',
                       labelsize=11-2)

        axes.set_title('Esto es una prueba de subtitulo',
                         x=0.5,
                         y=0.83,
                         transform=figure.transFigure,
                         fontsize=14,
                         fontfamily="Times New Roman",
                         fontstyle='italic')

        #superior title
        plt.suptitle('Prueba de titulo...',
                 x=0.5,
                 y=0.95,
                 transform=figure.transFigure,
                 fontsize=16,
                 fontweight="normal",
                 fontfamily="Calibri",
                 fontstyle='oblique')

        #ax1.axis([0, 10+0.5, 0, 15])
        plt.subplots_adjust(top=0.8)


    # Set default frequency
    default_frequency = 2
    #window['slider'].update(default_frequency)
    normal(default_frequency)
    #plot_f(default_frequency)
    while True:
        event, values = window.read() 
        if event == 'slider':
            normal(freq=2)
        if event == sg.WIN_CLOSED:
            break
    window.close()



Canvas()