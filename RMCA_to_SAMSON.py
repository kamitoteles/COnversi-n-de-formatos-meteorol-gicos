###  CONVERSION DE FORMATO DE ARCHIVOS DE METEOROLOGIA RMCAB 2020 A SAMSON
### Autor: Camilo Moreno - cama9709@gmail.com

#// Importacion de librerias ////////////////////////////////////////////////////////////////////#
import pandas as pd             # Version 1.1.0 
import numpy as np              # Version 1.19.1
import os
import fileinput

#// Variables de estacion a cambiar /////////////////////////////////////////////////////////////#
# !!!! IMPORTANTE: Se asume que se utilizara informacion de la estacion Kennedy de la RMCAB.
#                  En caso de utilizar otra estacion, se debe cambiar las variables de 
#                  station_code, station_ name y station_location para que coincidan con la
#                  estacion requerida.#
#////////////////////////////////////////////////////////////////////////////////////////////////#
station_code = '44444'
station_name = 'KENNEDY'
station_location = 'CO -5  N 4 39  W 74 5' # COUNTRY_CODE UTZ_TIME N NORTH_COORD W WEST_COORD .. LATLON COORDS

var_dic = {

    '01': {'desc':'Extraterrestrial horizontal radiation'  , 'nan':'9999'},
    '02': {'desc':'Extraterrestial direct normal radiation', 'nan':'9999'},
    '03': {'desc':'Global horizontal radiation'            , 'RMCA_name':'Rad Solar', 'nan':'9999', 'extra':' ?0'},
    '04': {'desc':'Direct normal radiation'                , 'nan':'9999', 'extra':' ?0'},
    '05': {'desc':'Diffuse horizontal radiation'           , 'nan':'9999', 'extra':' ?0'},
    '06': {'desc':'Total cloud cover'                      , 'nan':' 5'},
    '07': {'desc':'Opaque cloud cover'                     , 'nan':' 5'},
    '08': {'desc':'Dry bulb temperature'                   , 'RMCA_name':'Temperatura', 'nan':'9999.'},
    '09': {'desc':'Dew point temperature'                  , 'nan':'9999.'},
    '10': {'desc':'Relative humidity'                      , 'RMCA_name':'HR', 'nan':'999'},
    '11': {'desc':'Station pressure'                       , 'RMCA_name':'Presion Baro', 'nan':'9999'},
    '12': {'desc':'Wind direction'                         , 'RMCA_name':'Dir Viento', 'nan':'999'},
    '13': {'desc':'Wind speed'                             , 'RMCA_name':'Vel Viento', 'nan':'9999.'},
    '14': {'desc':'Visibility'                             , 'nan':'99999.'},
    '15': {'desc':'Ceiling height'                         , 'nan':'999999'},
    '16': {'desc':'Present weather'                        , 'nan':'999999999'},
    '17': {'desc':'Precipitable water'                     , 'RMCA_name':'Precipitacion', 'nan':'9999'},
    '18': {'desc':'Broadband aerosol optical depth'        , 'nan':'99999.'},
    '19': {'desc':'Snow depth'                             , 'nan':'9999'},
    '20': {'desc':'Days since last snowfall'               , 'nan':'999'},
    '21': {'desc':'Hourly precipitation amount and flag'   , 'nan':' ' * 7},
}
#// Ingreso de direccion de archivo de meteorologia formato RMCAB 2020 //////////////////////////#
dir_meteorologia = ''
is_file = False
while len(dir_meteorologia) < 1 or not is_file:
    dir_meteorologia = input('\nIngrese la direccion del archivo excel de la RMCAB: ')
    
    if os.path.isfile(dir_meteorologia):
        is_file = True 
    else: 
         print('\n!!!ERROR: El archivo indicado no se encuentra')
    
#// Ingreso de nombre y direccion de destino del archivo de meteorologia formato SAMSON//////////#
name_samson = ''
while len(name_samson) < 1:
    name_samson = input('\nElija el NOMBRE del archivo SAMSON: ')
    
    if name_samson[-4:] != '.SAM':
        print('\n!!!ERROR: La extension del nombre del archivo debe finalizar en ".SAM"')
        name_samson = ''
        
dir_samson = ''
is_dir = False
while len(dir_samson) < 1 or not is_dir:
    dir_samson = input('\nIngrese la DIRECCION DE GUARDADO del archivo convertido: ')
    
    if os.path.isdir(dir_samson):
        is_dir = True
    else: 
         print('\n!!!ERROR: El directorio no existe')

print('\nEspere...')

