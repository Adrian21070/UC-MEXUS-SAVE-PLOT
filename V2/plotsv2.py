# Librerias
import os, sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import PySimpleGUI as sg
import pandas as pd
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm, style
from matplotlib.lines import Line2D
from datetime import datetime, timedelta
from dateutil import tz
from scipy import interpolate
from scipy.interpolate import griddata
from purple_air import *

# Diccionario para seleccionar el tipo de material
# particulado a graficar a partir de los archivos CSV
PM_Dict={"PM 1.0 CF": "pm1_0_cf_1",	
         "PM 2.5 CF": "pm2_5_cf_1",	
         "PM 10.0 CF": "pm10_0_cf_1",	
         "PM 1.0 ATM": "pm1_0_atm",	
         "PM 2.5 ATM": "pm2_5_atm",	
         "PM 10.0 ATM" : "pm10_0_atm"}

# Simple formato para transformar de csv a online.
CSV_dict = {"UTCDateTime":"created_at",
            "pm1_0_atm":"PM1.0_ATM_ug/m3",
            "pm2_5_atm":"PM2.5_ATM_ug/m3", 
            "pm10_0_atm":"PM10.0_ATM_ug/m3",
            "uptime":"UptimeMinutes", 
            "rssi":"RSSI_dbm",
            "current_temp_f":"Temperature_F", 
            "current_humidity":"Humidity_%",
            "pm1_0_cf_1":"PM1.0_CF1_ug/m3", 
            "pm2_5_cf_1":"PM2.5_CF1_ug/m3",
            "pm10_0_cf_1":"PM10.0_CF1_ug/m3", 
            "p_0_3_um":">=0.3um/dl", "p_0_5_um":">=0.5um/dl", 
            "p_1_0_um":">=1.0um/dl", "p_2_5_um":">=2.5um/dl", 
            "p_5_0_um":">=5.0um/dl", "p_10_0_um":">=10.0um/dl",
            "pm1_0_atm_b":"PM1.0_ATM_B_ug/m3",
            "pm2_5_atm_b":"PM2.5_ATM_B_ug/m3", 
            "pm10_0_atm_b":"PM10.0_ATM_B_ug/m3",
            "mem":"UptimeMinutes_B", "adc":"ADC", 
            "pressure":"Pressure_hpa",
            "pm1_0_cf_1_b":"PM1.0_CF1_B_ug/m3", 
            "pm2_5_cf_1_b":"PM2.5_CF1_B_ug/m3",
            "pm10_0_cf_1_b":"PM10.0_CF1_B_ug/m3", 
            "p_0_3_um_b":">=0.3_B_um/dl", "p_0_5_um_b":">=0.5_B_um/dl", 
            "p_1_0_um_b":">=1.0_B_um/dl", "p_2_5_um_b":">=2.5_B_um/dl", 
            "p_5_0_um_b":">=5.0_B_um/dl", "p_10_0_um_b":">=10.0_B_um/dl"}

# Diccionario para seleccionar el tipo de material 
# particulado a graficar a partir de los datos en el canal
# principal de thingspeak. 
PA_Dict={"PM 1.0 CF": "field1",	
         "PM 2.5 CF": "field2",	
         "PM 10.0 CF": "field3",
         "PM 2.5 ATM": "field8"}

# Todos los datos que puede pedir el usuario de online.
Column_labels = ['PM1.0_ATM_ug/m3', 'PM2.5_ATM_ug/m3', 'PM10.0_ATM_ug/m3',
                'PM1.0_CF1_ug/m3', 'PM2.5_CF1_ug/m3', 'PM10.0_CF1_ug/m3',
                'PM1.0_ATM_B_ug/m3', 'PM2.5_ATM_B_ug/m3', 'PM10.0_ATM_B_ug/m3',
                'PM1.0_CF1_B_ug/m3', 'PM2.5_CF1_B_ug/m3', 'PM10.0_CF1_B_ug/m3']

