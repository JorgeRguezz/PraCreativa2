import logging, subprocess, os

GRUP_NUM = 16 # Variable de entorno con el número de grupo. No se si la tengo que definir aquí, en el script principal o en un json aparte.
GRUP_NOM = 'g16'

log = logging.getLogger('manage-p2.py')


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
  subprocess.call(['sudo', 'docker', 'run', '--name', f'product-page-{GRUP_NOM}', '-p', '5080:5080', '-e', f'GROUP_NUM={GRUP_NUM}', '-d', f'product-page/{GRUP_NOM}'])

## 2.2. Eliminar todas las imágenes y contenedores Docker
def docker_destroy():
  subprocess.call(['sudo docker stop $(sudo docker ps -aq)'], shell=True)
  subprocess.call(['sudo docker rm $(sudo docker ps -aq)'], shell=True)
  subprocess.call(['sudo docker rmi --force $(sudo docker images -q)'], shell=True)
  
def mv_docker_compose (version, ratings, star):
  log.debug("mv_docker_compose ")
  # Guardar directorio raíz
  raiz = os.getcwd()
  # Clonar repositorio de la app
  subprocess.call(['git', 'clone', 'https://github.com/CDPS-ETSIT/practica_creativa2.git', '/practica_creativa2'])
  # Crear la imagen de ProductPage
  log.debug("CONSTRUIR PRODUCT_PAGE")
  subprocess.call(['sudo', 'docker', 'build', '-t', f'product-page/{GRUP_NOM}:latest', './ProductPage'])
  # subprocess.call(['sudo', 'docker', 'build', '-t', f'product-page/{GRUP_NOM}', './ProductPage'])
  subprocess.call(['sudo', 'docker', 'run', '--name', f'product-page-{GRUP_NOM}', '-p', '9080', '-d', '-it', f'product-page/{GRUP_NOM}:latest'])
  # Crear la imagen de Details
  log.debug("CONSTRUIR DETAILS")
  subprocess.call(['sudo', 'docker', 'build', '-t', f'details/{GRUP_NOM}:latest', './Details'])
  subprocess.call(['sudo', 'docker', 'run', '--name', f'details-{GRUP_NOM}', '-p', '9080', '-d', '-it', f'details/{GRUP_NOM}:latest'])
  # Crear la imagen de Ratings
  log.debug("CONSTRUIR RATINGS")
  subprocess.call(['sudo', 'docker', 'build', '-t', f'ratings/{GRUP_NOM}:latest', './Ratings'])
  subprocess.call(['sudo', 'docker', 'run', '--name', f'ratings-{GRUP_NOM}', '-p', '9080', '-d', '-it', f'ratings/{GRUP_NOM}:latest'])
  # Crear la imagen de Reviews
  log.debug("CONSTRUIR REVIEWS")
  os.chdir('practica_creativa2/bookinfo/src/reviews')
  subprocess.call(['sudo', 'docker', 'run', '--rm', '-u', 'root', '-v', '/home/gradle/project', '-w', '/home/gradle/project', 'gradle:4.8.1', 'gradle', 'clean', 'build'])
  subprocess.call(['sudo', 'docker', 'build', '-t', f'reviews/{GRUP_NOM}:latest', './reviews-wlpcfg']) 
  subprocess.call(['sudo', 'docker', 'run', '--name', f'reviews-{GRUP_NOM}', '-p', '9080', '-d', '-it', f'reviews/{GRUP_NOM}:latest'])
  
  # Cambiar al directorio raíz
  os.chdir(raiz)
  # Crear el contenido del fichero docker-compose.yaml
  log.debug("CONSTRUIR DOCKER_COMPOSE")
  contenido_docker_compose = f"""
      version: '3'
      services:
        product-page-{GRUP_NOM}:
          image: "product-page/{GRUP_NOM}:latest"
          ports:
            - 9080:9080
          environment:
            - GROUP_NUMBER=16
        details-{GRUP_NOM}:
          image: "details/{GRUP_NOM}:latest"
          environment:
            - SERVICE_VERSION=v1
            - ENABLE_EXTERNAL_BOOK_SERVICE=true
        reviews-{GRUP_NOM}:
          image: "reviews/{GRUP_NOM}:latest"
          environment:
            - SERVICE_VERSION={version}
            - ENABLE_RATINGS={ratings}
            - STAR_COLOR={star}
        ratings-{GRUP_NOM}:
          image: "ratings/{GRUP_NOM}:latest"
      """
  # Escribir el contenido en el fichero docker-compose.yaml
  with open('docker-compose.yaml', 'w') as file:
    file.write(contenido_docker_compose)

  # Crear los contenedores
  subprocess.call(['sudo', 'docker-compose', 'up'])