###  RMCAB 2020 TO SAMSON CONVERSOR
### Autor: Camilo Moreno - cama9709@gmail.com

#// Library imports //////////////////////////////////////////////////////////////////////////////#
import pandas as pd             # Version 1.0.5
import numpy as np              # Version 1.19.0
from datetime import datetime   # Version 4.3
import os
import fileinput
import glob

#// User input of the RMCAB 2020 file //////////////////////////////// //////////////////////////#
dir_meteorologia = ''
is_file = False
while len(dir_meteorologia) < 1 or not is_file:
    dir_meteorologia = input('\nEnter the RMCAB 2020 meteorology excel file: ')
    
    if os.path.isfile(dir_meteorologia):
        is_file = True 
    else: 
         print('\n!!!ERROR: File not found')
    
#// File name and location destiny set up for the SAMSON file ////////////////////////////////////#
name_samson = ''
while len(name_samson) < 1:
    name_samson = input('\nEnter the name for the SAMSON file: ')
    
    if name_samson[-4:] != '.SAM':
        print('\n!!!ERROR: Te file neme must end with ".SAM"')
        name_samson = ''
        
dir_samson = ''
is_dir = False
while len(dir_samson) < 1 or not is_dir:
    dir_samson = input('\nEnter the directory where you want to save the SAMSON file: ')
    
    if os.path.isdir(dir_samson):
        is_dir = True
    else: 
         print('\n!!!ERROR: The directory does not exist')

print('\nWAIT...')

#// RMCAB 2020 file reading  ////////////////////////////////////////////////////////////////////#    
archivo_meteorologia = pd.read_excel(dir_meteorologia, headers = 3, 
                                     dtype = str, skiprows = [0, 1, 2, 4],
                                     skipfooter = 11, na_values = '----')

#// File headers renaming ///////////////////////////////////////////////////////////////////////# 
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

#// No data filling function ////////////////////////////////////////////////////////////////////#
def actualizar_espacios(i, columna, campos, nada, extra = ''):
    
    if pd.isna(archivo_meteorologia[columna][i]):
        archivo_meteorologia[columna][i] = nada
    elif len(archivo_meteorologia[columna][i]) < campos:
        temporary = archivo_meteorologia[columna][i]
        space = campos - len(archivo_meteorologia[columna][i])
        archivo_meteorologia[columna][i] = ' ' * space + temporary + extra

#// Format conversion  //////////////////////////////////////////////////////////////////////////#
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
    
    flag.append('0')
    one.append('9999')
    two.append('9999')
    four.append('9999 ?0')
    five.append('9999 ?0')
    six.append(' 5')
    seven.append(' 5')
    nine.append('9999.')
    fourteen.append('99999.')
    fifteen.append('999999')
    sixteen.append('999999999')
    eighteen.append('99999.')
    nineteen.append('9999')
    twenty.append('999')
    twentyone.append(' ' * 7)
    
    actualizar_espacios(i, '03', 4, '9999 ?0', ' ?0')
    actualizar_espacios(i, '08', 5, '9999.')
    actualizar_espacios(i, '10', 3, '999')
    actualizar_espacios(i, '11', 4, '9999')
    actualizar_espacios(i, '12', 3, '999')
    actualizar_espacios(i, '13', 5, '9999.')
    actualizar_espacios(i, '17', 4, '9999')
    
archivo_meteorologia['01'] = one
archivo_meteorologia['02'] = two
archivo_meteorologia['04'] = four
archivo_meteorologia['05'] = five
archivo_meteorologia['06'] = six
archivo_meteorologia['07'] = seven
archivo_meteorologia['09'] = nine
archivo_meteorologia['14'] = fourteen
archivo_meteorologia['15'] = fifteen
archivo_meteorologia['16'] = sixteen
archivo_meteorologia['18'] = eighteen
archivo_meteorologia['19'] = nineteen
archivo_meteorologia['20'] = twenty
archivo_meteorologia['21'] = twentyone

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

#// SAMSON file creation /////////////////////////////////////////////////////////////////////////#
# !!!! IMPORTANT: It is set to default that the meteorology data proceeds from the Kennedy station
#                 of the RMCAB.
#
#                 If you want to use another station, you must change the station_code,  
#                 station_name and station_location variables listed below.
#/////////////////////////////////////////////////////////////////////////////////////////////////#
np.savetxt('tepm_' + name_samson, archivo_meteorologia.values, fmt = ' %s', delimiter = '')

#// Station variables to change /////////////////////////////////////////////////////////////////#
station_code = '44444'
station_name = 'KENNEDY'
station_location = 'CO -5  N 4 39  W 74 5'

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


#// Confirmation message ////////////////////////////////////////////////////////////////////////#
print(f'\n====================================')
print(f'=======CONVERSION COMPLETED!========')
print(f'====================================')
print(f'RMCAB File: {dir_meteorologia}')
print(f'SAMSON File: {dir_samson + "/" + name_samson}')