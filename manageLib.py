import logging, subprocess, os

log = logging.getLogger('manage-p2.py')

GRUP_NUM = 16 # Variable de entorno con el número de grupo. No se si la tengo que definir aquí, en el script principal o en un json aparte.

# Despliegue de la aplicación en máquina virtual pesada
def mv_pesada (puerto):
  log.debug("mv_pesada ")
  subprocess.call(['git', 'clone', 'https://github.com/CDPS-ETSIT/practica_creativa2.git'])
  subprocess.run(['find', './', '-type', 'f', '-exec', 'sed', '-i', f's/Simple Bookstore App/GRUPO{GRUP_NUM}/g', '{{}}', '\;'])
  os.chdir('practica_creativa2/bookinfo/src/productpage')
  subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])
  subprocess.call(['python3', 'productpage_monolith.py', f'{puerto}'])