PA_Onl = {"PM 1.0 ATM": "PM1.0_ATM_ug/m3", "PM 2.5 ATM": "PM2.5_ATM_ug/m3",
        "PM 10.0 ATM": "PM10.0_ATM_ug/m3", "PM 1.0 CF": "PM1.0_CF1_ug/m3",
        "PM 2.5 CF": "PM2.5_CF1_ug/m3", "PM 10.0 CF": "PM10.0_CF1_ug/m3",
        "PM 1.0 ATM B": "PM1.0_ATM_B_ug/m3", "PM 2.5 ATM B": "PM2.5_ATM_B_ug/m3",
        "PM 10.0 ATM B": "PM10.0_ATM_B_ug/m3", "PM 1.0 CF B": "PM1.0_CF1_B_ug/m3",
        "PM 2.5 CF B": "PM2.5_CF1_B_ug/m3", "PM 10.0 CF B": "PM10.0_CF1_B_ug/m3"}

Utc = tz.tzutc()
Local_H = tz.tzlocal()

def open_csv(window, value):
    # Leo los archivos dentro de la carpeta.
    data = {}
    it = 1
    minimum = {}
    maximum = {}

    try:
        with os.scandir(value['Browse']) as ficheros:
            # Ficheros right now has directories with csv inside
            for fichero in ficheros:
                dir = value['Browse'] + '/' + fichero.name
                if it == 1:
                    with os.scandir(dir) as files:
                        
                        try:
                            for file in files:
                                #file should have the name as SXXX_YYYY_MM_DD
                                name = file.name
                                # Abro el archivo
                                df = pd.read_csv(dir + '/' + name)
                                # Paso a datetime las fechas.
                                df['created_at'] = conversor_datetime_string(df['created_at'], key=0)

                                data[f'Sensor {name[1:4]}'] = df
                        except:
                            layout = [[sg.Text('Error al leer un archivo', font=('Times New Roman',18))],
                                    [sg.Text(f'Se tuvo problemas al leer el archivo {name}')],
                                    [sg.Button('Return'), sg.Button('Exit')]]
                            window.close()
                            window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
                            event, value = window.read()

                            if event in ('Exit', sg.WIN_CLOSED):
                                window.close()
                                sys.exit()
        
                            return True, 0, 0, window

                    it += 1
                else:
                    with os.scandir(dir) as files:

                        try:
                            for file in files:
                                # file should have the name as SXXX_YYYY_MM_DD
                                name = file.name
                                # Abro el archivo
                                df = pd.read_csv(dir + '/' + name)
                                # Paso a datetime las fechas
                                df['created_at'] = conversor_datetime_string(df['created_at'], key=0)

                                data[f'Sensor {name[1:4]}'] = pd.concat([data[f'Sensor {name[1:4]}'], df])

                                # Sort the data
                                data[f'Sensor {name[1:4]}'] = data[f'Sensor {name[1:4]}'].sort_values(by=['created_at'])

                                # Reset the index
                                data[f'Sensor {name[1:4]}'].reset_index(inplace=True, drop=True)
                        except:
                            layout = [[sg.Text('Error al leer un archivo', font=('Times New Roman',18))],
                                    [sg.Text(f'Se tuvo problemas al leer el archivo {name}')],
                                    [sg.Button('Return'), sg.Button('Exit')]]
                            window.close()
                            window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
                            event, value = window.read()

                            if event in ('Exit', sg.WIN_CLOSED):
                                window.close()
                                sys.exit()
        
                            return True, 0, 0, window
    except:
        layout = [[sg.Text('Carpeta no encontrada', font=('Times New Roman',18))],
                [sg.Text(f'Favor de introducir una carpeta valida.')],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()

        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        
        return True, 0, 0, window

    # Obtengo los minimos y maximos de cada sensor.
    for ii in data.keys():
        df = data[ii]
        date = df['created_at']

        # En formato datetime utc.
        maximum[ii] = date.iloc[-1]
        minimum[ii] = date.iloc[0]

    return data, minimum, maximum, window

def conversor_datetime_string(date, key):
    """
        Si key = 0, tomara a date como string en formato utc,
        regresara una lista con las fechas en formato datetime utc.

        Si key = 1, tomara a date como string en formato local,
        regresara una lista con las fechas en formato datetime local.

        Si key = 2, tomara a date como datetime, y cambiara de utc a local,
        o de local a utc.

        Si key = 3, tomara a date como datetime, y regresara
        una lista de strings.
    """
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    new_date = []
    if key == 0:
        for ii in range(len(date)):
            temp = date[ii].strip(' UTC')
            # Transformo de string a datetime utc
            time_utc = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
            new_date.append(time_utc)

    elif key == 1:
        for ii in range(len(date)):
            temp = date[ii]
            # Transformo de string a datetime local
            time_local = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=to_zone)
            new_date.append(time_local)

    elif key == 2:
        if str(date[0].tzinfo) == 'tzutc()':
            for ii in range(len(date)):
                temp = date[ii]
                time = temp.astimezone(to_zone)
                new_date.append(time)

        elif str(date[0].tzinfo) == 'tzlocal()':
            for ii in range(len(date)):
                temp = date[ii]
                time = temp.astimezone(from_zone)
                new_date.append(time)
    
    elif key == 3:
        if str(date.iloc[-1].tzinfo) == 'tzutc()':
            for ii in date:
                # Transformo de datetime a string
                time_local = ii.strftime('%Y-%m-%d %H:%M:%S UTC')
                new_date.append(time_local)
                
        elif str(date.iloc[-1].tzinfo) == 'tzlocal()':
            for ii in date:
                # Transformo de datetime a string
                time_local = ii.strftime('%Y-%m-%d %H:%M:%S')
                new_date.append(time_local)

    return new_date

