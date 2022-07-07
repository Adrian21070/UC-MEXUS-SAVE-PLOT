import main_gui as gui
import save_data2 as save
import csv_plot2 as Csv
import plots as Func

"""
Como compruebo que los csv que me dan para reparar huecos si son los adecuados??? Funcion fix_save.
(Sensores sin bateria)

Falta la opcion de no interpolacion (plot simple y surf simple...)

Lo anterior esta practicamente terminado, solo falta el caso de prueba que (la matriz sea más grande que el area de sensores)...

A todos los exit, hay que agregarles esto si les falta, if event in ('Exit', None): especificamente el None...
                                                            shutdown(window)
"""

if __name__ == '__main__':

    # Creamos una interfaz que pregunte que acción quiere realizar.
    window, event = gui.save_or_graph()

    if event == 'Save_data':
        event = 'sensor_info'
        while True:
            # Saca datos online y los revisa para guardarlos en csv...

            """
            Aquí falta hacer la corrección lineal si el usuario desea, checar que la GUI este bonita

            Returns tambien.
            """

            if event == 'sensor_info':
                key = True
                while key:
                    window, event, value, key = save.sensor_info(window)

                start = value['Start'] + '%20' + value['Start_hour'] + ':00'
                end = value['End'] + '%20' + value['End_hour'] + ':00'
                cargar = value['Cargar']
                holes_size = value['holes_size']
                del key
            
            if cargar:
                # Solicita un csv para cambiar los ids y keys de los sensores.
                key = True
                while key:
                    key, window, event = save.Cargar(window)
                del key

            if event == 'Continue':
                while True:
                    indx, window, event = save.sensors_in_field(window)
                    if not isinstance(indx, bool):
                        break
            
            if event == 'Next':
                data, window = save.total_extraction(indx, start, end, window)

                # Se comprueba que no existan huecos de información
                window, event, holes, num_csv_per_sensor = save.holes_verification(window, data, indx, holes_size)

                if event == 'Fix_errors':
                    key = True
                    while key:
                        window, data, key = save.fix_save(window, num_csv_per_sensor, holes, data)
                    event = 'Ajuste'
                elif event == 'Exit':
                    gui.shutdown(window)
                else:
                    # Paso las fechas a UTC
                    for ii in data.keys():
                        val = data[ii]['created_at']
                        val = Func.conversor_datetime_string(val, key=2) #Convierto a utc
                        data[ii]['created_at'] = val
                    event = 'Ajuste'
            
            if event == 'Ajuste':
                window, event, data = save.ajuste(window, data)
                pass

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
        # Saca datos por csv y los procesa para graficarlos.
        event = 'CSV'
        
        if event == 'CSV':
            event = 'Extraction'
            memory = {}
            while True:
                if event == 'Extraction':
                    window, event, value, minimum, maximum = Csv.csv_files(window)
                    csv_data_raw = value #csv_data is in UTC
                    del value

                if event == 'TypeData':
                    # Pregunta que tipo de dato quiere analizar
                    window, event, value = Csv.data_type(window)
                    if event != 'Sensor_info':
                        pass
                    else:
                        PMType_init = value

                if event == 'Return':
                    pass
                    # Como le hago para regresar hasta gui_creation???

                if event == 'Sensor_info':
                    # A partir de los archivos, deducimos los numeros de los sensores.
                    # Pedimos al usuario información sobre las columnas y filas de sensores,
                    # distancia entre ellos, etc.
                    key = True
                    while key:
                        window, event, value, indx, key = Csv.sensors_info(list(csv_data_raw.keys()),window)
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
                        window, event, indx, carretera_lateral, key, rows_sen = Csv.distribution(window,indx,rows,columns)
                    del key
                    # Se debe aplicar un filtro a data a partir de indx
                    if event == 'Coordenadas':
                        csv_data = Csv.filtro_data(csv_data_raw, indx)

                if event == 'Coordenadas':
                    # Ahora indx es un diccionario con las coordenadas del usuario y el numero del sensor.
                    window, event, indx, x_axis, y_axis = Csv.coordenadas(window, rows, row_dist, columns, col_dist, x0, y0, indx, carretera_lateral)
                
                ### Aquí inicia un bucle de graficado
                if event == 'Tipo_de_grafico':
                    window, graph_selection, event, value_anim, memory = Csv.type_graph(window, memory)

                if event == 'Date_hour':
                    # Solicitamos al usuario los rangos de fecha de las mediciones a graficar
                    llave = True
                    while llave:
                        window, event, value, days, memory, llave = Csv.date_hour(window, maximum, minimum, memory, key=1)
                    del llave
                    if event != 'Styles':
                        continue

                    start = value['Start'] + ' ' + value['Start_hour'] 
                    end = value['End'] + ' ' + value['End_hour']

                if event == 'Styles':
                    # Se preguntan cosas de las graficas
                    window, event, surface, lateral_avg, historico, memory, typedate = Csv.graph_domain(window, graph_selection, value_anim, PMType_init, memory)

                if event == 'Average':
                    # Se preparan los datos
                    new_data_anim, limites_anim, new_data_est, limites_est, PMType = Csv.data_average(csv_data, minimum, maximum, value_anim, graph_selection, PMType_init, start, end, typedate)
                    #data, limites, PMType2 = Csv.data_average(csv_data, minimum, maximum, value_anim, PMType, start, end)
                    event = 'Visualization'

                    """
                    Solo te falta modificar tamaños en toda la gui.

                    Faltan try-except??? Ni idea.
                    """
                if event == 'Visualization':

                    try:
                        if new_data_anim:
                            # Realiza la animación y la guarda.
                            if (graph_selection['Surface'] and graph_selection['An_superficie']):
                                #Animación superficie
                                window, event = Csv.graph(window, x_axis, y_axis, new_data_anim, columns, rows, row_dist, col_dist, PMType, indx, limites_anim, graph_selection, value_anim, surface, 'Surface', carretera_lateral, rows_sen)

                            if (graph_selection['LateralAvg'] and graph_selection['An_lateral']):
                                #Animación promedio lateral
                                window, event = Csv.graph(window, x_axis, y_axis, new_data_anim, columns, rows, row_dist, col_dist, PMType, indx, limites_anim, graph_selection, value_anim, lateral_avg, 'LateralAvg', carretera_lateral, rows_sen)
                            
                            if (graph_selection['Historico']):
                                # Promedios historicos
                                window, event = Csv.graph(window, x_axis, y_axis, new_data_anim, columns, rows, row_dist, col_dist, PMType, indx, limites_anim, graph_selection, value_anim, historico, 'Historico', carretera_lateral, rows_sen)
                            #Historico # (Construccion)

                        if new_data_est:
                            # Realiza la grafica y la guarda
                            if (graph_selection['Surface'] and graph_selection['Es_superficie']):
                                #Superficie estatica
                                window, event = Csv.graph(window, x_axis, y_axis, new_data_est, columns, rows, row_dist, col_dist, PMType, indx, limites_est, graph_selection, value_anim, surface, 'Surface', carretera_lateral, rows_sen)

                            if (graph_selection['LateralAvg'] and graph_selection['Es_lateral']):
                                #Lateral estatica
                                window, event = Csv.graph(window, x_axis, y_axis, new_data_est, columns, rows, row_dist, col_dist, PMType, indx, limites_est, graph_selection, value_anim, lateral_avg, 'LateralAvg', carretera_lateral, rows_sen)

                    except:
                        # Indicar que existio un error, probable por que falto un dato en el formato de la grafica o en los datos.
                        window, event = Csv.error_grafica(window)
                        
                    del new_data_anim, new_data_est, limites_anim, limites_est
                
                if event == 'Finalizar programa':
                    gui.shutdown(window)

        else:
            gui.shutdown(window)