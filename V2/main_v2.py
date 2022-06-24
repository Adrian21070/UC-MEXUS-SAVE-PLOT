import main_gui as gui
import save_data2 as save
import csv_plot2 as Csv

"""
Holes verification, tamaño de hueco en segundos, modificable por el usuario?

Sensors_info, debo preguntar de que lado se encuentra la avenida laterial???

Incluir un popup al momento de pasar por extracción de datos, tarda mucho ya que son muchos campos.
Esto relajara al usuario de que si se esta ejecutando algo.

Datatype  Puedo hacerlo frame y poner todo en el centro mas estetico

Como compruebo que los csv que me dan para reparar huecos si son los adecuados??? Funcion fix_save.
"""

"""
Cosas a modificar -> Para que el usuario modifique los titulos de grafica, archivo csv_plot, linea: 420
"""


if __name__ == '__main__':

    # Creamos una interfaz que pregunte que acción quiere realizar.
    window, event = gui.save_or_graph()

    if event == 'Save_data':
        event = 'sensor_info'
        while True:
            # Saca datos online y los revisa para guardarlos en csv...

            if event == 'sensor_info':
                window, event, value = save.sensor_info(window)
                #numsen = int(value['NumSen'])
                start = value['Start'] + '%20' + value['Start_hour'] + ':00'
                end = value['End'] + '%20' + value['End_hour'] + ':00'
                cargar = value['Cargar']
            
            if cargar:
                # Solicita un csv para cambiar los ids y keys de los sensores.
                key = True
                while key:
                    key, window = save.Cargar(window)
                event = 'Continue'
                del key

            if event == 'Continue':
                while True:
                    indx, window, event = save.sensors_in_field(window)
                    if not isinstance(indx, bool):
                        break
                #window, event, indx = save.sensors_in_field(window)
            
            if event == 'Next':
                data, window = save.total_extraction(indx, start, end, window)

                # Se comprueba que no existan huecos de información
                window, event, holes, num_csv_per_sensor = save.holes_verification(window, data, indx)

                if event == 'Fix_errors':
                    key = True
                    while key:
                        window, data, key = save.fix_save(window, num_csv_per_sensor, holes, data)
                    event = 'Save'
                else:
                    event = 'Save'

            if event == 'Save':
                # Guardo los archivos.
                window, event = save.save(window, data, indx, value['Start'], value['End'])
            
            if event == 'Graficar':
                # Se queda data, start, end, indx

                # Principalmente data...
                # Todo lo demas eliminado.
                # Extraigo minimo y maximo de cada sensor...

                # event = TypeData
                # csv_data = data
                # del data
                pass

            if event == 'Finalizar':
                gui.shutdown(window)
    
    elif event == 'Plot':
        # Saca datos online o por csv y los procesa para graficarlos.
        window, event = gui.gui_graph_creation(window)

        if event == 'CSV':
            event = 'Extraction'
            while True:
                if event == 'Extraction':
                    window, event, value, minimum, maximum = Csv.csv_files(window)
                    csv_data = value
                    del value

                if event == 'TypeData':
                    # Pregunta que tipo de dato quiere analizar
                    window, event, value = Csv.data_type(window)
                    if event != 'Sensor_info':
                        pass
                    else:
                        PMType = value
                
                # No seria mas eficiente si desde typeData filtramos los datos relevantes para el usuario?
                # Creo que el usuario puede pedir hacer graficas con otro tipo de dato cuando este en la zona de graficado...

                if event == 'Return':
                    pass
                    # Como le hago para regresar hasta gui_creation???

                if event == 'Sensor_info':
                    # A partir de los archivos, deducimos los numeros de los sensores.
                    # Pedimos al usuario información sobre las columnas y filas de sensores,
                    # distancia entre ellos, etc.
                    key = True
                    while key:
                        window, event, value, indx, key = Csv.sensors_info(list(csv_data.keys()),window)
                    del key

                    if event != 'SensorDistribution':
                        continue
                    # Almacenamos los datos importantes de esto
                    rows = int(value['Rows'])
                    columns = int(value['Columns'])
                    col_dist = float(value['Col_dis'])
                    row_dist = float(value['Row_dis'])
                    num_sen = len(indx)
                    x0 = float(value['X0'])
                    y0 = float(value['Y0'])

                if event == 'SensorDistribution':
                    # Solicitamos la distribución de los sensores.
                    key = True
                    while key:
                        window, event, indx, key = Csv.distribution(window,indx,rows,columns)

                if event == 'Coordenadas':
                    window, event, indx, x_axis, y_axis = Csv.coordenadas(window, rows, row_dist, columns, col_dist, x0, y0, indx)
                    # Ahora indx es un diccionario con las coordenadas del usuario y el numero del sensor.

                if event == 'Date_hour':
                    # Solicitamos al usuario los rangos de fecha de las mediciones
                    window, event, value, days = Csv.date_hour(window, maximum, minimum, key=1)
                    if event != 'Graph':
                        continue

                    start = value['Start'] + ' ' + value['Start_hour'] 
                    end = value['End'] + ' ' + value['End_hour']

                if event == 'Graph':
                    # Se preguntan cosas de las graficas
                    window, value = Csv.graph_domain(window)

                    # Se preparan los datos
                    data, limites, PMType2 = Csv.data_average(csv_data, minimum, maximum, value['delta'], PMType, start, end)

                    # Se grafica
                    window, event, value = Csv.graph(window, x_axis, y_axis, data, columns, rows, row_dist, col_dist, PMType2, indx, limites, value)

                    del data

        else:
            gui.shutdown(window)