def animate(i,measurements,x_axis,y_axis,ax1,columns,rows,lateral_length,depth_length,PMType,indx,limites,fig,prom, styles, carretera):
    """
    Función que realiza la superficie.
    """

    z_axis = []

    # Se obtiene la lista de las fechas de cada medición
    for k in range(len(measurements)):
        jj = indx[k] #Numero del sensor actual.
        #Accede al dato del sensor jj, en el tiempo i.
        df = measurements[f'Sensor {jj}']
        dato = df[PMType[0]][i]
        z_axis.append(float(dato))
    
    minimum = round(min(z_axis),2)
    maximum = round(max(z_axis),2)
    textstr = "Min: "+str(minimum)+" ug/m3   Max: "+str(maximum)+" ug/m3"

    ax1.clear()
    ax1.annotate(textstr,
            xy=(0.5, 0), xytext=(0, 10),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=styles['Label_size'], ha='center', va='bottom')

    # Scatter
    if styles['Marker'] != 'No marker':
        scamap = plt.cm.ScalarMappable(cmap='inferno')
        fcolors = scamap.to_rgba(maximum)
        size_scatter = [100 for n in range(len(x_axis))]
        ax1.scatter3D(x_axis, y_axis, z_axis, marker=styles['Marker'], s=size_scatter, c=z_axis, facecolors=fcolors, cmap='inferno')

    x_final = max(max(x_axis))
    y_final = max(max(y_axis))
    x_min = min(min(x_axis))
    y_min = min(min(y_axis))

    # Interpolación
    if styles['Interp'] == 'Cúbica':
        gridx,gridy,gridz0 = Interpol(x_axis,y_axis,z_axis,x_final,y_final,x_min,y_min)
    else:
        points = np.concatenate((x_axis.T, y_axis.T), axis=1)
        gridx, gridy = np.mgrid[x_min:x_final, y_min:y_final]
        gridz0 = griddata(points, z_axis, (gridx, gridy), method='linear')

    ax1.plot_surface(gridx, gridy, gridz0,cmap=cm.inferno, linewidth=0, antialiased=False)

    # Plot style
    ax1.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax1.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax1.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    #axis labels
    ax1.set_ylabel(styles['ylabel_content'],
                fontsize=styles['Label_size'],
                fontfamily=styles['Font'])

    ax1.set_xlabel(styles['xlabel_content'],
                fontsize=styles['Label_size'],
                fontfamily=styles['Font'])

    ax1.set_zlabel(styles['zlabel_content'],
                fontsize=styles['Label_size'],
                rotation = 180,
                fontfamily=styles['Font'])

    # Limites de los ejes y ticks
    ax1.set_xlim3d(x_min, x_final)
    ax1.set_xticks(np.arange(x_min, x_final+lateral_length, lateral_length))

    if carretera == 'Derecha':
        pass
    else:
        ax1.invert_xaxis()

    ax1.set_ylim3d(y_min, y_final)
    ax1.set_yticks(np.arange(y_min, y_final+depth_length, depth_length))

    ax1.set_zlim3d(0, limites[1])

    ax1.tick_params(axis='both',
                labelsize=styles['Label_size']-2)

    if prom == 0:
        #subtitle
        ax1.set_title(styles['Subtitle_content'],
             x=0.5,
             y=0.87,
             transform=fig.transFigure,
             fontsize=styles['Subtitle_size'],
             fontfamily=styles['Font'])
        
        if styles['Bold']:
            #superior title
            plt.suptitle(styles['Title_content'],
                 x=0.5,
                 y=0.92,
                 transform=fig.transFigure,
                 fontsize=styles['Title_size'],
                 fontweight="bold",
                 fontfamily=styles['Font'])
        else:
            #superior title
            plt.suptitle(styles['Title_content'],
                 x=0.5,
                 y=0.92,
                 transform=fig.transFigure,
                 fontsize=styles['Title_size'],
                 fontweight="regular",
                 fontfamily=styles['Font'])
        
    else:
        #subtitle
        ax1.set_title(f'Promedio cada {round(prom*60)} minutos\n'+df['created_at'][i],
             x=0.5,
             y=0.87,
             transform=fig.transFigure,
             fontsize=styles['Subtitle_size'],
             fontfamily=styles['Font'])

        if styles['Bold']:
            #superior title
            plt.suptitle('Concentración ' + 'PM2.5_ATM_ug/m3'.replace('_','').replace('ATM','').strip('ug/m3'),
                 x=0.5,
                 y=0.92,
                 transform=fig.transFigure,
                 fontsize=styles['Title_size'],
                 fontweight="bold",
                 fontfamily=styles['Font'])
        else:
            #superior title
            plt.suptitle('Concentración ' + 'PM2.5_ATM_ug/m3'.replace('_','').replace('ATM','').strip('ug/m3'),
                 x=0.5,
                 y=0.92,
                 transform=fig.transFigure,
                 fontsize=styles['Title_size'],
                 fontweight="regular",
                 fontfamily=styles['Font'])

    ax1.view_init(styles['Polar'], styles['Azimutal'])

