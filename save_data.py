import PySimpleGUI as sg
import functions as Func
import pandas as pd
from datetime import datetime
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

# Diccionario para pasar las columnas de online a un csv estandar.
PA_Onl_A = {'PM '}

PA_Onl_B = {}

PA_Onl = {"PM 1.0 ATM": "PM1.0_ATM_ug/m3", "PM 2.5 ATM": "PM2.5_ATM_ug/m3",
        "PM 10.0 ATM": "PM10.0_ATM_ug/m3", "PM 1.0 CF": "PM1.0_CF1_ug/m3",
        "PM 2.5 CF": "PM2.5_CF1_ug/m3", "PM 10.0 CF": "PM10.0_CF1_ug/m3",
        "PM 1.0 ATM B": "PM1.0_ATM_B_ug/m3", "PM 2.5 ATM B": "PM2.5_ATM_B_ug/m3",
        "PM 10.0 ATM B": "PM10.0_ATM_B_ug/m3", "PM 1.0 CF B": "PM1.0_CF1_B_ug/m3",
        "PM 2.5 CF B": "PM2.5_CF1_B_ug/m3", "PM 10.0 CF B": "PM10.0_CF1_B_ug/m3"}

# Fuentes para la interfaz
font = ('Times New Roman', 16)
font2 = ('Times New Roman', 12)

def sensor_info(window):
    # Primero solicita el número de sensores a guardar e intervalo de tiempo
    # de la medición.
    layout = [[sg.Text('Datos acerca del número de sensores y el intervalo de medición')],
                [sg.Text('Numero de sensores:'), sg.Input(key='NumSen')],
                [sg.CalendarButton('Dia de inicio de la medición',target='Start', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='Start')],
                [sg.Text('Hora de inicio (hh:mm)', size=(25,1)), sg.InputText(key='Start_hour')],
                [sg.CalendarButton('Dia del fin de la medición',target='End', size=(24,1), format='20%y-%m-%d',font=font2), sg.Input(key='End')],
                [sg.Text('Hora de finalización (hh:mm)', size=(25,1)), sg.InputText(key='End_hour')],
                [sg.Button('Continue'), sg.Button('Return'), sg.Button('Exit')]]
    
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', layout, font = font2, size=(720,480))
    event, value = window.read()
    
    if 'Exit' in event:
        shutdown()

    elif 'Return' in event:
        event = 'init'
        return window, event, value

    numsen = int(value['NumSen'])
    start = value['Start'] + '%20' + value['Start_hour'] + ':00'
    end = value['End'] + '%20' + value['End_hour'] + ':00'

    return window, event, value

def sensors_in_field(window, numsen):
    # Ahora, solicito los numeros de los sensores en campo.
    
    chain = list(range(1,numsen+1))
    lay = []
    layout = []
    
    r = 0
    c = 0
    for ii in chain:
        if ii%9 == 0:
            r += 1
            c = 0
            layout.append(lay)
            lay = []
        lay.append(sg.Input(ii,key=f'{r},{c}', size=(5,1)))
        c += 1
    if lay:
        layout.append(lay)
        lay = []
    lay = [[sg.Text('Carretera', font=('Times New Roman', 24), justification='center', expand_x=True)],
            [sg.Frame('Disposición de los sensores', layout)],
            [sg.Button('Continue',key='Next'),sg.Button('Return',key='Init'),sg.Button('Exit')]]
    window.close()
    window = sg.Window('Proyecto UC-MEXUS', lay, font = font2, size=(720,480))
    event, indx = window.read()

    return window, event, indx

def total_extraction(indx, start, end):
    # Se extraera la data del canal A y B primario y secundario.
    # Diccionario de df
    total_data = {}
    for ii in indx.values():
        df = pd.DataFrame()

        ii = int(ii)
        ids = []
        keys = []
        # A primario
        ids.append(id_A_primaria[ii-1])
        keys.append(key_A_primaria[ii-1])
        id_A = id_A_primaria[ii-1]
        key_A = key_A_primaria[ii-1]
        # A secundario
        ids.append(id_A_secundario[ii-1])
        keys.append(key_A_secundario[ii-1])
        id_A_sec = id_A_secundario[ii-1]
        key_A_sec = key_A_secundario[ii-1]
        # B primario
        ids.append(id_B_primaria[ii-1])
        keys.append(key_B_primaria[ii-1])
        id_B = id_B_primaria[ii-1]
        key_B = key_B_primaria[ii-1]
        # B secundario
        ids.append(id_B_secundario[ii-1])
        keys.append(key_B_secundario[ii-1])
        id_B_sec = id_B_secundario[ii-1]
        key_B_sec = key_B_secundario[ii-1]

        for jj in range(4):
            TSobject = Thingspeak(read_api_key=keys[jj], channel_id=ids[jj])
            data,c = TSobject.read_one_sensor(start=start, end=end)
            df_aux = pd.DataFrame(data)
            df_aux = df_aux.drop(['entry_id'], axis=1)
            if jj > 0:
                df_aux = df_aux.drop(['created_at'], axis=1)

            rename = {}
            for kk in range(8):
                name = 'field'+str(kk+1)
                rename.update({name:c[name]})
            df_aux.rename(columns=rename, inplace=True)

            df = pd.concat([df, df_aux], axis=1)

def shutdown(window):
    window.close()
    sys.exit()