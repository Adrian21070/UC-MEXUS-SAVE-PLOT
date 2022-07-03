import PySimpleGUI as sg
import plots as Func
import main_gui as gui
import pandas as pd
import sys
import os
import csv
from datetime import datetime, timedelta
from dateutil import tz
from purple_air import *

# Ids y llaves de los sensores

# Canal A primario
id_A_primaria = [1367948, 1367997, 1336916, 1367985, 1369647,
                 1369624, 1379154, 1368013, 1369640, 1367969,
                 1379214, 1367956, 1367952, 1336974, 1368009, 
                 1453911, 1452796, 1451589, 1450382, 1452792,
                 1452813, 1450481, 1447356, 1452808, 1451577,
                 1451621, 1452812, 1452804, 1450358, 1450485]

key_A_primaria  =  ['TMTVNTYUXGGT7MK3','T5VPQSVT9BAE5ZI1','F2K1DV64M1Z75VU4','O94LWPUDGE645M0W','3DHCZRPJ1M6YIFV7',
                    'LMP9I4DYO31RLQCM','4YNO8GQDC5V4D8AH','YR676V09QO1KX1Q7','YTLP8VLPWKIJ9G4K','ODM4VO7RDXCYWL2O',
                    '0S1GMA57I3VO7TN8','IJ44H5T0VGAPOM1X','4MGD149UTH64IKO1','D1EPGDRFWRLFDRWL','3GOKID03X1ZQI7UO',
                    'IO35IQWN7OD7QZRI','KYOJ88GAQ573QZOG','D6NQDA4PSE9FDW9N','KR2E9MGDRAR8U4FI','TV45OPQDRKXEOYF3',
                    'WXQHTF7MVPTGUV3H','HWHD61TYPRC08IJ0','TEQLCBVA8W53X6MQ','LYE31WD6M75Z3J8E','CF8HVDROSC9N04O7',
                    'BCJV79PNCBA20CEI','ITO12LYZ84AXMSB1','LAU5S4Y8NY6F9FNK','9WAVRBGJHR27Q9SB','FP815UH9YRZ77MY1']

# Canal A secundario
id_A_secundario = [ 1367949,1367998,1336917,1367986,1369649,
                    1369625,1379155,1368014,1369641,1367970,
                    1379215,1367957,1367953,1336975,1368010,
                    1453912,1452797,1451590,1450383,1452793,
                    1452815,1450482,1447357,1452809,1451578,
                    1451622,1452814,1452805,1450359,1450486]

key_A_secundario = ['N35ZTFXU25M0A6CA','MCM57TRYAOGJ57VR','BEYTKDKR4C0AMGCM','KLM2U0CL391PP3DG','5NQMLBFPN7W283IL',
                    '3MPDB21FMKGH1P2X','849VV10E7X1ETSOI','ZYABOKBEKNMB5AXY','QSYMW4EO1SOOQFM1','3UZ115LMBL6XM07O',
                    '28TVNV2W36FOP5DE','L0K8TEB4HCLQBVJN','UN8HTPYPZXBLJU2Y','Z2MMXGBGJ04RL76F','2M0Z2C2TK8MQ0IRF',
                    'AHXTLEY2LI3UM00B','01YVXQQNWTHFZJJ7','GKVARQR905CVIB2A','0KL46B1VFIKHBY86','0VG3SG00QAZXM89Y',
                    '5WMHAY9WVZHT2TRC','OCJOC97TIDK38CYQ','CXTXDJMQFSPU3QRZ','W8COUOT2RZ0N6MV1','U82JIM55AAWAQ7EZ',
                    'S8TY9Y9OKXIO6W8O','K0YKDCUCB5XIOSCF','FRKFG5QCECZVBPTP','B60BR8CJJBX28PCV','X5QUOFZHOCI1RRG6']

# Canal B primario
id_B_primaria =    [1367950,1367999,1336918,1367987,1369650,
                    1369626,1379156,1368015,1369642,1367971,
                    1379216,1367958,1367954,1336976,1368011,
                    1453913,1452798,1451591,1450384,1452794,
                    1452816,1450483,1447358,1452810,1451579,
                    1451623,1452817,1452806,1450360,1450487]