def Interpol(x,y,z,xfinal,yfinal,xmin,ymin):
    """
    Función que realiza la interpolación cúbica para la superficie.
    """
    points = np.concatenate((x.T, y.T), axis=1)
    grid_x, grid_y = np.mgrid[xmin:xfinal:300j, ymin:yfinal:300j]
    grid_z0 = griddata(points, z, (grid_x, grid_y), method='cubic')
    return grid_x, grid_y, grid_z0

def animate_1D(i, measurements, y_axis, PMType, depth, ax1, columns, rows, indx, limites, alpha, prom, fig, styles, rows_sen):
    """
    Función que realiza la grafica del promedio lateral.
    """
    # Solo importa y_axis, profundidad
    z_axis = []
    y_axis = np.arange(min(min(y_axis)), max(max(y_axis))+depth, depth)

    # Creando lista con los datos ii
    for jj in indx.values():
        df = measurements[f'Sensor {jj}']
        s = df[PMType[0]][i]
        z_axis.append(float(s))

    # Promedio por filas.
    filas = []
    sum = []
    for ii in rows_sen.keys():
        for jj in rows_sen[ii]:
            df = measurements[f'Sensor {jj}']
            s = df[PMType[0]][i]
            sum.append(float(s))
        filas.append(np.mean(sum))
        sum = []
    # Aquí ya se obtuvo el promedio por filas en el tiempo ii, se obtendra una cantidad n de promedio de filas a lo largo
    # de todo el for principal.
    
    # Realiza el plot
    ax1.clear()
    if styles['Marker'] != 'No marker':
        ax1.scatter(y_axis, filas, s=styles['MarkerSize'], marker=styles['Marker'], c=styles['MarkerColor'])

    # Interpolación
    if styles['Interp'] == 'Cuadrática':
        f = interpolate.interp1d(y_axis, filas, kind='quadratic')
        x = np.arange(min(y_axis), max(y_axis), 0.05)
        ax1.plot(x, f(x), styles['LineStyle'], linewidth=styles['LineSize'], c=styles['LineColor'])
    else:
        ax1.plot(y_axis, filas, styles['LineStyle'], linewidth=styles['LineSize'], c=styles['LineColor'])

    #axis labels
    ax1.set_xlabel(styles['xlabel_content'],
                  fontsize=styles['Label_size'],
                  fontfamily=styles['Font'],
                  fontstyle=styles['Xstyle'])

    ax1.set_ylabel(styles['ylabel_content'],
                  fontsize=styles['Label_size'],
                  fontfamily=styles['Font'],
                  fontstyle=styles['Ystyle'])

    ax1.set_xticks(y_axis, axis = 0)

    ax1.tick_params(axis='both',
                   labelsize=styles['Label_size']-2)

    if prom == 0:
        #subtitle
        ax1.set_title(styles['Subtitle_content'],
                     x=0.5,
                     y=0.83,
                     transform=fig.transFigure,
                     fontsize=styles['Subtitle_size'],
                     fontfamily=styles['Font'],
                     fontstyle=styles['Substyle'])
        
        if styles['Bold']:
            #superior title
            plt.suptitle(styles['Title_content'],
                         x=0.5,
                         y=0.95,
                         transform=fig.transFigure,
                         fontsize=styles['Title_size'],
                         fontweight="bold",
                         fontfamily=styles['Font'],
                         fontstyle=styles['Titlestyle'])
        else:    
            #superior title
            plt.suptitle(styles['Title_content'],
                         x=0.5,
                         y=0.95,
                         transform=fig.transFigure,
                         fontsize=styles['Title_size'],
                         fontweight="regular",
                         fontfamily=styles['Font'],
                         fontstyle=styles['Titlestyle'])

    else:
        #subtitle
        ax1.set_title(f'Promedio cada {round(prom*60)} minutos\n'+df['created_at'][i],
                     x=0.5,
                     y=0.83,
                     transform=fig.transFigure,
                     fontsize=styles['Subtitle_size'],
                     fontfamily=styles['Font'],
                     fontstyle=styles['Substyle'])
        
        if styles['Bold']:
            #superior title
            plt.suptitle('Concentración ' + PMType[0].replace('_','').replace('ATM','').strip('ug/m3'),
                         x=0.5,
                         y=0.95,
                         transform=fig.transFigure,
                         fontsize=styles['Title_size'],
                         fontweight="bold",
                         fontfamily=styles['Font'],
                         fontstyle=styles['Titlestyle'])
        else:
            #superior title
            plt.suptitle('Concentración ' + PMType[0].replace('_','').replace('ATM','').strip('ug/m3'),
                         x=0.5,
                         y=0.95,
                         transform=fig.transFigure,
                         fontsize=styles['Title_size'],
                         fontweight="regular",
                         fontfamily=styles['Font'],
                         fontstyle=styles['Titlestyle'])

    interp = styles['Interp']
    if (styles['Marker'] != 'No marker') and (styles['LineStyle'] != 'No line'):
        # Incluye el promedio y interpolación en la leyenda.
        ax1.legend(['Promedio', f'Interpolación {interp}'], loc=styles['Legend'], framealpha=alpha, fontsize=styles['Label_size']-2, prop={'family': styles['Font']})
    
    elif (styles['Marker'] != 'No marker') and (styles['LineStyle'] == 'No line'):
        # Incluye promedio, no interpolación
        ax1.legend(['Promedio'], loc=styles['Legend'], framealpha=alpha, fontsize=styles['Label_size']-2, prop={'family': styles['Font']})
    
    elif (styles['Marker'] == 'No marker') and (styles['LineStyle'] != 'No line'):
        # Incluye interpolación, no promedio
        ax1.legend([f'Interpolación {interp}'], loc=styles['Legend'], framealpha=alpha, fontsize=styles['Label_size']-2, prop={'family': styles['Font']})
    
    #Si no entra en ninguna, no habra leyenda.

    if styles['Recorrer']:
        ax1.axis([min(y_axis)-0.1, max(y_axis)+0.5, 0, limites[1]])
    else:
        ax1.axis([0, max(y_axis)+0.5, 0, limites[1]])

    plt.subplots_adjust(top=0.8)

