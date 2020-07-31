# Conversores de formato de datos meteorológicos

Este repositorio contiene herramientas de conversión de formatos de archivos de meteorología de fácil implementaión. La carpeta  `metconversor` contiene todas las implementaciones en formato de funciones de python. Los scripts que se encuentran fuera de dicha carpeta son implementaciones pensadas para ser corridas en un IDE.

---
## RMCAB 2020 a SAMSON
Esta herramienta está configurada para convertir datos de meteorología .xlsx sin procesar descargados de la [Red de Monitoreo de Calidad del Aire de Bogotá] (http://rmcab.ambientebogota.gov.co/Report/stationreport) (RMCA) al formato de texto SAMSON.

Importante: el archivo SAMSON generado por este script siempre tendrá el mismo encabezado `~ 44444 KENNEDY CO -5 N 4 39 W 74 5`. Si desea convertir el formato de los datos de otra estación meteorológica **diferente a Kennedy**, debe cambiar las variables `station_code`, `station_name` y `station_location` para que coincidan con los atributos de la estación escogida.

Importante 2: el script asume que la **cobertura total de nubes** y la **cobertura de nubes opacas** tienen un valor constante de 5.
