#!/usr/bin/env python
# ---- dsiervo@sgc.gov.co-------
# ---- gvalenciah@sgc.gov.co----
import sys

class RespFile:
	
	def __init__(self,file_name):
		self.file_name = file_name
		l = file_name.split(".")
		if len(l) != 5 and l[0] != "RESP":
			print ("El archivo RESP debe nombrarse de la forma estandar:\n \
			 \t RESP.network.station.location_code.channel  ejem --> RESP.CM.PTB.00.HHZ")
			return None
		self.station = l[2]
		self.sensor = l[3]
		if self.sensor == '':
			self.sensor = '50'		
		self.channel = l[4]
		self.in_file = open(file_name).readlines()
		
		# bloques (numero de archivos de respuesta)
		# en un RESP file. 
		self.blocks = 1
		
		# lista que contiene diccionarios con la informacion relevante
		# de los RESP files.
		self.blocks_info = []
		
		# metodo que llena a self.block_info
		self.separate_blocks()
		print (self.file_name)
	
	
	# metodo que cuenta el numero de bloques en el archivo RESP.
	# Lo hace contando las veces que aparece la linea de Station
	def count_blocks(self):
		# lista que contendra los indices de las lineas donde termina
		# cada bloque
		l_index = []
		for i in range(len(self.in_file)):
			if self.in_file[i][0:7] == "B050F03": 
				#print i
				l_index.append(i)
		
		self.blocks = len(l_index)
		
		#print l_index
		return l_index
	
	
	# metodo que separa los bloques del archivo RespFile 
	# en diccionarios contenidos en una lista
	def separate_blocks(self):
		f = self.in_file
		for i in self.count_blocks():
			dic = {}
			zeroes = []
			poles = []
			for j in range(i,len(f)):
				if f[j][0:7] ==  "B052F22": dic["start date"] = f[j][25:-1]
				if f[j][0:7] ==  "B052F23": dic["end date"] = f[j][25:-1]
				if f[j][0:7] ==  "B053F07": dic["A0"] = f[j][51:-1].strip(" ")
				if f[j][0:7] ==  "B053F09": dic["num zeroes"] = f[j][51:-1].strip(" ")
				if f[j][0:7] ==  "B053F14": dic["num poles"] = f[j][51:-1].strip(" ")
				if f[j][0:10]=="B053F10-13": zeroes.append(f[j][16:43].strip())
				if f[j][0:10] ==  "B053F15-18": poles.append(f[j][16:43].strip())
				if f[j][0:7] ==  "B058F03":
					if f[j][51:-1].strip(" ") == "1":
						dic["seism sens"] = f[j+1][51:-1].strip(" ")
					elif f[j][51:-1].strip(" ") == "3":
						dic["digi sens"] = f[j+1][51:-1].strip(" ")
				if f[j][26:45] == "Channel Sensitivity":
					dic["zeroes"] = zeroes
					dic["poles"] = poles
					self.blocks_info.append(dic)
					break

			if "\n".join(f).find("Channel Sensitivity") == -1:
				try:
					print ("\n\tEl archivo RESP %s no contiene el bloque Channel Sensitivity\n")%(self.file_name)
					dic["zeroes"] = zeroes
					dic["poles"] = poles
					self.blocks_info.append(dic)
				except:
					return False
	
	# devuelve en un diccionario los datos de la ultima actualizacion al
	# archivo RESP	
	def get_last_block(self):
		return self.blocks_info[len(self.blocks_info)-1]
	
	# crea un archivo pz (isola) del archivo RESP
	def resp2pz(self, pzdir):
		
		from obspy import UTCDateTime
		import time 
		import os

		if (self.sensor != '00' and self.sensor != '10') or self.sensor == -1 :
			print('Sensor no necesario')
			return False
		
		 
		try:
			pz_name = self.station+"B"+self.channel[1:]+".pz"
		except:
			return False
		# se coloca channel bh debido a la decimacion en isola
		root_path= "/opt/rutinas/Archivos_respuesta/pz_files"

		if not os.path.exists(root_path + (time.strftime('/%Y/%m/%d'))):
			os.makedirs(root_path +  (time.strftime('/%Y/%m/%d')))		
		try:
			pz = open(os.path.join(pzdir, pz_name),"w")
		except:
			return False
		f = open("/opt/rutinas/Archivos_respuesta/example.pz").read()
		try:
			dic = self.get_last_block()
		except IndexError:
			return False
		
		try:
			dic["seism sens"]
		except KeyError:
			print('\n\n\tNo fue posible encontrar sensibilidad del sismometro en el archivo %s'%self.file_name)
			return False
		try:
		  count = 1.0/(float(dic["seism sens"])*float(dic["digi sens"]))
		except KeyError as ke:
		  print (("\n  \tel arhivo %s no contiene %s, se asume 4.194300E+05\n")%(self.file_name, ke))
		  dic["digi sens"] = "4.194300E+05"
		  count = 1.0/(float(dic["seism sens"])*float(dic["digi sens"]))
		  
		  
		l_t = dic["start date"].split(",")
		t = UTCDateTime(year=int(l_t[0]),julday=int(l_t[1]))
		try:
			f = f%(dic["A0"], count, dic["num zeroes"], "\n".join(dic["zeroes"]),dic["num poles"],"\n".join(dic["poles"]),
			t.strftime("%d-%b-%Y"), self.station, "%.2f"%float(dic["digi sens"]), "%.2f"%float(dic["seism sens"]))
		except KeyError:
			print('\n \t No se pudo completar el archivo de respuesta ')
		
		print (("Creando archivo %s")%(pz_name))
		pz.write(f)
		pz.close()
		return True

if __name__ == "__main__":
  
  PTB = RespFile("RESP.CM.PTB.00.BHZ")
  #PTB.separate_blocks()
  #print PTB.blocks
  #print PTB.blocks_info
  #for block in PTB.blocks_info: print block["start date"]
  PTB.resp2pz()
  