key_B_primaria =   ['UJUFOPEW3TOQWV8W','SBE27R7ZJHWLJ0V9','6U1OM87T7HB2SHO6','4P2NPP0DZBQ5H01U','NYKKMFEOO7D4QTNQ',
                    'H23N20TQIQXG9TZ1','87B2JFJ8M2YE28XU','OUAIRU5KUF51GKW7','X2UI2TVHRR6KLNE1','NDWTG00GYY45TIHT',
                    'WCD4MQFA6XHG3898','W8HHP4TYIQSX5KTC','TRE7T06OLPEAQNEU','IDFY2IKBD5YYQ3IC','2QHPEK2LV6XTPCLI',
                    'XVDJ2HO3CPWTCNOE','8QD9X0NLU5LMBGRQ','V38CTGH0KK1NG5H6','6HZR1CKM9A14DYGY','SQXHOCR8Z2TY4IN3',
                    'EJFTAH9141Z9L5CJ','MTMROSCL10MQSF45','F7MVFPZZK6DMD2RB','4XYU9Z7P4R00TM8T','D1K7QCKT439VRTQC',
                    'BPE6OPXW2GB9M43M','HWHFD4R9DUIU7AIC','EE1CBSNYYB9DX795','BLF46BW5G54ELS24','UP85N2L0PR4214CO']

# Canal B secundario
id_B_secundario = [ 1367951,1368000,1336919,1367988,1369651,
                    1369627,1379157,1368016,1369643,1367972,
                    1379217,1367959,1367955,1336977,1368012,
                    1453914,1452799,1451592,1450385,1452795,
                    1452819,1450484,1447359,1452811,1451580,
                    1451624,1452818,1452807,1450361,1450488]

key_B_secundario = ['S26M6JT22KN1VIDK','O45GOHMJ4Q47JAFR','IBA7X29X9UX5JGCQ','75ZV3RKH6E1TIRU3','UG4HPEVRHLUJ2D17',
                    'UYK5CKP6IV5Q4OC5','5TQT1AHKDQKEUYY9','XLMZSET7Q38QE15P','1R2623SZGX30YLVP','E9HPEE0C5A0DCSYD',
                    'WOAFDRUD332VJENJ','1HEF9A8O8S3NKTXL','H0Y3TL1DG2AIOCDO','SYBQNPPD7O9M6J2N','DHMI5UGG4W9O4E5L',
                    'PGLSR0J9Q83WF9VX','5JROZTWYU2AWNJFY','0XNZ6Z41J1K3GBMD','NXONF32TNAPHY3J6','J7NP76EK4EG8KEZI',
                    'DOXG6QXVA1Y9IGUB','BOB1R0Y2SGBTTUOM','0TS9YT52ZNJ0X9P4','I75ZX6FP7MCDSH9O','3QJ0OUMJZ6TFSKFY',
                    'FAKAE3TIIP7EVWJD','GP8N5TST5N9XXTPR','PUN6KC9U1MAOQUPT','MVEKFJNPQ69915ZH','A7SM2BENAMNB8IHI']

IDS_KEY = {}
for ii in range(len(id_A_primaria)):
    IDS_KEY[ii+1] = (id_A_primaria[ii], key_A_primaria[ii], id_A_secundario[ii], key_A_secundario[ii],
                     id_B_primaria[ii], key_B_primaria[ii], id_B_secundario[ii], key_B_secundario[ii])

del id_A_primaria, key_A_primaria
del id_A_secundario, key_A_secundario
del id_B_primaria, key_B_primaria
del id_B_secundario, key_B_secundario

# Diccionario para pasar las columnas de online a un csv estandar.
# Canal A

PA_Onl_A = {"PM1.0 (ATM)": "PM1.0_ATM_ug/m3", "PM2.5 (ATM)": "PM2.5_ATM_ug/m3",
            "PM10.0 (ATM)": "PM10.0_ATM_ug/m3", "Uptime":"UptimeMinutes",
            "RSSI":"RSSI_dbm", "Temperature": "Temperature_F",
            "Humidity":"Humidity_%", "PM2.5 (CF=1)": "PM2.5_CF1_ug/m3",
            "0.3um":">=0.3um/dl", "0.5um":">=0.5um/dl",
            "1.0um":">=1.0um/dl", "2.5um":">=2.5um/dl",
            "5.0um":">=5.0um/dl", "10.0um":">=10.0um/dl",
            "PM1.0 (CF=1)": "PM1.0_CF1_ug/m3","PM10.0 (CF=1)": "PM10.0_CF1_ug/m3"}

