#!/usr/bin/env python3
"""
Script de arranque para RumbIA Backend
Facilita el inicio de la aplicación con configuración predeterminada
"""
import os
import sys
import uvicorn
from app.core.config import get_settings

def main():
    """Función principal para iniciar la aplicación"""
    settings = get_settings()
    
    print("🤖 Iniciando RumbIA Backend...")
    print(f"📡 Versión: {settings.APP_VERSION}")
    print(f"🌐 Host: {settings.HOST}:{settings.PORT}")
    print(f"🔧 Modo Debug: {settings.DEBUG}")
    print("📚 Documentación disponible en:")
    print(f"   - Swagger UI: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"   - ReDoc: http://{settings.HOST}:{settings.PORT}/redoc")
    print()
    
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.RELOAD,
            log_level=settings.LOG_LEVEL.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo RumbIA Backend...")
        print("✅ ¡Hasta pronto!")
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
