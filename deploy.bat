@echo off
REM Script de despliegue rápido para RumbIA Backend en GCP Cloud Run (Windows)
REM Uso: deploy.bat PROJECT_ID [REGION]

setlocal

REM Verificar argumentos
if "%~1"=="" (
    echo Error: Debes proporcionar el PROJECT_ID
    echo Uso: deploy.bat PROJECT_ID [REGION]
    echo Ejemplo: deploy.bat mi-proyecto-123 us-central1
    exit /b 1
)

set PROJECT_ID=%1
set REGION=%2
if "%REGION%"=="" set REGION=us-central1
set SERVICE_NAME=rumbia-backend

echo ================================
echo  Iniciando despliegue de RumbIA Backend
echo ================================
echo Proyecto: %PROJECT_ID%
echo Region: %REGION%
echo.

REM Configurar proyecto
echo [1/8] Configurando proyecto...
call gcloud config set project %PROJECT_ID%

REM Habilitar APIs necesarias
echo [2/8] Habilitando APIs necesarias...
call gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com

REM Obtener número de proyecto
echo [3/8] Obteniendo información del proyecto...
for /f %%i in ('gcloud projects describe %PROJECT_ID% --format="value(projectNumber)"') do set PROJECT_NUMBER=%%i

REM Dar permisos a Cloud Build
echo [4/8] Configurando permisos...
call gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%PROJECT_NUMBER%@cloudbuild.gserviceaccount.com" --role="roles/run.admin" --no-user-output-enabled
call gcloud iam service-accounts add-iam-policy-binding %PROJECT_NUMBER%-compute@developer.gserviceaccount.com --member="serviceAccount:%PROJECT_NUMBER%@cloudbuild.gserviceaccount.com" --role="roles/iam.serviceAccountUser" --no-user-output-enabled

REM Construir imagen
echo [5/8] Construyendo imagen Docker...
call docker build -t gcr.io/%PROJECT_ID%/%SERVICE_NAME%:latest .

REM Configurar autenticación
echo [6/8] Configurando autenticación...
call gcloud auth configure-docker --quiet

REM Subir imagen
echo [7/8] Subiendo imagen a Container Registry...
call docker push gcr.io/%PROJECT_ID%/%SERVICE_NAME%:latest

REM Desplegar
echo [8/8] Desplegando en Cloud Run...
call gcloud run deploy %SERVICE_NAME% --image gcr.io/%PROJECT_ID%/%SERVICE_NAME%:latest --platform managed --region %REGION% --allow-unauthenticated --memory 512Mi --cpu 1 --max-instances 10 --timeout 300 --set-env-vars DEBUG=False,HOST=0.0.0.0,PORT=8080

REM Obtener URL
for /f %%i in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --format="value(status.url)"') do set SERVICE_URL=%%i

echo.
echo ================================
echo  Despliegue completado exitosamente
echo ================================
echo.
echo URL del servicio: %SERVICE_URL%
echo Documentacion API: %SERVICE_URL%/docs
echo Health check: %SERVICE_URL%/health
echo.
echo IMPORTANTE: Recuerda configurar las variables de entorno sensibles usando Secret Manager
echo Ver DEPLOYMENT_GUIDE.md para mas informacion

endlocal