def historic_means(measurements, y_axis, PMType, depth, columns, rows, ax1, fig, indx, limites, alpha, prom, styles, rows_sen):
    """
    Función que realiza la grafica de promedio historicos.
    """
    # Solo importa y_axis, profundidad
    y_axis = np.arange(min(min(y_axis)), max(max(y_axis))+depth, depth)
    
    datos = {f'Fila {ii+1}':[] for ii in range(rows)}
    x_label = []
    pos = []

    # Bucle que toma todos los promedios.
    for ii in range(len(measurements[f'Sensor {indx[0]}'])):
        # Creando lista con los datos ii
        df = measurements[f'Sensor {indx[-1]}']

        date = df['created_at'][ii].replace(' (hora de inicio)', '')
        time = datetime.strptime(date, '%Y/%m/%d, %H:%M')
        if ii == 0:
            x_label.append(date)
            pos.append(ii)
        else:
            if time.day != time2.day:
                x_label.append(date)
                pos.append(ii)
        time2 = time

        filas = []
        sum = []
        ww = 0
        for kk in rows_sen.keys():
            for jj in rows_sen[kk]:
                df = measurements[f'Sensor {jj}']
                s = df[PMType[0]][ii]
                sum.append(float(s))
            filas.append(np.mean(sum))
            datos[f'Fila {ww+1}'].append(filas[ww])
            ww += 1
            sum = []

    # Realiza el plot
    ley = []
    maxy = []
    for ii in datos.keys():
        # Aquí se colocan todos los plots.
        y_axis = np.linspace(0, len(datos[ii]), len(datos[ii]))
        
        if styles['Marker'] != 'No marker':
            ax1.scatter(y_axis, datos[ii], s=styles['MarkerSize'], marker=styles['Marker'])

        # Interpolación
        if styles['Interp'] == 'Cuadrática':
            f = interpolate.interp1d(y_axis, datos[ii], kind='quadratic')
            x = np.arange(min(y_axis), max(y_axis), 0.05)
            ax1.plot(x, f(x), styles['LineStyle'], linewidth=styles['LineSize'])
        else:
            ax1.plot(y_axis, datos[ii], styles['LineStyle'], linewidth=styles['LineSize'])

        color = ax1.get_lines()[-1].get_color()
        ley.append((color, ii))
        maxy.append(max(datos[ii]))

    #axis labels
    ax1.set_xlabel(styles['xlabel_content'],
                  fontsize=styles['Label_size'],
                  fontfamily=styles['Font'],
                  fontstyle=styles['Xstyle'])

    ax1.set_ylabel(styles['ylabel_content'],
                  fontsize=styles['Label_size'],
                  fontfamily=styles['Font'],
                  fontstyle=styles['Ystyle'])
    
    y_axis2 = []
    for ii in pos:
        y_axis2.append(y_axis[ii])

    ax1.set_xticks(y_axis2, labels=x_label)

    ax1.tick_params(axis='both',
                   labelsize=styles['Label_size']-2)
    
    #subtitle
    ax1.set_title(styles['Subtitle_content'],
                x=0.5,
                y=0.83,
                transform=fig.transFigure,
                fontsize=styles['Subtitle_size'],
                fontfamily=styles['Font'],
                fontstyle=styles['Substyle'])
        
    if styles['Bold']:
        #superior title
        plt.suptitle(styles['Title_content'],
                    x=0.5,
                    y=0.95,
                    transform=fig.transFigure,
                    fontsize=styles['Title_size'],
                    fontweight="bold",
                    fontfamily=styles['Font'],
                    fontstyle=styles['Titlestyle'])
    else:    
        #superior title
        plt.suptitle(styles['Title_content'],
                    x=0.5,
                    y=0.95,
                    transform=fig.transFigure,
                    fontsize=styles['Title_size'],
                    fontweight="regular",
                    fontfamily=styles['Font'],
                    fontstyle=styles['Titlestyle'])
    
    # Leyenda
    ax1.legend([Line2D([0], [0], color=clave[0], lw=2) for clave in ley],
           [clave[1] for clave in ley], loc=styles['Legend'], framealpha=alpha, fontsize=styles['Label_size']-2, prop={'family': styles['Font']})
    
    ax1.set_ylim(0, max(maxy)+0.5)

    plt.subplots_adjust(top=0.8)

