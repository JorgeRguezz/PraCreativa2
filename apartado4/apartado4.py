#!usr/bin/python3
import os

#Instalacion de Minikube
os.system('sudo apt-get update -y')
os.system('sudo apt install -y curl wget apt-transport-https')
os.system('sudo apt install virtualbox virtualbox-ext-pack')


# 


#Descarga las imagenes del repositorio Docker Hub
os.system('sudo docker pull jorgerguezz/details:latest')
os.system('sudo docker pull jorgerguezz/productpage:latest')
os.system('sudo docker pull jorgerguezz/reviews2:latest')
os.system('sudo docker pull jorgerguezz/ratings:latest')

#Configuracion para usar Docker con Kubernetes
os.system('sudo apt-get remove docker docker-engine docker.io containerd runc')
os.system('sudo apt-get update')
os.system('sudo apt-get install -y ca-certificates curl gnupg lsb-release')
os.system('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg')
os.system('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
os.system('sudo apt-get update')
os.system('sudo apt-get install -y docker-ce docker-ce-cli containerd.io')

#Establece el proyecto de Google Cloud Platform y habilita el servicio de Kubernetes Engine en Google Cloud Platform
os.system('sudo gcloud config set project pcreatica2')     # Se pone el ID del proyecto (en este caso es pract-creat-2) 
os.system('sudo gcloud services enable container.googleapis.com')


# Crea los pods a partir de los archivos de configuracion .yaml (sino funciona añadir --disk-size=20)
os.system('sudo gcloud container clusters create clusterkubernetes --num-nodes=3 --zone=europe-southwest1 --no-enable-autoscaling') 
# os.system('sudo gcloud container clusters get-credentials autopilot-cluster-1 --region europe-southwest1 --project pcreatica2') 


os.system('sudo kubectl apply -f productpage.yaml')
os.system('sudo kubectl apply -f details.yaml')
os.system('sudo kubectl apply -f ratings.yaml')
os.system('sudo kubectl apply -f reviews-service.yaml')

# Se puede elegir la version que queramos 
#os.system('sudo kubectl apply -f reviews-v1-deployment.yaml')
#os.system('sudo kubectl apply -f reviews-v2-deployment.yaml')
os.system('sudo kubectl apply -f reviews-v3-deployment.yaml')

# Lanzamos el servicio
os.system('sudo kubectl expose deployment productpage --type=LoadBalancer --port=9080')