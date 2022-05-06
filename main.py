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
                event, indx = gui.distribution(window,num_sen,rows,columns)
            
            if event == 'Date_hour':
                event, value = gui.date_hour(window)



    elif event == 'CSV':
        pass

    else:
        gui.shutdown(window)