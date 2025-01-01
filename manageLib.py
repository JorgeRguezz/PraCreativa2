import logging, subprocess, os

log = logging.getLogger('manage-p2.py')

# Despliegue de la aplicación en máquina virtual pesada
def mv_pesada (puerto):
  log.debug("mv_pesada ")
  subprocess.call(['git', 'clone', 'https://github.com/CDPS-ETSIT/practica_creativa2.git'])
  subprocess.run(['find', './', '-type', 'f', '-exec', 'sed', '-i', f's/Simple Bookstore App/GRUPO16/g', '{{}}', '\;'])
  os.chdir('practica_creativa2/bookinfo/src/productpage')
  subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])
  subprocess.call(['python3', 'productpage_monolith.py', f'{puerto}'])
