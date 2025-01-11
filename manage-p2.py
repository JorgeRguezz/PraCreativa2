import logging, sys, os
# from manageLib import mv_pesada, mv_docker, mv_docker_compose, mv_kubernetes, destroy_cluster, config_cluster, docker_destroy, info_cluster
from manageLib import mv_pesada, mv_docker, docker_destroy, mv_docker_compose

def init_log():
    # Creacion y configuracion del logger
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('auto_p2')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.propagate = False

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def main():
    
    orden = sys.argv[1] # Establecer la posición de la orden en la línea de argumentos

    if orden == "parte1":
        puerto = sys.argv[2]
        mv_pesada(puerto)

    elif orden == "parte2":
        if sys.argv[2] == "start":
            mv_docker()
        elif sys.argv[2] == "destruir":
            docker_destroy()
    elif orden == "parte3":
        if sys.argv[2] == "start":
            mv_docker_compose()
        elif sys.argv[2] == "destruir":
            docker_destroy()
        
    else:
        print(f"Orden no reconocida: {orden}")

if __name__ == "__main__":
    main()