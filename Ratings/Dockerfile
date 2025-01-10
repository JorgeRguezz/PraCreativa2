FROM node:12.18.1-slim

# Indicar el puerto accesible
EXPOSE 9080


ENV SERVICE_VERSION=v1

# Cambiar directorio al de /opt/microservices
WORKDIR /opt/microservices

# # Actualizar sistema e instalar dependencias
# RUN apt-get update && apt-get install -y git \
#     && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git /practica_creativa2

# RUN apt-get clean && apt-get update -y || (echo "Fallo en apt-get update (RATINGS)" && exit 1) \
#     && apt-get install -y git || (echo "Fallo al instalar git" && exit 1) \
#     && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git ./practica_creativa2 \
#     || echo "Fallo al clonar el repositorio, verifica la URL o el acceso" && exit 1

# RUN apt-get update -y \
# && apt-get install -y git \
# && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git \
# && cd practica_creativa2 

RUN apt-get update -y \
        && apt-get install -y python3-pip \
        && apt-get install -y git \
        && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git \
        && cd practica_creativa2


# Cambiar directorio al de /ratings
WORKDIR /practica_creativa2/bookinfo/src/ratings/

# Copiar package.json y ratings.json
RUN cp package.json /opt/microservices \
    && cp ratings.js /opt/microservices

# Cambiar directorio al de /opt/microservices
WORKDIR /opt/microservices

# Instalar app
RUN npm install

# Lanzar app en el puerto 9080
CMD ["node", "ratings.js", "9080"]

# Indicar que se ha instalado correctamente
RUN echo "La imagen Docker de RATINGS se ha instalado correctamente"
