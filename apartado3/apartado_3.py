#!usr/bin/python3
from subprocess import call
import os
import subprocess

#Instalamos Docker
call(['sudo', 'apt-get', 'install', '-y', 'docker.io'])
call(['sudo', 'apt-get', 'install', '-y', 'docker-compose'])

#Instalaciones en la máquina virtual
call(['sudo', 'apt-get', 'upgrate'])
call(['sudo', 'apt-get', 'install', '-y', 'python3-pip']) 
call(['sudo', 'apt-get', 'install', '-y','git'])
call(['git', 'clone', 'https://github.com/CDPS-ETSIT/practica_creativa2.git'])
call(['sudo', 'apt-get', 'update'])


#Ejecutar el comando que dice el enunciado en la ruta src/reviews:				
os.chdir('practica_creativa2/bookinfo/src/reviews')
os.system('sudo docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build')
os.chdir(os.path.expanduser("~"))
os.chdir('practicaCreativa2/apartado3')
print("Directorio actual")
subprocess.run(['pwd'])
print("Archivos en el directorio actual")
subprocess.run(['ls', '-l'])


#Situarnos en la carpeta donde se encuentra docker-compose.yaml e iniciar los servicios definidos en ese archivo
#os.chdir('practica_creativa2/bookinfo/src')
call(['sudo', 'docker-compose', 'build'])
call(['sudo', 'docker-compose', 'up', '-d'])