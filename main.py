# Librerias
import sys
import gui2 as gui
from purple_air import *

if __name__ == "__main__":
    # Creamos la interfaz grafica
    window, event = gui.gui_creation()
    
    # Comprobamos si se obtendran datos de online o csv.
    if event == 'Online':
        event = 'TypeData'
        while True:
            if event == 'TypeData':
                # Pregunta que tipo de dato quiere analizar
                window, event, value = gui.data_type(window)
                PMType = value

            if event == 'Return':
                pass
                # Como le hago para regresar hasta gui_creation???

            if event == 'Sensor_info':
                # Pedimos al usuario información sobre el número de sensores,
                # distancia entre ellos, etc.
                window, event, value = gui.sensors_info(window)
                if event != 'Sensor Distribution':
                    continue
                # Almacenamos los datos importantes de esto
                rows = int(value['Rows'])
                columns = int(value['Columns'])
                col_dist = int(value['Col_dis'])
                row_dist = int(value['Row_dis'])
                num_sen = int(value['NumSen'])

            if event == 'SensorDistribution':
                # Solicitamos al usuario los rangos de fecha de las mediciones
                window, event, indx = gui.distribution(window,num_sen,rows,columns)
            
            if event == 'Date_hour':
                window, event, value = gui.date_hour(window)
                if event != 'Extraction':
                    continue
                start = value['Start'] + '%20' + value['Start_hour'] + ':00'
                end = value['End'] + '%20' + value['End_hour'] + ':00'

            if event == 'Extraction':
                window,x_axis,y_axis,z_axis,minimum_dates,maximum_dates,holes,num_csv_per_sensor,it = gui.extraction(PMType,rows,
                                                                                                    columns,col_dist,row_dist,
                                                                                                    indx,start,end)
                if it > 0:
                    window, event = gui.holes_warning(window,holes,num_csv_per_sensor)
                else:
                    event = 'Graphs'
            
            if event == 'Fix_errors':
                pass

            if event == 'Graphs':
                pass

    elif event == 'CSV':
        pass

    else:
        gui.shutdown(window)