def surface(x,y,z,columns, rows, row_dist, col_dist, graph_selection, value_anim, PMType, indx, limites, Surface, carretera_lateral):
    """
    Función que controla la animación y grafico estatico de la superficie
    """

    # Value_anim viene información sobre periodo, y duración de la animación
    # graph_selection tiene información sobre el tipo de grafica deseada.
    # Styles viene toda la información de tipo de letra, markers, nombre del archivo, ruta, etc.

    indx = list(indx.values())

    if graph_selection['An_superficie']:
        # Esto genera un gif
        prom = float(value_anim['delta']) #Delta
        length = float(value_anim['Length']) #Minutes

        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')

        frames = len(z[f'Sensor {indx[0]}']['created_at'])
        frame_rate = length*60000/frames

        ani = animation.FuncAnimation(fig,animate,interval=frame_rate,
                fargs=(z,x,y,ax1,columns,rows,col_dist,row_dist,PMType,indx,limites,fig,prom,Surface,carretera_lateral),
                frames=frames, repeat=True)
        
        # Ubicación principal
        if '.gif' in Surface['Name']:
            path = os.path.join(Surface['Surf_folder'], Surface['Name'])
            path2 = os.path.join(Surface['Surf_folder'], Surface['Name'][0:len(Surface['Name'])-4]+'_frames')
        else:
            path = os.path.join(Surface['Surf_folder'], Surface['Name']+'.gif')
            path2 = os.path.join(Surface['Surf_folder'], Surface['Name']+'_frames')

        ani.save(path, writer='imagemagick', fps=frames/(length*60))
        #plt.show()

        if True:
            os.makedirs(path2, exist_ok=True)

            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111, projection='3d')
            for ii in range(frames):
                path = os.path.join(path2,f'Frame{ii}.png')
                animate(ii,z,x,y,ax2,columns,rows,col_dist,row_dist, PMType, indx, limites, fig2, prom, Surface, carretera_lateral)
                if Surface['Fondo']:
                    plt.savefig(path, transparent=True)
                else:
                    plt.savefig(path, transparent=False)
    
    else:
        # Grafico estatico
        window = sg.Window(title='Promedios históricos',
                    layout=[[sg.Canvas(key='canvas', size=(720,480))]],
                    finalize=True, size=(720,480))
        # Obtención del canvas
        canvas = window['canvas'].TKCanvas
        # Genera una estatica
        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='right', expand=1)

        animate(0, z, x, y, ax1, columns, rows, col_dist, row_dist, PMType, indx, limites, fig, 0, Surface, carretera_lateral)
        figure_canvas_agg.draw()
        if '.png' in Surface['Name']:
            path = os.path.join(Surface['Surf_folder'], Surface['Name'])
        else:
            path = os.path.join(Surface['Surf_folder'], Surface['Name']+'.png')

        if Surface['Fondo']:
            fig.savefig(path, transparent=True)
        else:
            fig.savefig(path, transparent=False)

def lateral_avg(x,y,z,columns, rows, row_dist, col_dist, graph_selection, value_anim, PMType, indx, limites, lateral, rows_sen):
    """
    Función que controla la animación y grafico estatico del promedio lateral.
    """

    indx_2 = list(indx.values())
    
    if graph_selection['An_lateral']:
        prom = float(value_anim['delta']) #Delta
        length = float(value_anim['Length']) #Minutes

        fig3, ax3 = plt.subplots(1,1,dpi=100)
        frames = len(z[f'Sensor {indx_2[0]}']['created_at'])
        frame_rate = length*60000/frames
        #animate_1D(6, z, y, PMType, row_dist, ax3, columns, rows, indx, limites,1.0, prom, fig3, lateral)
        
        anim = animation.FuncAnimation(fig3, animate_1D, interval=frame_rate,
                fargs=(z,y,PMType,row_dist,ax3,columns,rows,indx,limites,1.0, prom, fig3, lateral, rows_sen),
                frames=frames, repeat=True)

        # Ubicación principal
        if '.gif' in lateral['Name']:
            path = os.path.join(lateral['Lateral_folder'], lateral['Name'])
            path2 = os.path.join(lateral['Lateral_folder'], lateral['Name'][0:len(lateral['Name'])-4]+'_frames')
        else:
            path = os.path.join(lateral['Lateral_folder'], lateral['Name']+'.gif')
            path2 = os.path.join(lateral['Lateral_folder'], lateral['Name']+'_frames')
        
        anim.save(path, writer='imagemagick', fps=frames/(length*60))

        if True:
            # Pasa los frames a pngs
            os.makedirs(path2, exist_ok=True)

            fig4, ax4 = plt.subplots(1,1,dpi=100)
            for ii in range(frames):
                path = os.path.join(path2,f'Frame{ii}.png')
                animate_1D(ii, z, y, PMType, row_dist, ax4, columns, rows, indx, limites,0.0, prom, fig4, lateral, rows_sen)
                if lateral['Fondo']:
                    plt.savefig(path, transparent=True)
                else:
                    plt.savefig(path, transparent=False)

    else:
        window = sg.Window(title='Promedio lateral',
                       layout=[[sg.Canvas(key='canvas', size=(720,480))]],
                        finalize=True, size=(720,480))
        # Obtención del canvas
        canvas = window['canvas'].TKCanvas
        fig3, ax3 = plt.subplots(1, 1, dpi=100, figsize=(7,5))
        figure_canvas_agg = FigureCanvasTkAgg(fig3, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='right', expand=1)

        if '.png' in lateral['Name']:
            path = os.path.join(lateral['Lateral_folder'], lateral['Name'])
        else:
            path = os.path.join(lateral['Lateral_folder'], lateral['Name']+'.png')
        
        if lateral['Fondo']:
            animate_1D(0, z, y, PMType, row_dist, ax3, columns, rows, indx, limites, 0.0, 0, fig3, lateral, rows_sen)
            figure_canvas_agg.draw()
            fig3.savefig(path, transparent=True)
        else:
            animate_1D(0, z, y, PMType, row_dist, ax3, columns, rows, indx, limites, 1.0, 0, fig3, lateral, rows_sen)
            figure_canvas_agg.draw()
            fig3.savefig(path, transparent=False)

