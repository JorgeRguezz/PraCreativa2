# Dockerfile para ProductPage
FROM python:3.7.7-slim

ENV GROUP_NUMBER=16
EXPOSE 9080

# Instalamos dependencias del requirements
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/CDPS-ETSIT/practica_creativa2.git
RUN apt-get update
RUN apt-get install -y python3-pip
WORKDIR practica_creativa2/bookinfo/src/productpage
RUN pip3 install -r requirements.txt


# Cambiamos el título y ejecutamos la aplicación con el script productpage_monolith.py
WORKDIR /practica_creativa2/bookinfo/src/productpage/templates
CMD sed -i "s/{{ product.title }}/{{ product.title }} ${GROUP_NUMBER}/g" productpage.html && \
    python3 /practica_creativa2/bookinfo/src/productpage/productpage.py 9080