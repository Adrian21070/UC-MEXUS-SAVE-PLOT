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
Con el objetivo de poder monitorear un sensor en tiempo real y validar que sus mediciones sean correctas se creo este código. Este script utiliza el API de thingspeak para acceder a un canal, obtener una cantidad definida de datos de ese canal graficar dichas concentraciones de PM contra el tiempo y cada 2.1 minutos verificar si se han recibido nuevos datos para actualizar el grafico. Esta validación de nuevos datos se hace a traves de una funcion llamada animate() donde se obtiene la ultima medición añadida a un canal de thingspeak, para posteriormente checar si el tiempo en el que se obtuvo dicha medición coincide con una que ya se tenia. En caso de ser así pues este no es un dato nuevo. Caso contrario, es una nueva medición y se guardan en listas la estampa de tiempo y el la medición. Estas listas son las que se utiliza para hacer el grafico que se actualiza periodicamente. Finalmente, para modificar el ID, llave y numero de resultados se deben modificar las lineas 15, 16 y 44 del script respectivamente.MODIFICAR PM
#### AvgFunctions.py
Para evitar tener en un mismo script la interfaz de usuario y las funciones a ejecutar al presionar botones especificos de la interfaz de usuario, se optó por separar estos dos. Este código contiene las funciones a ejecutar por el GUI. De manera mas especifica este script contiene 7 funciones las cuales se describiran a continuación:
- **avg():** esta función permite sacar un promedio de los elementos de una lista. Por lo que unicamente es necesario proveerle un lista y esta función regresara el promedio obtenido.
- **GraphAvg():** función que intenta acceder a una cantidad definida de archivos csv (correspondientes asensores PurpleAir) para despues buscar mediciones para cierto tipo de PM a partir de cierta hora y hasta cierta hora en cada uno de los archivos csv.En este aspecto, es importante mencionar que la funcion itera a traves de cada uno de los archivos csv, por lo que estos deben tener un nombre especifico, correspondiente al numero de sensor ("S1","S2","S3","S4",...). Las mediciones de cada sensor se añaden a una lista, para despues obtener el valor promedio usando la función *avg.py*. Los promedios de cada uno de los sensores se añade a una lista (que representa los valores del eje z). Posteriormente, a partir del arreglo definido para los sensores y la distancia entre estos se generan do listas mas una que define las posiciones en el eje X de cada sensor y otra que define las posiciones en el eje Y. Adicionalmente, es importante mencionar que el primer se ubica en la coordenada (0,0). Despues, se define el formato de la grafica, se convierten las listas con los datos de todos los ejes coordenados a arreglos numpy para poder hacer interpolacion entre los sensores y obtener una grafica con curvas suaves. Finalmente se genera el grafico.
- **LateralAvg():** Funciona de manera similar a la función anterior. Sin embargo, una vez obtenida la lista de promedios para cada sensor, se itera a traves de cada fila y se obtiene un valor promedio para las columnas de esa fila los resultados se añaden despues a una lista. Despues, unicamente se genera una lista describiendo la posicion de los sensores en el eje Y (a partir de la distancia entre filas). Posteriormente, se definen las configuraciones del grafico para despues generar un grafico 2D a partir de archivos CSV. es importante mencionar que en este caso el promedio de la primera fila de sensores se encuentra en Y = 0.
- **animate():** Funcion llamada para animar un grafico. Esta funcion recibe las mediciones de un arreglo de sensores en un periodo de tiempo determinado. Al mismo tiempo, esta funcion recibe la iteración actual (el numero de iteraciones esta definido por la cantidad de datos recolectados por cada sensor) por lo que esta función itera a traves de todos los sensores y obtiene la medicion de cierto tipo de PM en un instante especifico de tiempo (definido por la iteracion actual) para cada sensor, estos valores se guardan en una lista que define los valores del grafico en el eje Z. Por otro lado, los valores en los ejes X y Y se le entregan directamente a la función en forma de listas. Las listas de todos los ejes se convierten a arreglos numpy para poder interpolar y suavizar las curvas del grafico. Adicionalmente, se definen las configuraciones del grafico y se crea el grafico o se actualiza en caso de que ya existiese. Esta funcion se llama periodicamente al desear crear una animación, con cada llamada el valor de la iteración actual cambia, por lo que se obtienen los valores medidos por los sensores en otros instantes de tiempo, generando así una animación. 
- **AnimationCSV():** Esta funcion tra
#### GUI.py

