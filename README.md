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
Los sensores PurpleAir suben información a la nube, la cual puede ser accesada usando el API de PurpleAir o el API de Thingspeak. Debido a que en un inicio se desconocia como obtener las llaves para utilizar el API de PurpleAir se opto por usar el API de Thingspeak. En este aspecto, esta API genera 4 canales por cada sensor PurpleAir, esto debido a que cada uno de estos dispositivos de PurpleAir a su vez cuentan con dos sensores (sensor A y B) los cuales reportan la misma información y unicamente permiten validar que ambos sensores funcionen de manera correcta. Los datos de cada uno de estos sensores dentro del dispositivo se entrega en 2 partes (un canal primario y uno secundario) resultando así en los 4 canales por dispositivo PurpleAir. Para acceder a los datos de los sensores se tenia que acceder a los canales previamente mencionados. Con este objetivo en mente se generó un script con funciones capaces de acceder a un canal (a partir de un ID y una llave) y llamar un cantidad definida de datos de dicho canal. Es importante mencionar que dichas funciones pueden ser utilizadas por otros scripts. 

Nota: Adicionalmente, es importante mencionar que para obtener el ID y las llaves de un dispositivo PurpleAir (considerando que este ya fue registrado en el sitio web de PurpleAir), se debe acceder a este [link](https://www.purpleair.com/data.json) (el cual contiene la lista de todos los sensores registrados en PurpleAir), buscar el dispositivo por su nombre, copiar el numero de dispositivo y acceder a:

```
https://www.purpleair.com/json?show=SEN_NUM
```
Donde SEN_NUM es remplazado por el numero de dispositivo. Este ultimo enlace contendra los IDs y llaves para todos los canales del dispositivo PurpleAir, los cuales llevan por nombre "THINGSPEAK_PRIMARY_ID", "THINGSPEAK_PRIMARY_ID_READ_KEY","THINGSPEAK_SECONDARY_ID" y "THINGSPEAK_SECONDARY_ID_READ_KEY". Por ejemplo si primero buscamos el dispositivo con nombre *GIECC_UCMEXUS_1* encontraremos que su numero es 104774 y al utilizar:

```
https://www.purpleair.com/json?show=104774
```
encontramos los siguientes IDs y llaves:
- Sensor A:
    - "THINGSPEAK_PRIMARY_ID":"1367948"
    - "THINGSPEAK_PRIMARY_ID_READ_KEY":"TMTVNTYUXGGT7MK3"
    - "THINGSPEAK_SECONDARY_ID":"1367949"
    - "THINGSPEAK_SECONDARY_ID_READ_KEY":"N35ZTFXU25M0A6CA"
- Sensor B:
    - "THINGSPEAK_PRIMARY_ID":"1367950"
    - "THINGSPEAK_PRIMARY_ID_READ_KEY":"UJUFOPEW3TOQWV8W"
    - "THINGSPEAK_SECONDARY_ID":"1367951"
    - "THINGSPEAK_SECONDARY_ID_READ_KEY":"S26M6JT22KN1VIDK"

#### LivePlot.py
Con el objetivo de poder monitorear un sensor en tiempo real y validar que sus mediciones sean correctas se creo este código. Este script utiliza el API de thingspeak para acceder a un canal, obtener una cantidad definida de datos de ese canal graficar dichas concentraciones de PM contra el tiempo y cada 2.1 minutos verificar si se han recibido nuevos datos para actualizar el grafico. Esta validación de nuevos datos se hace a traves de una funcion llamada animate() donde se obtiene la ultima medición añadida a un canal de thingspeak, para posteriormente checar si el tiempo en el que se obtuvo dicha medición coincide con una que ya se tenia. En caso de ser así pues este no es un dato nuevo. Caso contrario, es una nueva medición y se guardan en listas la estampa de tiempo y el la medición. Estas listas son las que se utiliza para hacer el grafico que se actualiza periodicamente. Finalmente, para modificar el ID, llave y numero de resultados se deben modificar las lineas 15, 16 y 44 del script respectivamente.
#### AvgFunctions.py

#### GUI.py

## TO DO:
- [ ] Definir hora de inicio (en PurpleAir no se pone hora, busca de la ultima medición a cierta cantidad de valores en el pasado)
- [x] #739
- [ ] https://github.com/octo-org/octo-repo/issues/740
- [ ] Add delight to the experience when all tasks are complete :tada:
