from subprocess import call
import os, sys
def build():
 # Clonar el repositorio
 os.system('git clone https://github.com/CDPS-ETSIT/practica_creativa2.git')
 os.system('sudo apt install -y docker-compose')
 # Construir la aplicación Reviews
 os.chdir('practica_creativa2/bookinfo/src/reviews')
 os.system('docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build')
 # Cambiar de directorio al proyecto principal
 os.chdir('/home/rrjorge8/PraCreativa2')
 os.system('pwd') # Mostrar la ruta actual para verificación
 # Ejecutar los comandos Docker Compose
 os.system('sudo docker-compose -f compose.yaml build')
 os.system('sudo docker-compose -f compose.yaml up')
def start():
    os.system('sudo docker-compose -f compose.yaml up')
def startdetached():
    os.system('sudo docker-compose -f compose.yaml up -d')
def stop():
    os.system('sudo docker-compose -f compose.yaml stop')
def delete():
    os.system('sudo docker-compose -f compose.yaml down')
    os.system('sudo rm -rf practica_creativa2/')
param = sys.argv
 # Comandos del script
if param[1] == "build":
 build()
elif param[1] == "start":
 start()
elif param[1] == "startdetached":
 startdetached()
elif param[1] == "stop":
    stop()
elif param[1] == "delete":
 delete()
else:
 print("Unknown command")