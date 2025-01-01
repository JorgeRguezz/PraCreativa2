import logging, subprocess, os

log = logging.getLogger('manage-p2.py')

GRUP_NUM = 16 # Variable de entorno con el número de grupo. No se si la tengo que definir aquí, en el script principal o en un json aparte.
GRUP_NOM = 'g16'

# 1. DESPLIEGUE DE LA APLICACIÓN EN MÁQUINA VIRTUAL PESADA
def mv_pesada (puerto):
  log.debug("mv_pesada ")
  subprocess.call(['git', 'clone', 'https://github.com/CDPS-ETSIT/practica_creativa2.git'])
  subprocess.run(['find', './', '-type', 'f', '-exec', 'sed', '-i', f's/Simple Bookstore App/GRUPO: {GRUP_NUM}/g', '{}', '+'])
  os.chdir('practica_creativa2/bookinfo/src/productpage')
  subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])
  subprocess.call(['python3', 'productpage_monolith.py', f'{puerto}'])

# 2. DESPLIEGUE DE LA APLICACIÓN MONOLÍTICA USANDO DOCKER
## 2.1. Despliegue de la aplicación mediante Docker
def mv_docker ():
  log.debug("mv_docker ")
#   subprocess.call(['sudo', 'docker', 'build', '-t', 'g27/product-page-mono', '.'])
  subprocess.call(['sudo', 'docker', 'build', '-t', f'product-page/{GRUP_NOM}', '.'])
#   subprocess.call(['sudo', 'docker', 'run', '--name', 'g27-product-page-mono', '-p', '9080:9080', '-e', 'GROUP_NUMBER=27', 'g27/product-page-mono'])
  subprocess.call(['sudo', 'docker', 'run', '--name', f'product-page-{GRUP_NOM}', '-p', '9080:5060', '-e', f'GROUP_NUM={GRUP_NUM}', '-d', f'product-page/{GRUP_NOM}'])

## 2.2. Eliminar todas las imágenes y contenedores Docker
def docker_destroy():
  subprocess.call(['sudo docker stop $(sudo docker ps -aq)'], shell=True)
  subprocess.call(['sudo docker rm $(sudo docker ps -aq)'], shell=True)
  subprocess.call(['sudo docker rmi --force $(sudo docker images -q)'], shell=True)