#!/usr/bin/env python
import json, logging, os, sys, subprocess
import lxml.etree as ET
from manageLib import VM, Red

def init_log(debug=False):  # -> Creación y configuración del logger (debug por defecto a False)
    logging.basicConfig(level=logging.DEBUG) # -> Nivel de log por defecto
    log = logging.getLogger('manage-p2') # -> Creación del logger
    log.setLevel(logging.DEBUG if debug else logging.INFO)  # -> Nivel de log dependiendo de si la variable debug pasada como parámetro es True o False

    # Configura un handler para enviar los logs al stdout
    ch = logging.StreamHandler(sys.stdout) # -> Creación del handler
    ch.setLevel(logging.DEBUG if debug else logging.INFO) # -> Nivel de log dependiendo de si la variable debug pasada como parámetro es True o False

    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s' if debug else '%(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)

    log.addHandler(ch)
    log.propagate = False

def create_default_config(): # -> Creación del archivo manage-p2.json con la configuración por defecto si este no existe (MEJORA)
    config_data = {
        "number_of_servers": 3,
        "debug": True
    }

    with open("manage-p2.json", "w") as config_file:
        json.dump(config_data, config_file, indent=4)
    
    print("Archivo manage-p2.json creado con contenido predeterminado.")

def load_configuration(): # -> Carga la configuración del archivo manage-p2.json
    config_path = 'manage-p2.json'
    if not os.path.exists(config_path):
        print(f"Archivo {config_path} no encontrado. Creando uno con configuración predeterminada.")
        create_default_config()

    with open(config_path) as config_file:
        return json.load(config_file)

def main():
    # Verificar que se pasa un comando
    if len(sys.argv) < 2: # -> Si no se pasa ningún comando sale error
        print("Uso: python3 manage-p2.py <comando>")
        sys.exit(1) # -> Salimos del script con código de error 1

    # Comando principal
    orden = sys.argv[1] # -> Guardamos el comando pasado como argumento (create, start, stop, destroy, monitor)

    # Si el comando es "create", asegúrate de que el archivo de configuración exista
    if orden == "create":
        if not os.path.exists("manage-p2.json"):
            print("Creando archivo de configuración predeterminado...")
            create_default_config()

    # Cargar configuración
    config = load_configuration()
    debug_mode = config.get("debug", False)  # Obtiene el valor de debug (False por defecto)

    # Inicializar logger
    init_log(debug=debug_mode)
    log = logging.getLogger('manage-p2')
    log.info("Iniciando script manage-p2")

    num_servidores = config.get("number_of_servers", 0)
        
    # Creamos los componentes de la red menos los servidores
    c1 = VM("c1")
    host = VM("host")
    lb = VM("lb")
    red = Red("red")

    if orden == "create":
        log.info("Preparando entorno antes de crear la red y las máquinas virtuales")
        # Ejecutar el comando prepare-vnx-debian
        log.debug("Ejecutando comando: /lab/cnvr/bin/prepare-vnx-debian")
        subprocess.call(["/lab/cnvr/bin/prepare-vnx-debian"]) # -> Ejecutamos el comando prepare-vnx-debian (MEJORA)
        
        log.info("Creando la red virtual y las máquinas")
        red.create_red()  # -> Creamos la red
        for i in range(num_servidores):  # -> Definimos los servidores y los creamos 
            s = VM(f's{i + 1}')
            s.create_vm("LAN2", False)
        c1.create_vm("LAN1", False)
        host.create_vm("LAN1", False)
        lb.create_vm("null", True)

    elif orden == "start":
        log.info("Arrancando las máquinas virtuales")
        if len(sys.argv) < 3: # (MEJORA)
            for i in range(num_servidores):
                server = VM(f's{i + 1}')
                server.start_vm()
            c1.start_vm()
            host.start_vm()
            lb.start_vm()
        else:
            name_VM = sys.argv[2]
            vm = VM(name_VM)
            vm.start_vm()

    elif orden == "stop":
        log.info("Deteniendo las máquinas virtuales")
        if len(sys.argv) < 3:
            for i in range(num_servidores):
                server = VM(f's{i + 1}')
                server.stop_vm()
            c1.stop_vm()
            host.stop_vm()
            lb.stop_vm()
        else:
            name_VM = sys.argv[2]
            vm = VM(name_VM)
            vm.stop_vm()

    elif orden == "destroy":
        log.info("Destruyendo las máquinas virtuales y la red")
        for i in range(num_servidores):
            s = VM(f's{i + 1}')
            s.destroy_vm()
        c1.destroy_vm()
        host.destroy_vm()
        lb.destroy_vm()
        red.destroy_red()

    elif orden == "monitor": # (MEJORA)
        log.info("Monitorizando el estado de las máquinas virtuales")
        subprocess.call(["sudo", "virsh", "list", "--all"])
        print("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª")
        for i in range(num_servidores):
                server = VM(f's{i + 1}')
                server.monitor()
        c1.monitor()
        host.monitor()
        lb.monitor()


    else:
        log.error(f"Orden no reconocida: {orden}")

if __name__ == "__main__":
    main()
