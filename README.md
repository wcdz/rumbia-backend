# 🤖 RumbIA Backend

Backend orquestador de servicios para RumbIA - Tu Agente Inteligente

## 📋 Descripción

RumbIA Backend es una API REST construida con FastAPI que actúa como orquestador de servicios para el agente inteligente RumbIA. Diseñado siguiendo las mejores prácticas de desarrollo de software, este backend proporciona una base sólida y escalable para integrar diversos servicios de IA y automatización.

## 🚀 Características

- **FastAPI**: Framework moderno y de alto rendimiento para APIs
- **Arquitectura Modular**: Estructura de proyecto organizada y escalable
- **Sin Base de Datos**: Diseñado como orquestador de servicios
- **Documentación Automática**: Swagger UI y ReDoc incluidos
- **Manejo de Errores**: Sistema robusto de manejo de excepciones
- **CORS Configurado**: Listo para integración con frontends
- **Logging Avanzado**: Sistema de logs estructurado
- **Configuración Flexible**: Variables de entorno configurables
- **Validación de Datos**: Pydantic para validación automática

## 📁 Estructura del Proyecto

```
rumbia-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── rumbia.py          # Router principal de RumbIA
│   ├── core/
│   │   └── config.py              # Configuración de la aplicación
│   ├── models/                    # Modelos de datos (futuro)
│   ├── services/                  # Servicios de negocio (futuro)
│   ├── utils/                     # Utilidades (futuro)
│   └── main.py                    # Aplicación principal
├── tests/                         # Tests (futuro)
├── requirements.txt               # Dependencias de Python
├── .env.example                   # Ejemplo de configuración
└── README.md                      # Este archivo
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\\Scripts\\activate
   
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Copiar el archivo de ejemplo
   cp .env.example .env
   
   # Editar .env según tus necesidades
   ```

5. **Ejecutar la aplicación**
   ```bash
   # Desde la raíz del proyecto
   python -m app.main
   
   # O usando uvicorn directamente
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🌐 Endpoints Disponibles

### Endpoints Principales

- **GET /** - Información de bienvenida de la API
- **GET /health** - Estado de salud de la aplicación

### Endpoints de RumbIA (API v1)

- **GET /api/v1/rumbia/** - Presentación del agente RumbIA
- **GET /api/v1/rumbia/saludo** - Saludo personalizado de RumbIA
- **GET /api/v1/rumbia/health** - Estado de salud del agente
- **GET /api/v1/rumbia/info** - Información detallada del agente

### 📚 Documentación Interactiva

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔧 Configuración

La aplicación se configura mediante variables de entorno. Las principales configuraciones disponibles son:

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `APP_NAME` | Nombre de la aplicación | RumbIA Backend |
| `APP_VERSION` | Versión de la aplicación | 1.0.0 |
| `HOST` | Host del servidor | 0.0.0.0 |
| `PORT` | Puerto del servidor | 8000 |
| `DEBUG` | Modo debug | true |
| `LOG_LEVEL` | Nivel de logging | INFO |
| `ALLOWED_ORIGINS` | Orígenes permitidos para CORS | ["http://localhost:3000"] |

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests (cuando estén implementados)
pytest
```

## 🚀 Despliegue

### Usando Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Usando Gunicorn + Uvicorn

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤖 Sobre RumbIA

RumbIA es un agente inteligente diseñado para asistir y automatizar tareas mediante la orquestación de diversos servicios. Este backend proporciona la infraestructura necesaria para:

- 🔗 Integrar múltiples servicios de IA
- 📊 Procesar y orquestar requests complejos
- 🛡️ Manejar autenticación y autorización
- 📈 Monitorear y loggear actividades
- 🔄 Gestionar workflows de automatización

## 📝 Próximas Funcionalidades

- [ ] Integración con servicios de IA
- [ ] Sistema de autenticación
- [ ] Métricas y monitoreo
- [ ] Tests automatizados
- [ ] Cache distribuido
- [ ] Rate limiting
- [ ] Documentación de API extendida

## 🤝 Contribución

Este proyecto sigue las mejores prácticas de desarrollo:

- Código limpio y documentado
- Arquitectura modular y escalable
- Manejo robusto de errores
- Logging estructurado
- Configuración flexible

## 📄 Licencia

[Especificar licencia aquí]

## 📞 Soporte

Para soporte y consultas sobre RumbIA Backend, [especificar canales de soporte].

---

**¡Bienvenido a RumbIA! 🤖 Tu agente inteligente está listo para ayudarte.**
