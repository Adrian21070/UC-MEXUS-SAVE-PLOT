# Graficado de Datos Proyecto UC-MEXUS
El presente repositorio contiene multiples scripts que se crearon con el objetivo de poder graficar informacion proveniente de medidciones de material particulado de arreglos de sensores PurpleAir a traves de una superficies. En este aspecto el repositorio contiene 4 scripts clave, los cuales seran descritos de manera especifica mas adelantes. De forma general los scripts tienen las siguientes funciones:
- **TSClasses.py:** Script que contiene las funciones necesarias para obtener los datos de un canal de Thingspeak
- **LivePlot.py:**  Script que permite graficar en tiempo real los datos recibidos de un Sensor PurpleAir (utilizando las funciones de TSclasses.py)
- **AvgFunctions.py:** Script con las funciones necesarias para hacer distintos tipos de graficas y animaciones a partir de datos recibidos de canales de thingspeak (utilizando funciones de *TSclasses.py*) o archivos CSV
- **GUI.py:** Script para generar una interfaz de usuario que permita de manera facil y rapida realizar el graficado de datos a partir de las funciones de *AvgFunctions.py*

Nota: Estos scripts unicamente han sido probados con Python 3.7 en Windows 10.

## Estructura del repositorio
El repositorio esta conformado por los scripts previamente mencionados, los cuales no se encuentran en ninguna carpeta. Durante el desarrollo de este proyecto se crearon varios scripts con el objetivo de comprender como descargar datos y proponer distintas maneras de graficarlos. La mayoria de estos scripts fueron simplificados y se integraron a alguno de los 4 scripts clave (prinicpalmente *AvgFunctions.py*), por lo que se volvieron obsoletos. Sin embargo, en caso de ser necesarios revisarlos estos se colocaron en la carpeta [**Backup**](/Backup). Adicionalmente, en este repositorio se encuentran dos carpetas con configuraciones. Por un lado, la carpeta [**.idea**](/.idea) contiene las configuraciones de PyCharm al ejecutar este repositorio (esta carpeta no es necesaria y puede ser eliminada sin causar problemas en el repositorio. Por otro lado, la carpeta [**__pycache__**](/__pycache__) contiene archivos que son versiones simplificadas de algunos scripts que permiten ejecutarlos de manera rapida al ser llamados por otro script (por ejemplo cuando el script *GUI.py* llama una funcion de *AvgFunctions.py*).
## Scripts de Respaldo
Como se mencionó en la sección anterior, varios scripts fueron de prueba. Al volverse obsoletos estos se transfierieron la carpeta **Backup**. A traves de esta sección se describira en que consistieron dichos scripts. Sin embargo, es importante mencionar que la mayoria de estos scripts no fueron comentados.
- **CSV_read.py:** Script que abre un archivo CSV (correspondiente a un sensor), lee su contenido y grafica la concentración de PM a traves del tiempo. De manera mas especifca, grafica las concentraciones de PM1.0, PM2.5 y PM10.0.
- **PlotAnimation.py:** Script para graficar las mediciones de sensores PurpleAir distribuidos en cierto lugar durante una cantidaad de tiempo. Los datos se obtienen de canales de thingspeak. 
- **PurpleAirReadTest.py:** Este script usa las funciones del script TSClasses para abrir obtener los datos de un canal de thingspeak y posteriormente graficar la concentracion de PM1.0, PM2.5 y PM10.0 contra el tiempo.
- **ReadMultiplePA.py:** Script capaz de obtener los datos de 3 sensores PurpleAir, a partir de su canales de thingspeak, para despues graficar la información de PM1.0, PM2.5 y PM10.0 con respecto al tiempo. 
- **ReadMultiplePACSV.py:** Script diseñado para graficar los datos de la primera campaña de monitoreo (llevada a cabo en el Parque de Investigación e Innovación Tecnológica). De manera mas especifica, este script usa 6 archivos csv con datos de mediciones. Despues se guardan en listas los datos de concentraciones PM1.0 para cada sensor, se hace un promedio de las mediciones de cada sensor y se grafican los datos en un espacio tridimensional. Donde el eje Y y X describen la ubicación de los sensores y el eje Z describe la concentracion de PM en un rango de tiempo.
- **ReadMultiplePACSV_AVG.py:** Script muy similar al anterior. Sin embargo, se le realizaron algunas modificaciones para graficar los datos obtenidos de un segunda campaña de monitoreo (en el Tec de Monterrey) donde se utilizo una mayor cantidad de sensores.
- **ReadMultiplePACSV_AVG_10_MIN.py:** Script similar a *ReadMultiplePACSV.py*. Sin embargo, en vez de hacer un promedio de todos los datos en cada archivo csv, este script (a partir de un hora de inicio) hace una grafica de un promedio de 10 minutos.
- **Test.csv:** Archivo de prueba para validar el graficado de datos a partir de un archivo csv
- **testtime.py:** Script para comprender como generar formatos de fecha en python.
## Scripts Principales
#### TSClasses.py
#### LivePlot.py
#### AvgFunctions.py
#### GUI.py
## TO DO:
