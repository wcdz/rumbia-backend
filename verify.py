#!/usr/bin/env python3
"""
Script de verificación para RumbIA Backend
Verifica que todos los componentes estén funcionando correctamente
"""
import sys
import importlib.util

def check_imports():
    """Verificar que todas las importaciones funcionen"""
    print("🔍 Verificando importaciones...")
    
    try:
        # Verificar FastAPI
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
        
        # Verificar Uvicorn
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__}")
        
        # Verificar Pydantic
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__}")
        
        # Verificar la aplicación principal
        from app.main import app
        print("✅ Aplicación principal")
        
        # Verificar router de RumbIA
        from app.api.v1.rumbia import router
        print(f"✅ Router RumbIA ({len(router.routes)} endpoints)")
        
        # Verificar configuración
        from app.core.config import settings
        print(f"✅ Configuración cargada - {settings.APP_NAME}")
        
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def check_endpoints():
    """Verificar que los endpoints estén definidos correctamente"""
    print("\n🎯 Verificando endpoints...")
    
    try:
        from app.api.v1.rumbia import router
        
        routes = [route for route in router.routes if hasattr(route, 'methods')]
        endpoint_count = len(routes)
        
        print(f"✅ {endpoint_count} endpoints de RumbIA configurados")
        
        for route in routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                methods = ', '.join(route.methods)
                print(f"  📡 {methods} {route.path}")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando endpoints: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🤖 RumbIA Backend - Verificación del Sistema")
    print("=" * 50)
    
    success = True
    
    # Verificar Python
    print(f"🐍 Python {sys.version.split()[0]}")
    
    # Verificar importaciones
    success &= check_imports()
    
    # Verificar endpoints
    success &= check_endpoints()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡Todo está listo! RumbIA Backend está funcionando correctamente.")
        print("\n📚 Para iniciar el servidor:")
        print("   python run.py")
        print("   # o")
        print("   uvicorn app.main:app --reload")
        print("\n🌐 Documentación disponible en:")
        print("   http://localhost:8000/docs (Swagger)")
        print("   http://localhost:8000/redoc (ReDoc)")
    else:
        print("❌ Se encontraron problemas. Revisa los errores anteriores.")
        sys.exit(1)

if __name__ == "__main__":
    main()
