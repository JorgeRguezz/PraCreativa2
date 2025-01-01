import subprocess, logging, os, getpass
import lxml.etree as ET
from copy import deepcopy

log = logging.getLogger('manage-p2') # -> Creación un logger con el nombre "manage-p2"

# Clase para manejar máquinas virtuales
class VM:
    def __init__(self, name): # -> Inicialización de las máquinas virtuales
        self.name = name # -> Nombre de la MV pasado como parámetro
        self.image_base = "cdps-vm-base-pc1.qcow2" # -> Imagen base de la MV (todas la misma)
        self.xml_template = "plantilla-vm-pc1.xml" # -> Plantilla XML de la MV (todas la misma)
        self.usuario = getpass.getuser() # -> Nombre del usuario donde se ejecuta el script 
        log.debug(f"Inicializando máquina virtual: {self.name}") 

    def create_vm(self, interfaz_red, router):  # -> Creación de las máquinas virtuales. Parámetros: self(no cuenta), LAN a la que pertenecen y si actuan como router o no
        log.info(f"Creando máquina virtual: {self.name}")
        log.debug(f"Usando imagen base: {self.image_base}, plantilla XML: {self.xml_template}")

        subprocess.call(["qemu-img", "create", "-F", "qcow2", "-f", "qcow2", "-b", self.image_base, f"{self.name}.qcow2"]) # -> Creación de la imagen base para la MV de nombre pasado como parámetro
        log.debug(f"Imagen de disco creada: {self.name}.qcow2")

        subprocess.call(["cp", self.xml_template, f"{self.name}.xml"]) # -> Copia de la plantilla XML para la MV de nombre pasado como parámetro
        log.debug(f"Archivo XML generado: {self.name}.xml")

        tree = ET.parse(f"{self.name}.xml") # -> Parseamos el archivo XML de la MV a lxml tree (arbol de nodos, nos permite navegar por el XML)
        root = tree.getroot() # -> Obtenemos el nodo raíz del XML

        # Camnbiamos el nombre de la MV en el XML por el nombre pasado como parámetro
        name = root.find("name") 
        name.text = self.name

        # Cambiamos la ruta de la imagen base en el XML por la ruta de la imagen creada
        source_file = root.find("./devices/disk/source") # -> Obtenemos la etiqueta "source", dentro de "disk", dentro de "devices" en el XML
        source_file.set("file", f"/mnt/tmp/{self.usuario}/{self.name}.qcow2") # -> Cambiamos el atributo "file" de la etiqueta "source" 
        log.debug(f"Ruta de disco configurada: /mnt/tmp/{self.usuario}/{self.name}.qcow2")

        # Configuración de red
        if router: # -> Si la MV es True en el parámetro router
            log.info(f"Configurando red para el router: {self.name}")
            interface_tag = root.find(".//interface") # -> Obtenemos la etiqueta "interface" en el XML (solo hay una) (La "//" significa que busca a cualquier altura de las etiquetas)
            source_tag1 = interface_tag.find(".//source") # -> Obtenemos la etiqueta "source" dentro de "interface" 
            source_tag1.set("bridge", "LAN1")  # -> Cambiamos el atributo "bridge" de la etiqueta "source" con el valor "LAN1" (el contrario que la otra etiqueta "interface")
            ET.SubElement(interface_tag, "virtualport").set("type", "openvswitch") # -> Establecemos los bridges con tecnologia Open VSwitch. Añadimos una nueva etiqueta "virtualport" a "interface" con el atributo "type" y valor "openvswitch"
            log.debug(f"Interfaz principal configurada para bridge LAN1 con soporte Open vSwitch")

            new_interface = deepcopy(interface_tag) # -> Creamos una copia de la etiqueta "interface" (deepcopy copia todo el contenido de la etiqueta)
            root.find(".//devices").append(new_interface) # -> Encontramos la etiqueta "devices" (da igual a que altura) y añadimos la nueva etiqueta "interface" copiada

            source_tag2 = new_interface.find(".//source") # -> Obtenemos la etiqueta "source" dentro de la nueva etiqueta "interface"
            source_tag2.set("bridge", "LAN2") # -> Cambiamos el atributo "bridge" de la etiqueta "source" con el valor "LAN2" (el contrario que la otra etiqueta "interface")
            ET.SubElement(new_interface, "virtualport").set("type", "openvswitch") # -> Establecemos los bridges con tecnologia Open VSwitch. Añadimos una nueva etiqueta "virtualport" a la nueva "interface" con el atributo "type" y valor "openvswitch"
            log.debug(f"Interfaz secundaria configurada para bridge LAN2 con soporte Open vSwitch")
        else: # -> Si la MV es False en el parámetro router
            source_tag = root.find("./devices/interface/source") # -> Obtenemos la etiqueta "source", dentro de "interface", dentro de "devices" 
            source_tag.set("bridge", interfaz_red) # Cambia el valor de "bridge" en la etiqueta "source" por el valor de la interfaz de red pasada como parámetro (LAN1 o LAN2)
            ET.SubElement(root.find("./devices/interface"), "virtualport").set("type", "openvswitch") # -> Establecemos los bridges con tecnologia Open VSwitch. Añadimos una nueva etiqueta "virtualport" a "interface" con el atributo "type" y valor "openvswitch"
            log.debug(f"Interfaz configurada para bridge {interfaz_red} con soporte Open vSwitch")

        tree.write(f"{self.name}.xml") # -> Escribimos el árbol de nodos en el archivo XML de la MV
        log.info(f"Máquina virtual {self.name} configurada correctamente")

    def start_vm(self): # -> Arranque de las máquinas virtuales
        log.debug("arrancar MV " + self.name)
            
        # Configuracion de VMs antes de arrancar, modificando los ficheros /etc/hosts, /etc/hostname y /etc/network/interfaces de cada MV (RQ4)
        vm_image_path = f"/mnt/tmp/{self.usuario}/{self.name}.qcow2"
        # 1) Cambiar la dirección IP de las interfaces de red en /etc/network/interfaces
            # 1.1) Crear contenido de las interfaces
            
        server_ip_addresses = { # -> Diccionario con las direcciones IP asociadas a los servers
                "s1": "10.1.2.11",
                "s2": "10.1.2.12",
                "s3": "10.1.2.13",
                "s4": "10.1.2.14",
                "s5": "10.1.2.15", 
            }
        other_ip_addresses = { # -> Diccionario con las direcciones IP asociadas al resto de maquinas   
                "c1": "10.1.1.2",
                "host": "10.1.1.3"
            }

        if self.name in server_ip_addresses: # -> Verificar si la MV es un servidor
                contenido_interfaces = f"""
                auto lo
                iface lo inet loopback

                auto eth0
                    iface eth0 inet static
                    address {server_ip_addresses[self.name]}
                    netmask 255.255.255.0
                    gateway 10.1.2.1
                """
        elif self.name in other_ip_addresses: # -> Verificar si la MV es del otro lado del enlace
                contenido_interfaces = f"""
                auto lo
                iface lo inet loopback

                auto eth0
                    iface eth0 inet static
                    address {other_ip_addresses[self.name]}
                    netmask 255.255.255.0
                    gateway 10.1.1.1
                """
        elif self.name == "lb": # -> Verificar si la máquina es el router ("lb")
                contenido_interfaces = """
                auto lo
                iface lo inet loopback
        
                auto eth0
                    iface eth0 inet static
                    address 10.1.1.1
                    netmask 255.255.255.0
        
                auto eth1
                    iface eth1 inet static
                    address 10.1.2.1
                    netmask 255.255.255.0
                """
        else:
                raise ValueError(f"Nombre de máquina desconocido: {self.name}")
            
        directorio_trabajo = os.getcwd() # -> Obtenemos el directorio de trabajo actual (/mnt/tmp/jorge.rodriguez)

            # 1.2) Escribir el contenido en el fichero /etc/network/interfaces
        ruta_interfaces = os.path.join(directorio_trabajo, "interfaces") # -> Creamos la ruta /mnt/tmp/jorge.rodriguez/interfaces
        with open(ruta_interfaces, 'w') as interfaces:
            interfaces.write(contenido_interfaces) # -> Escribimos el contenido de las interfaces en el fichero /mnt/tmp/jorge.rodriguez/interfaces
            
        # 2) Cambiar el nombre de la MV en /etc/hostname
        ruta_hostname = os.path.join(directorio_trabajo, "hostname") # -> Creamos la ruta /mnt/tmp/jorge.rodriguez/hostname
        with open(ruta_hostname, 'w') as hostname:
            hostname.write(f'{self.name}')  # -> Escribimos el nombre de la MV en el fichero /mnt/tmp/jorge.rodriguez/hostname
        
        # Copiar los ficheros de configuración a las máquinas virtuales
        subprocess.call(['sudo', 'virt-copy-in', '-a', f'{self.name}.qcow2', 'interfaces', '/etc/network']) # -> Copia el fichero /mnt/tmp/jorge.rodriguez/interfaces al directorio /etc/network de la MV
        subprocess.call(['sudo', 'virt-copy-in', '-a', f'{self.name}.qcow2', 'hostname', '/etc']) # -> Copia el fichero /mnt/tmp/jorge.rodriguez/hostname al directorio /etc/hostname de la MV
        
        # 3) Cambiar la dirección de la MV en /etc/hosts
        subprocess.call(['sudo', 'virt-edit', '-a', vm_image_path, '/etc/hosts', '-e', f"s/127.0.1.1.*/127.0.1.1 {self.name}/"]) # -> Sustituye la linea 127.0.1.1 "lo que sea" por 127.0.1.1 s1 (por ejemplo) del fichero /etc/hosts de la MV
        
        # Configuramos el balanceador de carga como un router (MEJORA)
        if self.name == "lb":
            os.system(f"sudo virt-edit -a {self.name}.qcow2 /etc/sysctl.conf -e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'") # -> Habilitar el reenvío de paquetes en el balanceador de carga. Descomenta la linea "net.ipv4.ip_forward=1" en el fichero /etc/sysctl.conf (Enunciado)
            
            # Ruta completa al archivo "rc.local"
            ruta_rc = os.path.join(directorio_trabajo, "rc.local") # -> Creamos la ruta /mnt/tmp/jorge.rodriguez/rc.local
            # Crear el contenido de rc.local
            contenido_rc = """
            #!/bin/bash
            # Detener el servicio Apache
            sudo service apache2 stop
            
            # Añadir configuración a haproxy.cfg
            sudo cat <<EOL >> /etc/haproxy/haproxy.cfg
            frontend lb
                bind *:80
                mode http
                default_backend webservers
            backend webservers
                mode http
                balance roundrobin
                server s1 10.1.2.11:80 check
                server s2 10.1.2.12:80 check
                server s3 10.1.2.13:80 check
            EOL

            # Reiniciar el servicio HAProxy
            sudo service haproxy restart
            exit 0
            """

            # Escribir el contenido sobre el archivo "rc"
            with open(ruta_rc, 'w') as rc:
                rc.write(contenido_rc) # -> Escribimos el contenido del archivo rc.local en el fichero /mnt/tmp/jorge.rodriguez/rc.local

            # Copiar el fichero de configuración al router lb
            subprocess.call(['sudo', 'virt-copy-in', '-a', 'lb.qcow2', 'rc.local', '/etc']) # -> Copia el fichero /mnt/tmp/jorge.rodriguez/rc.local al directorio /etc de la MV lb

            # Asignar permisos de ejecución al archivo rc.local en el router lb
            subprocess.call(['sudo', 'virt-customize', '-a', 'lb.qcow2', '--run-command', 'chmod +x {}'.format('/etc/rc.local')]) 
        # (FIN DE LA MEJORA)
        
        os.environ["HOME"]= "/mnt/tmp/" # -> Establecemos la variable de entorno HOME para que apunte al directorio /mnt/tmp/usuario (HOME=/mnt/tmp/jorge.rodriguez)
        subprocess.call(["sudo", "virt-manager"]) # -> Abrimos el gestor de máquinas virtuales
            
        subprocess.call(["sudo", "virsh", "define", f'{self.name}.xml']) # -> Definimos la MV en el sistema
        subprocess.call(["sudo", "virsh", "start", self.name]) # -> Arrancamos la MV
        log.debug('Abriendo consola de la MV: ' + self.name)
        subprocess.Popen(["xterm", "-rv", "-sb", "-rightbar", "-fa", "monospace", "-fs", "10", "-title", f"'{self.name}'","-e", f"sudo virsh console {self.name}"]) # -> Abrimos una terminal (xterm) y accedemos a la consola de la MV (virsh console).
        #  subprocess.call(["xterm", "-rv", "-sb", "-rightbar", "-fa", "monospace", "-fs", "10", "-title", f"'{self.name}'","-e", f"sudo virsh console {self.name}", "&"])  #  Utilizamos subprocess.Popen pq a diferencia de subprocess.call, que espera a que el
                                                                                                                                                                            #  comando termine antes de continuar, Popen permite una interacción más avanzada con el proceso,
                                                                                                                                                                            #  incluyendo la posibilidad de ejecutarlo en segundo plano. 

    def stop_vm(self):  # -> Parada de las máquinas virtuales
        log.info(f"Apagando máquina virtual: {self.name}")
        subprocess.call(["sudo", "virsh", "shutdown", self.name]) # -> Apagamos la MV
        log.debug(f"Máquina virtual {self.name} apagada correctamente")

    def destroy_vm(self):  # -> Destrucción de las máquinas virtuales
        log.info(f"Destruyendo máquina virtual: {self.name}")
        subprocess.call(["sudo", "virsh", "destroy", self.name]) # -> Destruimos la MV
        subprocess.call(["rm", "-f", f"{self.name}.qcow2", f"{self.name}.xml", "interfaces", "hostname", "rc.local"]) # -> Eliminamos los archivos asociados a la MV (imagen, XML, interfaces, hostname, rc.local)
        log.debug(f"Archivos asociados a {self.name} eliminados")
    def monitor(self):
        print(f"Información detallada de {self.name} ->")
        print("")
        subprocess.call(["sudo", "virsh", "dominfo", self.name])
        print("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª")

