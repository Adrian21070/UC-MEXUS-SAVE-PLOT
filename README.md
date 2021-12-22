# Graficado de Datos Proyecto UC-MEXUS
El presente repositorio contiene multiples scripts que se crearon con el objetivo de poder graficar informacion proveniente de medidciones de material particulado de arreglos de sensores PurpleAir a traves de una superficies. En este aspecto el repositorio contiene 4 scripts clave, los cuales seran descritos de manera especifica mas adelantes. De forma general los scripts tienen las siguientes funciones:
- **TSClasses.py:** Script que contiene las funciones necesarias para obtener los datos de un canal de Thingspeak
- **LivePlot.py:**  Script que permite graficar en tiempo real los datos recibidos de un Sensor PurpleAir (utilizando las funciones de TSclasses.py)
- **AvgFunctions.py:** Script con las funciones necesarias para hacer distintos tipos de graficas y animaciones a partir de datos recibidos de canales de thingspeak (utilizando funciones de *TSclasses.py*) o archivos CSV
- **GUI.py:** Script para generar una interfaz de usuario que permita de manera facil y rapida realizar el graficado de datos a partir de las funciones de *AvgFunctions.py*
