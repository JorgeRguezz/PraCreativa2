# ------- Pt. 2 - DOCKERFILE ----------------------------------

# Usar la imagen base de Python 3.7.7
FROM python:3.7.7-slim

# Exponer el puerto 5080 (el que se pide en el enunciado)
EXPOSE 5080

# Definir la variable de entorno GROUP_NUM (se pasará al ejecutar el contenedor)
ENV GROUP_NUM=16

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /home

# Instalar las dependencias necesarias para la aplicación
RUN apt-get update -y \
        && apt-get install -y python3-pip \
        && apt-get install -y git \
        && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git \
        && cd practica_creativa2/bookinfo/src/productpage/ \
        && pip3 install -r requirements.txt

# Cambiar el título de la app y lanzar app en el puerto 5080
# CMD find ./ -type f -exec sed -i "s/Simple Bookstore App/GRUPO$GROUP_NUM/g" {} \; \
#     && python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 5080
CMD find ./ -type f -exec sed -i "s/Simple Bookstore App/GRUPO: ${GROUP_NUM}/g" {} + \
    && python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 5080


# Indicar que se ha instalado correctamente
RUN echo "La imagen Docker se ha configurado correctamente"

