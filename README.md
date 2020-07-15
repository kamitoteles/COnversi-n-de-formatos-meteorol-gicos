# Meteorology data format conversors

This respository contains various scripts that should be usefull in order to convert divere meteorology data formats.

---
## RMCAB 2020 to SAMSON
This first conversor is contained into the python script 'RMCA_to_SAMSON.py'. The code was developed on python 3.7 and all the libraries used are described in the commented code.

The code is set to convert raw .xlsx meteorology data downloaded from the [Bogota Air Quality Monitoring Network](http://rmcab.ambientebogota.gov.co/Report/stationreport) (RMCA) to SAMSON text format.

An important consideration: the SAMSON file generated by this script will always have the same header `~44444 KENNEDY           CO -5  N 4 39  W 74 5`. If you want to convert the format of the data from another weather station of the RMCA, you must change the `title` variable at the end of the escript (line 160) so it matchs the code and location of your specific station.