# Clase para manejar redes virtuales
class Red:
    def __init__(self, name):
        self.name = name
        log.debug(f"Inicializando red: {self.name}")

    def create_red(self):  # -> Creación de las redes virtuales
        log.info("Creando los bridges LAN1 y LAN2")
        subprocess.call(["sudo", "ovs-vsctl", "add-br", "LAN1"]) # -> Creamos el bridge LAN1
        log.debug("Bridge LAN1 creado")
        subprocess.call(["sudo", "ovs-vsctl", "add-br", "LAN2"]) # -> Creamos el bridge LAN2
        log.debug("Bridge LAN2 creado")
        subprocess.call(["sudo", "ifconfig", "LAN1", "up"]) # -> Activamos el bridge LAN1
        subprocess.call(["sudo", "ifconfig", "LAN2", "up"]) # -> Activamos el bridge LAN2
        log.info("Bridges LAN1 y LAN2 activados")

    def destroy_red(self):  # -> Destrucción de las redes virtuales
        log.info("Eliminando los bridges LAN1 y LAN2")
        subprocess.call(["sudo", "ifconfig", "LAN1", "down"]) # -> Desactivamos el bridge LAN1
        subprocess.call(["sudo", "ifconfig", "LAN2", "down"]) # -> Desactivamos el bridge LAN2
        subprocess.call(["sudo", "ovs-vsctl", "del-br", "LAN1"]) # -> Eliminamos el bridge LAN1
        log.debug("Bridge LAN1 eliminado")
        subprocess.call(["sudo", "ovs-vsctl", "del-br", "LAN2"]) # -> Eliminamos el bridge LAN2
        log.debug("Bridge LAN2 eliminado")
        log.info("Bridges LAN1 y LAN2 eliminados correctamente")
