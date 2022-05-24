# Librerias
import sys
import csv_plot as Csv
import gui2 as gui
import functions as Func
import save_data as save
import pandas as pd
#from purple_air import *

if __name__ == "__main__":
    # Creamos la interfaz grafica
    window, event = gui.save_or_graph()

    if event == 'Save_data':
        event = 'sensor_info'
        while True:
            # Saca datos online y los revisa para guardarlos en csv...

            if event == 'sensor_info':
                window, event, value = save.sensor_info(window)
                numsen = int(value['NumSen'])
                start = value['Start'] + '%20' + value['Start_hour'] + ':00'
                end = value['End'] + '%20' + value['End_hour'] + ':00'
            
            if event == 'Continue':
                window, event, indx = save.sensors_in_field(window, numsen)
            
            if event == 'Next':
                data = save.total_extraction(indx,start,end)

                # Se comprueba que no existan huecos de información
                window, event, holes, num_csv_per_sensor = save.holes_verification(window, data, indx)

                if event == 'Fix_errors':
                    window, data = save.fix_save(window, num_csv_per_sensor, holes, data)
                    event = 'Save'
                else:
                    event = 'Save'

            if event == 'Save':
                # Guardo los archivos.
                window, event = save.save(window, data, indx, value['Start'], value['End'])
            
            if event == 'Finalizar':
                gui.shutdown(window)

    elif event == 'Plot':
        # Saca datos online o por csv y los procesa para graficarlos.
        window, event = gui.gui_graph_creation(window)

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
                    if event != 'SensorDistribution':
                        continue
                    # Almacenamos los datos importantes de esto
                    rows = int(value['Rows'])
                    columns = int(value['Columns'])
                    col_dist = int(value['Col_dis'])
                    row_dist = int(value['Row_dis'])
                    num_sen = int(value['NumSen'])

                if event == 'SensorDistribution':
                    # Solicitamos la distribución de los sensores.
                    window, event, indx = gui.distribution(window,num_sen,rows,columns)

                if event == 'Date_hour':
                    # Solicitamos al usuario los rangos de fecha de las mediciones.
                    window, event, value = gui.date_hour(window)
                    if event != 'Extraction':
                        continue
                    start = value['Start'] + '%20' + value['Start_hour'] + ':00'
                    end = value['End'] + '%20' + value['End_hour'] + ':00'

                if event == 'Extraction':
                    x_axis,y_axis,z_axis,minimum_dates,maximum_dates,holes,num_csv_per_sensor,it,PMType = gui.extraction(PMType,rows,
                                                                                                        columns,col_dist,row_dist,
                                                                                                        indx,start,end)
                    if it > 0:
                        window, event = gui.holes_warning(window,holes,num_csv_per_sensor)
                    else:
                        event = 'Graphs'

                if event == 'Fix_errors':
                    # Solicito archivos csv
                    window, value = gui.csv_online(window, num_csv_per_sensor, holes)
                    # Arreglo los huecos
                    z_axis, limites, error = gui.fixing(value,z_axis,PMType,holes,minimum_dates, maximum_dates, key='Online')

                    if error != True:
                        event = 'Graphs'
                    else:
                        event = 'Fix_errors'

                if event == 'Graphs':
                    window, event, value = gui.graph_domain(window, x_axis, y_axis, z_axis, columns, rows, row_dist, col_dist, PMType, indx, limites)

                if event == 'No volver a graficar':
                    # Falta esto...
                    # Termino el programa...
                    # Pregunto si quiere regresar al inicio para hacer otra cosa...

                    pass

        elif event == 'CSV':
            event = 'Extraction'
            while True:
                if event == 'Extraction':
                    window, event, value, minimum, maximum = Csv.csv_files(window)
                    csv_data = value
                    value = []

                if event == 'TypeData':
                    # Pregunta que tipo de dato quiere analizar
                    window, event, value = Csv.data_type(window)
                    PMType = value

                if event == 'Return':
                    pass
                    # Como le hago para regresar hasta gui_creation???

                if event == 'Sensor_info':
                    # Pedimos al usuario información sobre el número de sensores,
                    # distancia entre ellos, etc.
                    window, event, value = Csv.sensors_info(window)
                    if event != 'SensorDistribution':
                        continue
                    # Almacenamos los datos importantes de esto
                    rows = int(value['Rows'])
                    columns = int(value['Columns'])
                    col_dist = int(value['Col_dis'])
                    row_dist = int(value['Row_dis'])
                    num_sen = int(value['NumSen'])
                    x0 = int(value['X0'])
                    y0 = int(value['Y0'])

                if event == 'SensorDistribution':
                    # Solicitamos la distribución de los sensores.
                    window, event, indx, x_axis, y_axis = Csv.distribution(window,num_sen,rows,columns,row_dist,col_dist,x0,y0)

                if event == 'Date_hour':
                    # Solicitamos al usuario los rangos de fecha de las mediciones
                    window, event, value, days = Csv.date_hour(window, key=1)
                    if event != 'Extraction':
                        continue
                    event = 'Graph'

                    start = value['Start'] + ' ' + value['Start_hour'] 
                    end = value['End'] + ' ' + value['End_hour']

                if event == 'Graph':
                    # Se preguntan cosas de las graficas
                    window, value = Csv.graph_domain(window)

                    # Se preparan los datos
                    data, limites, PMType2 = Csv.data_average(csv_data, minimum, maximum, value['delta'], PMType, start, end)

                    # Se grafica
                    window, event, value = Csv.graph(window, x_axis, y_axis, data, columns, rows, row_dist, col_dist, PMType2, indx, limites, value)

        else:
            gui.shutdown(window)
    
    else:
        gui.shutdown(window)