# Canal B
PA_Onl_B = {"PM1.0 (ATM)": "PM1.0_ATM_B_ug/m3", "PM2.5 (ATM)": "PM2.5_ATM_B_ug/m3",
            "PM10.0 (ATM)": "PM10.0_ATM_B_ug/m3", "Mem":"UptimeMinutes_B",
            "Adc":"ADC", "Pressure": "Pressure_hpa",
            "PM2.5 (CF=1)": "PM2.5_CF1_B_ug/m3", "Unused":"Unused",
            "0.3um":">=0.3_B_um/dl", "0.5um":">=0.5_B_um/dl",
            "1.0um":">=1.0_B_um/dl", "2.5um":">=2.5_B_um/dl",
            "5.0um":">=5.0_B_um/dl", "10.0um":">=10.0_B_um/dl",
            "PM1.0 (CF=1)": "PM1.0_CF1_B_ug/m3","PM10.0 (CF=1)": "PM10.0_CF1_B_ug/m3"}

CSV_dict = {"UTCDateTime":"created_at",
            "pm1_0_atm":"PM1.0_ATM_ug/m3",
            "pm2_5_atm":"PM2.5_ATM_ug/m3", 
            "pm10_0_atm":"PM10.0_ATM_ug/m3",
            "uptime":"UptimeMinutes", 
            "rssi":"RSSI_dbm",
            "current_temp_f":"Temperature_F", 
            "current_humidity":"Humidity_%",
            "pm1_0_cf_1":"PM1.0_CF1_ug/m3", 
            "pm2_5_cf_1":"PM2.5_CF1_ug/m3",
            "pm10_0_cf_1":"PM10.0_CF1_ug/m3", 
            "p_0_3_um":">=0.3um/dl", "p_0_5_um":">=0.5um/dl", 
            "p_1_0_um":">=1.0um/dl", "p_2_5_um":">=2.5um/dl", 
            "p_5_0_um":">=5.0um/dl", "p_10_0_um":">=10.0um/dl",
            "pm1_0_atm_b":"PM1.0_ATM_B_ug/m3",
            "pm2_5_atm_b":"PM2.5_ATM_B_ug/m3", 
            "pm10_0_atm_b":"PM10.0_ATM_B_ug/m3",
            "mem":"UptimeMinutes_B", "adc":"ADC", 
            "pressure":"Pressure_hpa",
            "pm1_0_cf_1_b":"PM1.0_CF1_B_ug/m3", 
            "pm2_5_cf_1_b":"PM2.5_CF1_B_ug/m3",
            "pm10_0_cf_1_b":"PM10.0_CF1_B_ug/m3", 
            "p_0_3_um_b":">=0.3_B_um/dl", "p_0_5_um_b":">=0.5_B_um/dl", 
            "p_1_0_um_b":">=1.0_B_um/dl", "p_2_5_um_b":">=2.5_B_um/dl", 
            "p_5_0_um_b":">=5.0_B_um/dl", "p_10_0_um_b":">=10.0_B_um/dl"}

# Fuentes para la interfaz
font = ('Times New Roman', 14)
font2 = ('Times New Roman', 12)
font3 = ('Times New Roman', 18)

