"""
Configuración de la aplicación FastAPI
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Información de la aplicación
    APP_NAME: str = Field(default="RumbIA Backend", description="Nombre de la aplicación")
    APP_VERSION: str = Field(default="1.0.0", description="Versión de la aplicación")
    DESCRIPTION: str = Field(
        default="Backend orquestador de servicios para RumbIA - Agente Inteligente",
        description="Descripción de la aplicación"
    )
    
    # Configuración del servidor
    HOST: str = Field(default="0.0.0.0", description="Host del servidor")
    PORT: int = Field(default=8000, description="Puerto del servidor")
    DEBUG: bool = Field(default=True, description="Modo debug")
    RELOAD: bool = Field(default=True, description="Auto-reload en desarrollo")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000"],
        description="Orígenes permitidos para CORS"
    )
    ALLOWED_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Métodos HTTP permitidos"
    )
    ALLOWED_HEADERS: List[str] = Field(
        default=["*"],
        description="Headers permitidos"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Nivel de logging")
    
    # API
    API_V1_PREFIX: str = Field(default="/api/v1", description="Prefijo de la API v1")
    
    # Configuración de servicios externos (para futuras implementaciones)
    EXTERNAL_SERVICE_TIMEOUT: int = Field(default=30, description="Timeout para servicios externos")
    MAX_RETRIES: int = Field(default=3, description="Máximo número de reintentos")
    
    # Configuración de Email (Hardcodeado)
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="Host del servidor SMTP")
    SMTP_PORT: int = Field(default=587, description="Puerto del servidor SMTP")
    SMTP_USER: str = Field(default="chavezdiaz4@gmail.com", description="Usuario SMTP")
    SMTP_PASSWORD: str = Field(default="utkw ykum scqp edha", description="Contraseña SMTP")
    FROM_EMAIL: str = Field(default="chavezdiaz4@gmail.com", description="Email remitente")
    FROM_NAME: str = Field(default="RumbIA | Bienvenido a Interseguro", description="Nombre remitente")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()


def get_settings() -> Settings:
    """Obtener configuración de la aplicación"""
    return settings
