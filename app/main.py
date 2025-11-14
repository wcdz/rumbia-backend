"""
Aplicación principal FastAPI - RumbIA Backend
Orquestador de servicios para el agente inteligente RumbIA
"""
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import logging
import sys
from datetime import datetime

# Importaciones locales
from app.core.config import get_settings
from app.api.v1 import rumbia


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Obtener configuración
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor del ciclo de vida de la aplicación
    """
    # Startup
    logger.info("🚀 Iniciando RumbIA Backend...")
    logger.info(f"📡 Versión: {settings.APP_VERSION}")
    logger.info(f"🌐 Modo Debug: {settings.DEBUG}")
    logger.info("✅ RumbIA Backend iniciado correctamente")
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando RumbIA Backend...")
    logger.info("✅ RumbIA Backend cerrado correctamente")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Middleware de host confiable
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # En producción, especificar hosts específicos
)


# Manejadores de excepciones personalizados
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Manejador de errores de validación"""
    logger.error(f"Error de validación: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Error de validación",
            "message": "Los datos proporcionados no son válidos",
            "details": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """Manejador de excepciones HTTP"""
    logger.error(f"Error HTTP: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"Error {exc.status_code}",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Manejador general de excepciones"""
    logger.error(f"Error interno del servidor: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Error interno del servidor",
            "message": "Ha ocurrido un error inesperado",
            "timestamp": datetime.now().isoformat()
        }
    )


# Endpoints de la aplicación principal
@app.get(
    "/",
    tags=["Root"],
    summary="Endpoint raíz de la API",
    description="Endpoint principal que proporciona información sobre la API"
)
async def root():
    """Endpoint raíz de la aplicación"""
    return {
        "message": "¡Bienvenido a RumbIA Backend! 🤖",
        "description": "API orquestadora de servicios para el agente inteligente RumbIA",
        "version": settings.APP_VERSION,
        "status": "active",
        "timestamp": datetime.now(),
        "docs_url": "/docs",
        "api_v1": "/api/v1"
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Estado de salud de la API",
    description="Verificar el estado de salud y disponibilidad de la API"
)
async def health_check():
    """Verificar el estado de salud de la aplicación"""
    return {
        "status": "healthy",
        "message": "RumbIA Backend funcionando correctamente",
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(),
        "uptime": "Sistema operativo"
    }


# Incluir routers de la API
app.include_router(
    rumbia.router,
    prefix=settings.API_V1_PREFIX,
    tags=["RumbIA v1"]
)


# Información adicional en el arranque
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"🔧 Configuración cargada:")
    logger.info(f"   - Host: {settings.HOST}")
    logger.info(f"   - Puerto: {settings.PORT}")
    logger.info(f"   - Debug: {settings.DEBUG}")
    logger.info(f"   - Reload: {settings.RELOAD}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