def sensor_info(window):
    # Primero solicita el número de sensores a guardar e intervalo de tiempo
    # de la medición.
    layout = [[sg.Text('Datos acerca del número de sensores y el intervalo de medición\n', font=font3)],
                [sg.Text('Favor de introducir el dia y hora en formato UTC.', font=font)],
                [sg.CalendarButton('Dia de inicio de la medición',target='Start', size=(25,1), format='20%y-%m-%d',font=font2), sg.Input(key='Start')],
                [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText('00:00',key='Start_hour')],
                [sg.CalendarButton('Dia del fin de la medición',target='End', size=(25,1), format='20%y-%m-%d',font=font2), sg.Input(key='End')],
                [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText('23:59',key='End_hour')],
                [sg.Text('')],
                [sg.Text('Introduce la tolerancia en minutos de datos perdidos (>2).'), sg.Input(5, key='holes_size', size=(10,1))],
                [sg.Text('')],
                [sg.Text('Nota: El programa tiene registrado las llaves y ids de 30 sensores,\nsi desea trabajar con más sensores, favor de seleccionar el recuadro:')],
                [sg.Checkbox('Cargar llaves y Ids', default=False, key='Cargar')],
                [sg.Button('Continue'), sg.Button('Return'), sg.Button('Exit')]]
    
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()
    
    if 'Exit' in event:
        shutdown(window)

    elif 'Return' in event:
        event = 'init'

    try:
        float(value['holes_size'])
    except:
        layout = [[sg.Text('Favor de introducir un número en la tolerancia', justification='center', font=('Times New Roman', 20))],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()

        return window, event, value, True
    
    if (not value['Start']) or (not value['End']) or (not value['Start_hour']) or (not value['End_hour']):
        layout = [[sg.Text('Favor de no dejar los espacios en blanco', justification='center', font=('Times New Roman', 20))],
            [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        return window, event, value, True
    
    start = value['Start'] + ' ' + value['Start_hour']
    end = value['End'] + ' ' + value['End_hour']

    try:
        start = datetime.strptime(start, '%Y-%m-%d %H:%M').replace(tzinfo=tz.tzutc())
        end = datetime.strptime(end, '%Y-%m-%d %H:%M').replace(tzinfo=tz.tzutc())
    except:
        layout = [[sg.Text('Favor de introducir de manera correcta las horas (hh:mm)', justification='center', font=('Times New Roman', 20))],
            [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        return window, event, value, True

    delta = end - start
    delta = delta.days*24*60*60 + delta.seconds

    if delta < 120:
        layout = [[sg.Text('La fecha de inicio debe ser por lo menos dos minutos menor a la final', justification='center', font=font3)],
            [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        return window, event, value, True

    return window, event, value, False
        
def Cargar(window):
    """
        @name: Cargar
        @brief: Se ejecuta si el usuario desea comprobar sensores nuevos que no estan añadidos en este código.
        @params: window
        @return: Actualiza la variable global de IDs y Keys.
    """

    layout = [[sg.Text('Carga de archivo csv\n', justification='center', font=('Times New Roman', 20), expand_x=True)],
                [sg.Text('Selecciona el archivo con los Ids y llaves de los sensores a trabajar')],
                [sg.Input(), sg.FileBrowse()],
                [sg.Button('Continue', key='Continue'), sg.Button('Return', key='sensor_info'), sg.Button('Exit')]]
        
    window.close()
    window = sg.Window('Monitoreo de los sensores', layout, font=font, size=(720,480), grab_anywhere=True)
    event, value = window.read()
    if event in ('Exit', sg.WIN_CLOSED):
        window.close()
        sys.exit()
    elif event == 'sensor_info':
        return False, window, event

    try:
        with open(value['Browse'], mode='rt', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            global IDS_KEY
            IDS_KEY = {}
            linea = 0
            for row in csv_reader:
                if linea == 0:
                    linea = 1
                    continue
                IDS_KEY[int(row[0])] = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        
        return False, window, event

    except:
        layout = [[sg.Text('Favor de cargar un archivo tipo CSV que contenga:', justification='center', font=('Times New Roman', 20))],
                [sg.Text('No, Ids_A, Keys_A, Ids_A_sec, keys_A_sec, Ids_B,..., keys_B_sec como columnas.', font=font2)],
                [sg.Button('Return'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()

        return True, window, event

def sensors_in_field(window):
    # Ahora, solicito los numeros de los sensores en campo.
    
    chain = list(IDS_KEY.keys())
    lay = []
    layout = []
    
    r = 0
    c = 0
    jj = 0
    for ii in chain:
        if jj%10 == 0:
            r += 1
            c = 0
            layout.append(lay)
            lay = []
        lay.append(sg.Input(ii,key=f'{r},{c}', size=(5,1)))
        c += 1
        jj += 1
    if lay:
        layout.append(lay)
        lay = []

    frame = [[sg.Frame('Sensores a descargar', layout, element_justification='center', expand_x=True)]]

    lay = [[sg.Text('Favor de indicar los sensores a descargar\n', justification='center', font=('Times New Roman', 20), expand_x=True)],
            [sg.Text('Escribe el número de identificación de los sensores en los recuadros (Ejemplo: 1, 6, 23).')],
            [sg.Text('En el recuadro se despliegan todos los sensores, si no requiere')],
            [sg.Text('alguno de ellos, deje en blanco su recuadro.')],
            [sg.Column(frame, scrollable=True, expand_y=True, justification='center')],
            [sg.Button('Continue',key='Next'), sg.Button('Return', key='sensor_info'), sg.Button('Exit')]]
    
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', lay, font=font, size=(720,480), grab_anywhere=True)
    #window = sg.Window('Proyecto UC-MEXUS', [[sg.Column(lay, element_justification='center')]], font=font2, size=(720,480), grab_anywhere=True)
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    elif 'sensor_info' in event:
        sensors = []
        return sensors, window, event

    # Extraigo los valores dados por el usuario y quito los repetidos.
    value = list(set(list(value.values())))

    # Quito los espacios vacios.
    if '' in value:
        value.remove('')
    
    # Hago una prueba para evitar que el usuario rompa el código.
    try:
        # Los paso de string a enteros y ordeno.
        sensors = value
        for jj in range(len(sensors)):
            num = int(sensors[jj])
            if num > 99:
                continue
            elif num >= 10 and num <= 99:
                sensors[jj] = f'0{sensors[jj]}'
            else:
                sensors[jj] = f'00{sensors[jj]}'

        sensors.sort()

        # Compruebo que los numeros esten dentro de los numeros dados por el usuario o del 1 a 30.
        num = list(IDS_KEY.keys())
        llave = False

        for ii in sensors:
            if int(ii) in num:
                pass

            else:
                llave = True
                # Si no se encuentra en el rango, se levanta un error y se pide ingresar de nuevo los datos.
                layout = [[sg.Text('Favor de introducir únicamente números enteros que estén')],
                [sg.Text('entre el 1 y 30, o entre los números del archivo csv cargado.')],
                [sg.Button('Try again'), sg.Button('Exit')]]
                window.close()
                window = sg.Window('Proyecto UC-MEXUS', layout, font=('Times New Roman', 18), size=(720,480), grab_anywhere=True)
                event, value = window.read()
                if event in ('Exit', sg.WIN_CLOSED):
                    window.close()
                    sys.exit()
                break

        if llave:
            return True, window, event
        else:
            return sensors, window, event

    except:
        layout = [[sg.Text('Favor de introducir únicamente números enteros que estén')],
                [sg.Text('entre 1 y 30, o entre los números del archivo csv cargado.')],
                [sg.Button('Try again'), sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=('Times New Roman', 18), size=(720,480), grab_anywhere=True)
        event, value = window.read()
        if event in ('Exit', sg.WIN_CLOSED):
            window.close()
            sys.exit()
        
        return True, window, event

def total_extraction(indx, start, end, window):
    # Se extraera la data del canal A y B primario y secundario.
    # Diccionario de df

    try:
        total_data = {}
        for ii in indx:
            df = pd.DataFrame()

            # No de sensor
            ii = int(ii)

            ids = []
            keys = []

            # A primario
            ids.append(IDS_KEY[ii][0])
            keys.append(IDS_KEY[ii][1])

            # A secundario
            ids.append(IDS_KEY[ii][2])
            keys.append(IDS_KEY[ii][3])

            # B primario
            ids.append(IDS_KEY[ii][4])
            keys.append(IDS_KEY[ii][5])

            # B secundario
            ids.append(IDS_KEY[ii][6])
            keys.append(IDS_KEY[ii][7])

            for jj in range(4):
                # Creo la conexión
                TSobject = Thingspeak(read_api_key=keys[jj], channel_id=ids[jj])
                # Extraigo los datos
                data,c = TSobject.read_one_sensor(start=start, end=end)
                # Lo conviero a dataframe
                df_aux = pd.DataFrame(data)
                # Quito la columna entry_id
                df_aux = df_aux.drop(['entry_id'], axis=1)

                # Elimino la fila created_at de los otros canales (es redundante)
                if jj > 0:
                    df_aux = df_aux.drop(['created_at'], axis=1)

                # Renombro las columnas.
                rename = {}
                if jj < 2:
                    for kk in range(8):
                        name = 'field'+str(kk+1)
                        rename.update({name:PA_Onl_A[c[name]]})
                    df_aux.rename(columns=rename, inplace=True)

                else:
                    for kk in range(8):
                        name = 'field'+str(kk+1)
                        rename.update({name:PA_Onl_B[c[name]]})
                    df_aux.rename(columns=rename, inplace=True)

                    if jj == 2:
                        df_aux = df_aux.drop(['Unused'], axis=1)

                # Uno los dataframes
                df = pd.concat([df, df_aux], axis=1)

            # Elimino los nan
            df = df[df['created_at'].notna()]

            # Cambio el formato en que aparece la fecha.
            date = df['created_at']
            time = []
            for jj in range(len(date)):
                temp = date[jj].strip('Z').replace('T', ' ')
                # Transformo de string a datetime local
                # Posteriormente en el proceso final se hara UTC
                time_utc = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.tzutc())
                time_utc = time_utc.astimezone(tz.tzlocal())
                time.append(time_utc)
            df['created_at'] = time

            if ii >= 100:
                num = ii
            elif ii >= 10 and ii < 100:
                num = f'0{ii}'
            else:
                num = f'00{ii}'

            total_data[f'Sensor {num}'] = df

        return total_data, window
    
    except:
        layout = [[sg.Text('¡Error fatal al intentar leer los datos de un sensor!', font=('Times New Roman',18))],
                [sg.Text(f'El error ocurrió al extraer datos del sensor {ii}.')],
                [sg.Text('Errores posibles:')],
                [sg.Text('1.- Se introdujo mal alguna Id o llave en el archivo csv.')],
                [sg.Text('2.- Mala conexión de internet.')],
                [sg.Text('3.- Problemas con el servidor de PurpleAir.')],
                [sg.Text(f'El programa finalizará después de esta ventana...')],
                [sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        sg.popup_auto_close('Cerrando programa...', font=('Times New Roman',16))
        shutdown(window)

def holes_verification(window, data, indx, holes_size):
    try:
        sizes = {}
        num_holes_per_sensor = {}
        for ii in indx:
            sensor = data[f'Sensor {ii}']
            time = sensor['created_at']

            sizes[f'Sensor {ii}'] = {}
            temp = 0

            for jj in range(len(time)-1):
                delta = time[jj+1] - time[jj]
                delta = delta.days*24*60*60 + delta.seconds
                if delta > float(holes_size)*60: #Modificable por usuario???
                    day = (time[jj]).day
                    day2 = (time[jj+1]).day
                    # Existe un hueco
                    # sizes tiene como llave el inicio del hueco y como value el final.
                    sizes[f'Sensor {ii}'].update({time[jj]:time[jj+1]})


                    if temp == 0:
                        temp += 1
                        num_holes_per_sensor[f'Sensor {ii}'] = temp
                        day3 = day
                        day4 = day2
                    else:
                        if day != day3 or day2 != day4:
                            temp += 1
                            num_holes_per_sensor[f'Sensor {ii}'] = temp
                            day3 = day
                            day4 = day2
        
    except:
        layout = [[sg.Text('¡Error fatal al intentar comprobar los huecos de un sensor!', font=('Times New Roman',18))],
                [sg.Text(f'El error ocurrió al verificar los huecos de inforamción del sensor {ii}.')],
                [sg.Text(f'El programa finalizará después de esta ventana...')],
                [sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        sg.popup_auto_close('Cerrando programa...', font=('Times New Roman',16))
        shutdown(window)

    try:
        # Si existen huecos, se notifica.
        if num_holes_per_sensor:
            window, event = gui.holes_warning(window,sizes,num_holes_per_sensor)
            return window, event, sizes, num_holes_per_sensor

        event = ''
        return window, event, sizes, num_holes_per_sensor
    except:
        layout = [[sg.Text('¡Error fatal al intentar notificar los huecos de un sensor!', font=('Times New Roman',18))],
                [sg.Text(f'El programa finalizará después de esta ventana...')],
                [sg.Button('Exit')]]
        window.close()
        window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
        event, value = window.read()
        sg.popup_auto_close('Cerrando programa...', font=('Times New Roman',16))
        shutdown(window)
    
def fix_save(window, num_csv_per_sensor, holes, data):
    # Solicito archivos csv
    window, value = gui.csv_online2(window, num_csv_per_sensor, holes)

    # Arreglo los huecos
    csv_data, window, key = csv_extraction(value, window, key=1)
    if key:
        return window, csv_data, True

    data = Fix_data(data, csv_data, 0, holes, key='CSV')
    for ii in data.keys():
        df = data[ii]
        df = df.reindex(columns=list(CSV_dict.values()))
        data[ii] = df
    
    return window, data, False

def csv_extraction(dir, window, key=0):
    """
        Si key = 1, dara un dataframe con la fecha en formato datetime,
        si no se da el parametros key, otorgara la fecha en string.

        Regresa un diccionario de dataframes, 1 por cada archivo que se le de.
    """
    from_zone = tz.tzutc()

    col_name = list(CSV_dict.keys())
    new_col_name = list(CSV_dict.values())
    data_frames = {}

    for ii in dir:
        df = pd.DataFrame()
        for jj in dir[ii]: # Lee todos los archivos del sensor XX, ya que puede tener mas de 1
            # Ahora, solo nos quedaremos con los mismos datos que otorga el online
            try:
                df2 = pd.read_csv(jj)
                df2 = df2[col_name]
                # Cambiamos los nombres de las columnas.
                df2.columns = new_col_name

                # Arreglamos las fechas para hacerlas más sencillas de tratar.
                date = list(df2['created_at'])

                # Comprobamos que no este vacio el csv
                if date:
                    pass
                else:
                    raise ValueError("CSV vacio")

                date_new = []
                
            except:
                layout = [[sg.Text('¡Error fatal al intentar leer el archivo csv de un sensor!', font=('Times New Roman',18))],
                        [sg.Text(f'El error ocurrió al leer el archivo del sensor {ii},')],
                        [sg.Text(f'con dirección: {jj}')]
                        [sg.Text('Asegurate de introducir el archivo correcto.')]
                        [sg.Button('Try again'), sg.Button('Exit')]]
                window.close()
                window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
                event, value = window.read()
                if event in ('Exit', sg.WIN_CLOSED):
                    window.close()
                    sys.exit()
                return 0, window, True

            try:
                if key == 1:
                    for temp in date:
                        temp = temp.replace('/','-')
                        temp = temp.replace('T',' ')
                        temp = temp.strip('z')
                        early = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)
                        if early.second >= 30:
                            early = early + timedelta(seconds=60-early.second)
                        else:
                            early = datetime(early.year, early.month, early.day, early.hour, early.minute, 0, tzinfo=from_zone)

                        date_new.append(early)
                else: #Quiza esto en otra funcion separada, no le veo utilidad aqui.
                    for temp in date:
                        temp = temp.replace('/','-')
                        temp = temp.replace('T',' ')
                        temp = temp.replace('z',' UTC')
                        date_new.append(temp)
            except:
                layout = [[sg.Text('¡Error fatal al tratar con las fechas del archivo csv de un sensor!', font=('Times New Roman',18))],
                        [sg.Text(f'El error ocurrió al leer el archivo del sensor {ii},')],
                        [sg.Text(f'con dirección: {jj}')]
                        [sg.Text('Asegurate de introducir el archivo correcto.')]
                        [sg.Button('Try again'), sg.Button('Exit')]]
                window.close()
                window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480), grab_anywhere=True)
                event, value = window.read()
                if event in ('Exit', sg.WIN_CLOSED):
                    window.close()
                    sys.exit()
                return 0, window, True
        
            date = [] #Limpio la variable

            df2['created_at'] = date_new #Asigno mi fecha corregida

            # Unimos
            df = pd.concat([df, df2])

        # Sort the data
        df = df.sort_values(by=['created_at'])

        # Reset the index
        df.reset_index(inplace=True, drop=True)

        # Ahora solo queda almacenar el dataframe en el diccionario
        data_frames[ii] = df
        
    return data_frames, window, False

def Fix_data(data_online, csv_data, PMType, holes, key):
    # Como un sensor puede presentar diversos huecos, debemos usar todos los csv designados a dicho sensor
    # este pedazo de codigo solo ordenara los csv acorde a su sensor.

    for ii in data_online.keys():
        val = data_online[ii]['created_at']
        val = Func.conversor_datetime_string(val, key=2) #Convierto a utc
        data_online[ii]['created_at'] = val
    df_online = data_online

    # Una vez con toda la data de online y csv puesta en dataframes
    # Se realizara el rellenado de los huecos.

    # Solo se realizara en los sensores que tengan huecos, no en todos.
    for ii in csv_data.keys():
        df = df_online[ii]
        
        df_c = csv_data[ii]
        sensor_holes = holes[ii]

        for kk in sensor_holes.keys():
            start = Func.conversor_datetime_string([kk, sensor_holes[kk]], key=2) 
            init = start[0]
            end = start[1]

            date = df_c['created_at'] 

            # Encuentra en csv, donde esta init y end.
            row = df_c.index[(((date-init) < timedelta(seconds=120)) & ((init-date) < timedelta(seconds=120)))].tolist()

            row_end = df_c.index[(((date-end) < timedelta(seconds=120)) & ((end-date) < timedelta(seconds=120)))].tolist()

            # Seleccionar el trozo de información entre row y row_end, no se incluyen
            chunk = df_c.loc[row[-1]+1:row_end[0]-1]

            # Unimos
            df = pd.concat([df, chunk])

            # Sort the data
            df = df.sort_values(by=['created_at'])

            # Reset the index
            df.reset_index(inplace=True, drop=True)

        # Se actualizan los datos de online ya corregidos.
        df_online[ii] = df

    return df_online

def save(window, data, indx, start, end):
    layout = [[sg.Text('¿Donde desea guardar los datos?', font=font3, justification='center', expand_x=True)],
            [sg.Text('',size=(1,1), font=('Times New Roman',1))],
            [sg.Text(f'Ubicación de creación de carpeta: ',size=(28,1)), sg.Input(size=(30,1)), sg.FolderBrowse()],
            [sg.Text('Nombre de la carpeta a crear: ', size=(28,1)), sg.InputText('Data',size=(30,1), key='FolderName')],
            [sg.Text('',size=(1,1), font=('Times New Roman',1))],
            [sg.Button('Guardar'), sg.Button('Exit')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480))
    event, value = window.read()

    if 'Exit' in event:
        shutdown(window)
    
    parent_id = value['Browse']
    dir = value['FolderName']

    # Ubicación principal
    path = os.path.join(parent_id, dir)

    kk = 0
    while True:
        if not os.path.exists(path):
            os.makedirs(path, exists_ok=True)
            break
        else:
            kk += 1
            path = os.path.join(parent_id, dir+f'_v{kk}')

    start = datetime.strptime(start, '%Y-%m-%d').replace(tzinfo=tz.tzutc())
    end = datetime.strptime(end, '%Y-%m-%d').replace(tzinfo=tz.tzutc())

    for jj in range(end.day-start.day + 1):

        path_new = os.path.join(path, start.strftime("%Y_%m_%d"))

        # Verifico si no existen los directorios.
        if not os.path.exists(path_new):
            os.makedirs(path_new, exist_ok=True)

        for ii in indx:
            # Crea todos los archivos csv con los nombres de ii.
            df = data[f'Sensor {ii}']
            date = df['created_at']
            end_day = datetime(start.year, start.month, start.day+1).replace(tzinfo=tz.tzutc())
            row = df.index[((date >= start) & (date < end_day))].tolist()

            # Compruebo que si existan datos en ese dia.
            if row:
                chunk = df.loc[row[0]:row[-1]]

                # Convierto created_at a string
                chunk['created_at'] = Func.conversor_datetime_string(chunk['created_at'], key=3)

                fecha = start.strftime("%Y_%m_%d")
                dir = f'S{ii}_' + fecha

                # Dirección del csv del sensor x
                csv_path = os.path.join(path_new,dir)

                kk = 0
                while True:
                    if not os.path.exists(csv_path):
                        chunk.to_csv(csv_path+'.csv', index=False)
                        break
                    else:
                        kk += 1
                        csv_path = os.path.join(path_new,dir+f'_v{kk}')

            else:
                continue

        start = start + timedelta(days=1)
    
    layout = [[sg.Text('Se termino de almacenar la información.', font=font3)],
            [sg.Button('Graficar'), sg.Button('Realizar otro guardado', key='sensor_info'), sg.Button('Finalizar')]]

    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font=font, size=(720,480))
    event, value = window.read()

    return window, event

def shutdown(window):
    window.close()
    sys.exit()