#// Lectura de archivo de meteorologia formato RMCAB 2020 ///////////////////////////////////////#    
archivo_meteorologia = pd.read_excel(dir_meteorologia,
                                     dtype = str, skiprows = [0, 1, 2, 4],
                                     skipfooter = 11, na_values = '----',
                                     )

#// Reasignacion de nombre de variables meteorlogicas segun formato SAMSON //////////////////////# 
headers = [*archivo_meteorologia]
for i in range(len(headers)):
    
    if headers[i] == 'Unnamed: 0':      headers[i] = '00'
    elif headers[i] == 'Rad Solar':     headers[i] = '03'
    elif headers[i] == 'Temperatura':   headers[i] = '08'
    elif headers[i] == 'HR':            headers[i] = '10'
    elif headers[i] == 'Presion Baro':  headers[i] = '11'
    elif headers[i] == 'Dir Viento':    headers[i] = '12'
    elif headers[i] == 'Vel Viento':    headers[i] = '13'
    elif headers[i] == 'Precipitacion': headers[i] = '17'
    else: headers[i] = 'No'

archivo_meteorologia.columns = headers
del archivo_meteorologia['No']

#// Funcion de actualizacion de espacios en blanco de los valores ///////////////////////////////#
def actualizar_espacios(i):
    
    num_rows = len(archivo_meteorologia['00'])
    
    for columna in list(var_dic):
        
        nada = var_dic[columna]['nan']
            
        try:
            extra = var_dic[columna]['extra'] 
        except:
            extra = ''
        
        if columna in archivo_meteorologia.columns:
            
            if pd.isna(archivo_meteorologia[columna][i]):
                archivo_meteorologia[columna][i] = nada + extra
                
            else:
                temporary = archivo_meteorologia[columna][i]
                space = len(nada) - len(temporary)
                archivo_meteorologia[columna][i] = ' ' * space + temporary + extra
        
        elif i == num_rows-1: 
            archivo_meteorologia[columna] = nada + extra
            

#// Conversion de formato de valores ////////////////////////////////////////////////////////////#
year = []; month = []; day = []; hour = []

for i in range(len(archivo_meteorologia['00'])):
    
    year.append(archivo_meteorologia['00'][i][8:10])
    
    if archivo_meteorologia['00'][i][3] == '0':
        month.append(' ' + archivo_meteorologia['00'][i][4])
    else:
        month.append(archivo_meteorologia['00'][i][3:5])

    if archivo_meteorologia['00'][i][0] == '0':
        day.append(' ' + archivo_meteorologia['00'][i][1])
    else:     
        day.append(archivo_meteorologia['00'][i][0:2])
        
    if archivo_meteorologia['00'][i][11] == '0':
        hour.append(' ' + archivo_meteorologia['00'][i][12])
    else:
        hour.append(archivo_meteorologia['00'][i][11:13])
    
    actualizar_espacios(i)

headers = [*archivo_meteorologia]
archivo_meteorologia.columns = headers
headers.sort()
archivo_meteorologia = archivo_meteorologia[headers]

archivo_meteorologia['YR'] = list(year)
archivo_meteorologia['MO'] = list(month)
archivo_meteorologia['DA'] = list(day)
archivo_meteorologia['HR'] = list(hour)
archivo_meteorologia['I'] = '0'

new_headers = ['YR', 'MO', 'DA', 'HR', 'I'] + headers
archivo_meteorologia = archivo_meteorologia[new_headers]
del archivo_meteorologia['00']

#// Creacion de archivo SAMSON ///////////////////////////////////////////////////////////////////#
np.savetxt('tepm_' + name_samson, archivo_meteorologia.values, fmt = ' %s', delimiter = '')

title = f'~{station_code} {station_name}           {station_location}\n~YR MO DA HR I    1    2       3       4       5  6  7     8     9  10   11  12    13     14     15        16   17     18   19  20      21\n'
f= open('title.txt','w+')
f.write(title)
f.close()

file_list = [ 'title.txt',  'tepm_' + name_samson]

with open(dir_samson + '/' + name_samson, 'w') as file:
    input_lines = fileinput.input(file_list)
    file.writelines(input_lines)
    
os.remove('title.txt')
os.remove('tepm_' + name_samson)


#// Resumen de las direcciones de guardado ///////////////////////////////////////////////////////#
print(f'\n====================================')
print(f'==CONVERSION DE FORMATOS COMPLETA!==')
print(f'====================================')
print(f'Archivo RMCAB: {dir_meteorologia}')
print(f'Archivo SAMSON: {dir_samson + "/" + name_samson}')

