FROM ruby:2.7.1-slim

# Indicar el puerto accesible
EXPOSE 9080

# Cambiar directorio al de /opt/microservices
# WORKDIR /opt/microservices

COPY practica_creativa2/bookinfo/src/details/details.rb /opt/microservices

# # Actualizar sistema e instalar dependencias
# RUN apt-get update \
#     && apt-get install -y git \
#     && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git /practica_creativa2


# RUN apt-get clean && apt-get update -y || (echo "Fallo en apt-get update (DETAILS)" && exit 1) \
#     && apt-get install -y git || (echo "Fallo al instalar git" && exit 1) \
#     && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git ./practica_creativa2 \
#     || echo "Fallo al clonar el repositorio, verifica la URL o el acceso" && exit 1

# RUN apt-get update -y \
#         && apt-get install -y python3-pip \
#         && apt-get install -y git \
#         && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git 

# RUN apt-get update -y \
# && apt-get install -y git \
# && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git \
# && cd practica_creativa2 

# Cambiar directorio al de /details
# WORKDIR /opt/microservices/practica_creativa2/bookinfo/src/details
WORKDIR /opt/microservices/

# Comprobar directorio
# RUN ls -la /practica_creativa2/bookinfo/src/details

# Copiar details.rb
# RUN cp details.rb /opt/microservices

# Cambiar directorio al de /opt/microservices
# WORKDIR /opt/microservices


# Especificar variables de entorno
ENV SERVICE_VERSION=v1
ENV ENABLE_EXTERNAL_BOOK_SERVICE=true

# Lanzar app en el puerto 9080
CMD ["ruby", "details.rb", "9080"]

# Indicar que se ha instalado correctamente
RUN echo "La imagen Docker de DETAILS se ha instalado correctamente"


# CODIGO DE CHAT ----------------------------------------------------------------
# FROM ruby:2.7.1-slim

# # Indicar el puerto accesible
# EXPOSE 9080

# WORKDIR /opt/microservices


# # Especificar variables de entorno
# ENV SERVICE_VERSION=v1
# ENV ENABLE_EXTERNAL_BOOK_SERVICE=true

# # Actualizar sistema e instalar dependencias
# RUN apt-get update -y \
#     && apt-get install -y git \
#     && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git ./practica_creativa2 \
#     || echo "Error al clonar el repositorio" && exit 1

# # Cambiar directorio al de details
# WORKDIR /opt/microservices/practica_creativa2/bookinfo/src/details

# # Comprobar directorio y copiar el archivo details.rb
# RUN ls -la && cp details.rb /opt/microservices

# # Cambiar directorio al de /opt/microservices
# WORKDIR /opt/microservices

# # Lanzar app en el puerto 9080
# CMD ["ruby", "details.rb", "9080"]

# # Indicar que se ha instalado correctamente
# RUN echo "La imagen Docker de DETAILS se ha instalado correctamente"
