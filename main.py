# Librerias
import sys
import gui2 as gui
import save_data as save
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
                #gui.saving_data(window)
            
            if event == 'Continue':
                window, event, indx = save.sensors_in_field(window, numsen)
            
            if event == 'Next':
                data = save.total_extraction(indx,start,end)

                # Se comprueba que no existan huecos de información
                window, event, holes, num_csv_per_sensor = save.holes_verification(window, data, indx)

            if event == 'Fix_errors':
                # Solicito archivos csv
                window, value = gui.csv_online(window, num_csv_per_sensor, holes)
                # Arreglo los huecos
                z_axis, limites, error = gui.fixing(value,data,PMType,holes,minimum_dates, maximum_dates)

                if error != True:
                    event = 'Graphs'
                else:
                    event = 'Fix_errors'

        
    else:
        # Saca datos online o por csv y los procesa para graficarlos.
        window, event = gui.gui_graph_creation()

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
                    z_axis, limites, error = gui.fixing(value,z_axis,PMType,holes,minimum_dates, maximum_dates)

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
                    # Solicitamos al usuario los rangos de fecha de las mediciones
                    window, event, value, days = gui.date_hour(window, key=1)
                    if event != 'Extraction':
                        continue
                    event = 'Save or Graph'
                    #start = value['Start'] + '%20' + value['Start_hour'] + ':00'
                    #end = value['End'] + '%20' + value['End_hour'] + ':00'

                if event == 'Save or Graph':
                    # Gui que pregunta si queremos guardar o solo graficar el csv.
                    pass

                # Creamos una gui para que cargue sus archivos en orden ascendente???

                if event == 'Extraction':
                    sorted_index = list(indx.values()).sort()
                    # Key == 1, fechas en datetime
                    # Key != 1, fechas en string.
                    window, event, value = gui.csv_files(sorted_index, days, key=1)
                    csv_data = value

        else:
            gui.shutdown(window)