import main_gui as gui
import save_data2 as save
import csv_plot2 as Csv

"""
Holes verification, tamaño de hueco en segundos, modificable por el usuario? (Pendiente)

Sensors_info, debo preguntar de que lado se encuentra la avenida laterial??? (Pendiente)

Incluir un popup al momento de pasar por extracción de datos, tarda mucho ya que son muchos campos.
Esto relajara al usuario de que si se esta ejecutando algo. (Pendiente)

Datatype Puedo hacerlo frame y poner todo en el centro mas estetico

Como compruebo que los csv que me dan para reparar huecos si son los adecuados??? Funcion fix_save.
(Sensores sin bateria)
"""

"""


(Guardar en memoria los estilos que dio el usuario.)




"""



if __name__ == '__main__':

    # Creamos una interfaz que pregunte que acción quiere realizar.
    window, event = gui.save_or_graph()

    if event == 'Save_data':
        event = 'sensor_info'
        while True:
            # Saca datos online y los revisa para guardarlos en csv...

            """
            Aquí falta hacer la corrección lineal si el usuario desea, checar que la GUI este bonita,
            y que lea un folder en lugar de multiples archivos para los huecos de información...
            indicandole al usuario que el folder debe tener unicamente los archivos que tienen huecos.

            Returns tambien.
            """

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
                    # Ahora indx es un diccionario con las coordenadas del usuario y el numero del sensor.
                    window, event, indx, x_axis, y_axis = Csv.coordenadas(window, rows, row_dist, columns, col_dist, x0, y0, indx)
                
                ### Aquí inicia un bucle de graficado
                if event == 'Tipo_de_grafico':
                    window, graph_selection, event, value_anim = Csv.type_graph(window)

                if event == 'Date_hour':
                    # Solicitamos al usuario los rangos de fecha de las mediciones a graficar
                    window, event, value, days = Csv.date_hour(window, maximum, minimum, key=1)
                    if event != 'Styles':
                        continue

                    start = value['Start'] + ' ' + value['Start_hour'] 
                    end = value['End'] + ' ' + value['End_hour']

                if event == 'Styles':
                    # Se preguntan cosas de las graficas
                    window, event, surface, lateral_avg, historico = Csv.graph_domain(window, graph_selection, value_anim, PMType)

                if event == 'Average':
                    # Se preparan los datos
                    new_data_anim, limites_anim, new_data_est, limites_est, PMType = Csv.data_average(csv_data, minimum, maximum, value_anim, graph_selection, PMType, start, end)
                    #data, limites, PMType2 = Csv.data_average(csv_data, minimum, maximum, value_anim, PMType, start, end)
                    event = 'Visualization'

                    """
                    Estara bien dar un preview de la grafica resultante para animación con el formato que me dio el usuario? y preguntarle
                    si esta conforme con eso???, esto ahorrara tiempo para el... (Pendiente)

                    Solo te falta modificar tamaños en toda la gui.

                    Faltan try-except??? Ni idea.
                    """
                if event == 'Visualization':
                    if new_data_anim:
                        # Realiza la animación y la guarda.
                        if (graph_selection['Surface'] and graph_selection['An_superficie']):
                            #Animación superficie
                            Csv.graph(window, x_axis, y_axis, new_data_anim, columns, rows, row_dist, col_dist, PMType, indx, limites_anim, graph_selection, value_anim, surface, 'Surface')

                        if (graph_selection['LateralAvg'] and graph_selection['An_lateral']):
                            #Animación promedio lateral
                            Csv.graph(window, x_axis, y_axis, new_data_anim, columns, rows, row_dist, col_dist, PMType, indx, limites_anim, graph_selection, value_anim, lateral_avg, 'LateralAvg')

                    if new_data_est:
                        # Realiza la grafica y la guarda
                        if (graph_selection['Surface'] and graph_selection['Es_superficie']):
                            #Superficie estatica
                            Csv.graph(window, x_axis, y_axis, new_data_est, columns, rows, row_dist, col_dist, PMType, indx, limites_est, graph_selection, value_anim, surface, 'Surface')

                        if (graph_selection['LateralAvg'] and graph_selection['Es_lateral']):
                            #Lateral estatica
                            Csv.graph(window, x_axis, y_axis, new_data_est, columns, rows, row_dist, col_dist, PMType, indx, limites_est, graph_selection, value_anim, lateral_avg, 'LateralAvg')

                        #Historico # (Construccion)


                    del new_data_anim, new_data_est, limites_anim, limites_est

        else:
            gui.shutdown(window)