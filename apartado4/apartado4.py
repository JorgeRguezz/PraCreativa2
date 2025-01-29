import os
import sys

def build(version):
    
    # Descargar las imágenes de Docker Hub
    os.system('sudo docker pull jorgerguezz/details:16')
    os.system('sudo docker pull jorgerguezz/productpage:16')
    os.system('sudo docker pull jorgerguezz/reviews:16')
    os.system('sudo docker pull jorgerguezz/ratings:16')
    
    # Crear los archivos de despliegue
    os.system('gcloud container clusters get-credentials autopilot-cluster-1 --region europe-southwest1 --project pcreatica2')
    os.system('kubectl apply -f productpage.yaml')
    os.system('kubectl apply -f ratings.yaml')
    os.system('kubectl apply -f details.yaml')
    os.system('kubectl apply -f reviews-svc.yaml')
    os.system(f'kubectl apply -f reviews-{version}-deployment.yaml')

def delete():
    os.system('kubectl delete --all deployments && kubectl delete --all pods && kubectl delete --all services')

param = sys.argv

if len(param) < 2:
    print("Usage: python3 bloque4.py [build|delete] [version]")
    sys.exit(1)

command = param[1]

if command == "construir":
    if len(param) < 3:
        print("Especifica la versión(e.g., v1, v2, v3)")
        sys.exit(1)
    version = param[2]
    build(version)
elif command == "borrar":
    delete()
else:
    print("Comando desconocido")