# Usa la imagen base de Python oficial
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos e instálalos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia todo el código fuente al contenedor
COPY . .

# Comando para ejecutar la aplicación, usando el Procfile
CMD gunicorn --bind :$PORT main:app
