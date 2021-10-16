![SGC](images/logoSGC.png)<!-- .element width="700"-->

# SGC_Archivos_respuesta

Rutina creada con el fin de transformar los archivos de respuesta a formato ISOLA, de manera simple y para acceso de todos los miembros de la red sismológica.
El rutina crea un archivo de respuesta .pz (isola) de un archivo RESP o de un directorio que contenga varios archivos RESP, creando un directorio llamado pz_files donde se almacenaran los archivos siguiento una estructura de caperta basadas en año mes y dia de la ejecución.

**SI ESTA EN EL PROC4 NO ES NECESARIA LA SECCION DE INSTALACIÓN**

## 1. Instalacion en linux 

Python version 3.7 
```bash
sudo apt-get install python3.7 
```
Instalar virtualenv
```bash
python3.7 -m pip install virtualenv
```

### Crear ambiente virtual con virtualenv
```bash
python3.7 -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
##2. Arquitectura

###1. Archivos:

-**resp.py**: Contiene la clase RespFile que saca la información relevante del archivo resp de todas las actualizaciones que se han hecho y las guarda en un diccionario, ademas de ser la ejecución en una carpeta con varios archivos creara una carpeta pz_files.
-**resp2pz.py**: Crea el archivo pz de la última actualización al archivo RESP que se pase por defecto.
-**example.pz**: Archivo de txt que contiene la forma del achivo de respuesta .pz

**TODOS ESTOS ARCHIVOS DEBEN ESTAR UBICADOS EN EL MISMO DIRECTORIO**

###2. Carpetas:

-**pz_files**: Esta carpeta se creara automaticamente por la rutina y contendra una estructura de carpetas con año mes y dia, alli se almacenaran los archivos .pz en el dia que se ejecute el codigo.


##3. Instrucciones de uso:

**IMPORTANTE**

El script recibe 1 argumento este puede ser la ruta de una carpeta donde esten almacenados varios archivos o una ruta a un archivo en especifico.

###1. Se ejecuta el script para una carpeta:

El script se encuentra disponible para todos en el proc4, la ejecución se realiza de la siguiente manera.

```bash
python3.7 /opt/rutinas/Archivos_respuesta/resp2pz.py /ruta/carpeta/con/archivos
```
Para el resto de proc solamente se cambia la ruta de la ubicacion del archivo resp2pz.py

Una vez se ejecute esta rutina los archivos de respuesta se alojaran en la ruta /opt/rutinas/Archivos_respuesta/pz_files/año/mes/dia
Los archivos de respuesta en el formato necesario para transformalos al formato ISOLA se actualizan automaticamente a medida que se agregan nuevas estaciones en la ruta /mnt/dl2resp/ por lo tanto se recomienda ejecutar el script utilizando esta ruta como argunmento.

```bash
python3.7 /opt/rutinas/Archivos_respuesta/resp2pz.py /mnt/dl2resp/
```

**RECOMENDACIONES PROC4**

Para la ejecución en el proc4 se recomienda agregar la siguiente linea al archivo .bashrc que se encuentra en el home de cada usuario:

```bash
alias resp_isola="source /opt/rutinas/Archivos_respuesta/.venv/bin/activate; python /opt/rutinas/Archivos_respuesta/resp2pz.py /mnt/dl2resp"
```
Posteriormente correr el siguiente codigo en consola:
```bash
source .bashrc
```
De este manera solo escribiendo en la consola **resp_isola** se ejecutara el codigo y se actualizaran los archvos de respuesta en la ruta /opt/rutinas/Archivos_respuesta/pz_files/año/mes/dia

###2. Se ejecuta el script para un archivo:

El script se encuentra disponible para todos en el proc4, la ejecución se realiza de la siguiente manera.
```bash
python3.7 /opt/rutinas/Archivos_respuesta/resp2pz.py /ruta/doc/
```

El archivo .pz se alojara en la misma ubicacion donde esta el archivo a trasnformar.

Para el resto de proc solamente se cambia la ruta de la ubicacion del archivo resp2pz.py


##4. Autores

- Geronimo Valencia gvalenciah@sgc.gov.codigo
- Daniel Siervo dsiervo@sgc.gov.co