def historico(y, z, columns, rows, row_dist, graph_selection, PMType, indx, limites, historico, rows_sen):
    """
    Función que controla el grafico estatico del historico
    """
    # Grafico estatico
    window = sg.Window(title='Promedios históricos',
                       layout=[[sg.Canvas(key='canvas', size=(720,480))]],
                        finalize=True, size=(720,480))
    # Obtención del canvas
    canvas = window['canvas'].TKCanvas
    fig3, ax3 = plt.subplots(1, 1, dpi=100, figsize=(7,5))
    figure_canvas_agg = FigureCanvasTkAgg(fig3, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='right', expand=1)
    indx = list(indx.values())
    if '.png' in historico['Name']:
        path = os.path.join(historico['Historico_folder'], historico['Name'])
    else:
        path = os.path.join(historico['Historico_folder'], historico['Name']+'.png')
        
    if historico['Fondo']:
        #Sin fondo
        historic_means(z, y, PMType, row_dist, columns, rows, ax3, fig3, indx, limites, 0, 0, historico, rows_sen)
        figure_canvas_agg.draw()
        fig3.savefig(path, transparent=True)
    else:
        # Con fondo
        historic_means(z, y, PMType, row_dist, columns, rows, ax3, fig3, indx, limites, 1.0, 0, historico, rows_sen)
        figure_canvas_agg.draw()
        fig3.savefig(path, transparent=False)