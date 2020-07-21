### Libreria de funciones de conversión de archivos
### Autor: Camilo Moreno - cama9709@gmail.com
#######################################################################################################
#// Importacion de librerias
import pandas as pd             # Version 1.0.5
import numpy as np              # Version 1.19.0
import os
import fileinput


#// Funcion: RMCAB 2020 --> SAMSON
def rmcab2samson(dir_meteorologia: str, name_samson: str, dir_samson: str,
                  station_code: str = '44444',
                  station_name: str = 'KENNEDY',
                  station_location: str = 'CO -5  N 4 39  W 74 5'):
    '''
    Funcion de conversion de archivo meteorologico en formato RMCAB 2020 a SAMSON
    que retorna la direccion del nuevo archivo SAMSON.
    
    Parametros:
    dir_meteorologia = Direccion de archivo excel en formato RMCAB a convertir
    name_samson = Nombre de archivo con el que guardar el nuevo archivo SAMSON
    dir_samson = Directorio destino del archivo samson
    station_code = Codigo de estacion meteorologica; Default = '44444'
    station_name = Nombre de estacion meteorologica; Default = 'KENNEDY'
    station_location = Nombre de coordenadas de estacion; Default = 'CO -5  N 4 39  W 74 5'
    '''
    if not isinstance(dir_meteorologia, name_samson, dir_samson):
        raise TypeError

    if not os.path.isfile(dir_meteorologia):
        raise Exception('\nERROR: El archivo indicado no se encuentra')
    
    if not name_samson[-4:] != '.SAM':
        raise Exception('\nERROR: La extension del nombre del archivo debe finalizar en ".SAM"')
        
    if not os.path.isdir(dir_samson):
       raise Exception('\nERROR: El directorio no existe')

    #// Lectura de archivo de meteorologia formato RMCAB 2020     
    archivo_meteorologia = pd.read_excel(dir_meteorologia, headers = 3, 
                                        dtype = str, skiprows = [0, 1, 2, 4],
                                        skipfooter = 11, na_values = '----')

    #// Reasignacion de nombre de variables meteorlogicas segun formato SAMSON 
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

    #// Funcion de actualizacion de espacios en blanco de los valores
    def actualizar_espacios(i, columna, campos, nada, extra = ''):
        
        if pd.isna(archivo_meteorologia[columna][i]):
            archivo_meteorologia[columna][i] = nada
        elif len(archivo_meteorologia[columna][i]) < campos:
            temporary = archivo_meteorologia[columna][i]
            space = campos - len(archivo_meteorologia[columna][i])
            archivo_meteorologia[columna][i] = ' ' * space + temporary + extra

    #// Conversion de formato de valores 
    year = []; month = []; day = []; hour = []; flag = []; one = []
    two = []; four = []; five = []; six = []; seven = []; nine = []
    fourteen = []; fifteen = []; sixteen = []; eighteen = []; nineteen = []
    twenty = []; twentyone = []

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
        
        actualizar_espacios(i, '03', 4, '9999 ?0', ' ?0')
        actualizar_espacios(i, '08', 5, '9999.')
        actualizar_espacios(i, '10', 3, '999')
        actualizar_espacios(i, '11', 4, '9999')
        actualizar_espacios(i, '12', 3, '999')
        actualizar_espacios(i, '13', 5, '9999.')
        actualizar_espacios(i, '17', 4, '9999')
        
    archivo_meteorologia['01'] = '9999'
    archivo_meteorologia['02'] = '9999'
    archivo_meteorologia['04'] = '9999 ?0'
    archivo_meteorologia['05'] = '9999 ?0'
    archivo_meteorologia['06'] = ' 5'
    archivo_meteorologia['07'] = ' 5'
    archivo_meteorologia['09'] = '9999.'
    archivo_meteorologia['14'] = '99999.'
    archivo_meteorologia['15'] = '999999'
    archivo_meteorologia['16'] = '999999999'
    archivo_meteorologia['18'] = '99999.'
    archivo_meteorologia['19'] = '9999'
    archivo_meteorologia['20'] = '999'
    archivo_meteorologia['21'] = ' ' * 7

    headers = [*archivo_meteorologia]
    archivo_meteorologia.columns = headers
    headers.sort()
    archivo_meteorologia = archivo_meteorologia[headers]

    archivo_meteorologia['YR'] = list(year)
    archivo_meteorologia['MO'] = list(month)
    archivo_meteorologia['DA'] = list(day)
    archivo_meteorologia['HR'] = list(hour)
    archivo_meteorologia['I'] = list(flag)

    new_headers = ['YR', 'MO', 'DA', 'HR', 'I'] + headers
    archivo_meteorologia = archivo_meteorologia[new_headers]
    del archivo_meteorologia['00']

    #// Creacion de archivo SAMSON
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
    
    return dir_samson + "/" + name_samson