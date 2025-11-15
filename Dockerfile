# Dockerfile para RumbIA Backend - Optimizado para GCP Cloud Run
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para docx2pdf, python-docx y html2image
RUN apt-get update && apt-get install -y \
    libreoffice \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno para Chromium (html2image)
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMIUM_FLAGS="--no-sandbox --disable-dev-shm-usage --headless"

# Copiar archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/db/documentos

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8080

# Cloud Run establece automáticamente la variable PORT a 8080
ENV PORT=8080
ENV HOST=0.0.0.0

# Comando para ejecutar la aplicación
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 1

