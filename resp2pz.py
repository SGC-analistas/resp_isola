#!/usr/bin/env python

from resp import RespFile
import sys
import os
import time 
import pathlib

try:
  pat_or_file = sys.argv[1]
except IndexError:
	print ("\n\n Argumentos insuficientes.\n Debe ingresar el archivo\
 RESP a convertir o el directorio que contiene los archivos como argumento. Ejem:\n\
	\t ./resp2pz.py RESP.CM.PTB.00.HHZ o ./resp2pz.py /directorio/con/archivos/RESP\n")
	sys.exit(1)
if os.path.isfile(pat_or_file):
	resp = RespFile(pat_or_file)
	# si la funcion devuelve True completo exitosamente
	success = resp.resp2pz()
else:
	
	for f in os.listdir(pat_or_file):
		
		resp = RespFile(pat_or_file+"/"+f)
		success = resp.resp2pz('/opt/rutinas/Archivos_respuesta/pz_files' + (time.strftime('/%Y/%m/%d')))

		if not success:
			continue
		
	
	print ("Archivos .pz en la ruta" + ' /opt/rutinas/Archivos_respuesta/pz_files' + (time.strftime('/%Y/%m/%d')))
