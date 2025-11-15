#!/bin/bash
# Script de despliegue rápido para RumbIA Backend en GCP Cloud Run
# Uso: ./deploy.sh PROJECT_ID [REGION]

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

# Verificar argumentos
if [ -z "$1" ]; then
    echo -e "${RED}Error: Debes proporcionar el PROJECT_ID${NC}"
    echo "Uso: ./deploy.sh PROJECT_ID [REGION]"
    echo "Ejemplo: ./deploy.sh mi-proyecto-123 us-central1"
    exit 1
fi

PROJECT_ID=$1
REGION=${2:-us-central1}  # Región por defecto: us-central1
SERVICE_NAME="rumbia-backend"

echo -e "${GREEN}🚀 Iniciando despliegue de RumbIA Backend${NC}"
echo -e "Proyecto: ${YELLOW}$PROJECT_ID${NC}"
echo -e "Región: ${YELLOW}$REGION${NC}"
echo ""

# Configurar proyecto
echo -e "${GREEN}📋 Configurando proyecto...${NC}"
gcloud config set project $PROJECT_ID

# Habilitar APIs necesarias
echo -e "${GREEN}🔌 Habilitando APIs necesarias...${NC}"
gcloud services enable run.googleapis.com \
    containerregistry.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com

# Obtener número de proyecto
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Dar permisos a Cloud Build
echo -e "${GREEN}🔐 Configurando permisos...${NC}"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin" \
  --no-user-output-enabled

gcloud iam service-accounts add-iam-policy-binding \
  ${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser" \
  --no-user-output-enabled

# Construir y desplegar
echo -e "${GREEN}🐳 Construyendo imagen Docker...${NC}"
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .

# Configurar autenticación de Docker
echo -e "${GREEN}🔑 Configurando autenticación...${NC}"
gcloud auth configure-docker --quiet

# Subir imagen
echo -e "${GREEN}📤 Subiendo imagen a Container Registry...${NC}"
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest

# Desplegar en Cloud Run
echo -e "${GREEN}🚢 Desplegando en Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars DEBUG=False,HOST=0.0.0.0,PORT=8080

# Obtener la URL del servicio
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")

echo ""
echo -e "${GREEN}✅ ¡Despliegue completado exitosamente!${NC}"
echo ""
echo -e "🌐 URL del servicio: ${YELLOW}$SERVICE_URL${NC}"
echo -e "📚 Documentación API: ${YELLOW}$SERVICE_URL/docs${NC}"
echo -e "💚 Health check: ${YELLOW}$SERVICE_URL/health${NC}"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE:${NC} Recuerda configurar las variables de entorno sensibles usando Secret Manager"
echo "Ver DEPLOYMENT_GUIDE.md para más información"