## Pendientes:
- [x] la GUI debe permitir definir hora de inicio para el graficado de datos (en PurpleAir no se pone hora, busca de la ultima medición a cierta cantidad de valores en el pasado).
- [x] la GUI debe permitir definir la duración de tiempo para hacer el promedio.
- [X] Generar un grafico 3D del promedio de mediciones en un espacio y tiempo definido.
- [X] El grafico 3D debe permitir visualizar los datos "desde arriba" generando un mapa de calor 2D, que muestre ejes X y Y.
- [ ] Promediar valores a lo largo del eje Y (una fila) para generar un segundo gráfico en 2D, que muestra la concentración promedio de PM a medida que nos alejamos de la vía, mostrando ejes X y Z (**Pendiente para datos de obtenidos de thingspeak**).
- [x] la GUI debe permitir definir duración de tiempo total para la animación.
- [x] la GUI debe permitir definir duración real de la animación. Es decir, tenemos datos de "x" horas, pero ¿en cuánto tiempo se despliega la animación?
- [ ] Permitir animaciones parciales, es decir que se puedan hacer animaciones con promedios de "x" cantidad de minutos y no unicamente con los datos de cada 2 minutos.
- [ ] Hacer una animación de un proemdio de valores a lo largo del eje Y (una fila) para generar un segundo gráfico en 2D, que muestra la concentración promedio de PM a medida que nos alejamos de la vía, mostrando ejes X y Z.
- [x] la GUI debe permitir definir la cantidad de sensores en eje Y y en eje X.
- [x] la GUI debe permitir definir la distancia entre sensores en eje Y y en eje X.
- [x] la GUI debe permitr declarar de dónde se sacará la información (Internet o MicroSD).
- [x] las gráficas se deben presentar como una gráfica de calor (esto no lo define el usuario, pero nos servirá para identificar concentraciones mayores a los límites permitidos/norma de calidad del aire).
- [x] Despues de ejecutar los scripts de promedio a lo largo del tiempo y espacio se debe generar un archivo de texto que incluya hora de inicio y fin de mediciones y Cantidad de datos tomados por cada sensor, esto para identificar algún error y poder hacer las correcciones necesarias.
- [ ] STDV: sería bueno tomar la desviación estándar (stdv) de cada fila, pues en teoría todos los sensores dentro de una misma fila en Y deberían reportar valores similares.
- [ ] ¿Qué pasa si perdemos datos intermedios en algún sensor?, por ejemplo S1 y S3 tienen 30 datos, pero S2 (en medio de S1 y S3) solo reporta 15. En ese caso, para el sensor S2, podemos tomar un promedio considerando solo los 15 datos o podríamos ajustar los datos faltantes como un promedio entre los valores entregados por S1 y S3.
- [x] la GUI debe permitir definir el tamaño de particula a utilizar.
- [x] la GUI debe permitir definir la ruta a seguir para obtener los datos de la MicroSD
- [ ] Checar si PA conectado a la Micro SD genera un archivo por día, es decir si lo conectamos una vez, y dura 3 días ¿genera 3 archivos?
- [ ] Guardar todos los ids de los 30  sensores para que el programa tenga la info local, y solo te pida el número del sensor que quieres usar.
- [ ] Utilizar los dos canales de cada sensor.
- [ ] Poder ver el # del sensor al pasar el cursor sobre la gráfica.
- [ ] Asignar colores de acuerdo al AQI de la EPA.
- [ ] Agregar a la interfaz la opción de checar lo que monitoreó un sensor en específico (Crear una función basada en *LivePlot.py* que pueda ser integrada a *AvgFunctions.py*).