"""
Router principal de RumbIA - Agente Inteligente
"""
from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Dict, Any, Optional

from app.services import PolizaService

router = APIRouter(prefix="/rumbia", tags=["RumbIA"])


class RumbiaResponse(BaseModel):
    """Modelo de respuesta de RumbIA"""
    message: str
    agent_name: str
    timestamp: datetime
    status: str


class HealthResponse(BaseModel):
    """Modelo de respuesta de salud del servicio"""
    status: str
    message: str
    timestamp: datetime
    version: str


# Modelos para Emisión de Póliza
class ClienteData(BaseModel):
    """Modelo de datos del cliente"""
    dni: str = Field(..., description="DNI del cliente")
    nombre: str = Field(..., description="Nombre completo del cliente")
    fechaNacimiento: date = Field(..., description="Fecha de nacimiento del cliente")
    genero: str = Field(..., description="Género del cliente (M/F)")
    telefono: str = Field(..., description="Teléfono del cliente")
    correo: EmailStr = Field(..., description="Correo electrónico del cliente")


class ParametrosCotizacion(BaseModel):
    """Modelo de parámetros de cotización"""
    edad_actuarial: int = Field(..., description="Edad actuarial del cliente")
    sexo: str = Field(..., description="Sexo del cliente (M/F)")
    prima: float = Field(..., description="Prima mensual")


class CotizacionData(BaseModel):
    """Modelo de datos de cotización"""
    producto: str = Field(..., description="Nombre del producto")
    parametros: ParametrosCotizacion = Field(..., description="Parámetros de la cotización")
    id: int = Field(..., description="ID de la cotización")
    fecha_creacion: datetime = Field(..., description="Fecha de creación de la cotización")
    porcentaje_devolucion: float = Field(..., description="Porcentaje de devolución")
    tasa_implicita: float = Field(..., description="Tasa implícita")
    suma_asegurada: float = Field(..., description="Suma asegurada")
    devolucion: float = Field(..., description="Monto de devolución")
    prima_anual: float = Field(..., description="Prima anual")
    tabla_devolucion: str = Field(..., description="Tabla de devolución en formato string")


class EmisionPolizaRequest(BaseModel):
    """Modelo de request para emisión de póliza"""
    cliente: ClienteData = Field(..., description="Datos del cliente")
    cotizacion: CotizacionData = Field(..., description="Datos de la cotización")


class EmisionPolizaResponse(BaseModel):
    """Modelo de respuesta de emisión de póliza"""
    status: str = Field(..., description="Estado de la emisión")
    message: str = Field(..., description="Mensaje de respuesta")
    numero_poliza: Optional[str] = Field(None, description="Número de póliza generado")
    id_poliza: int = Field(..., description="ID de la póliza")
    archivo_poliza: str = Field(..., description="Nombre del archivo de póliza generado")
    documento_generado: bool = Field(False, description="Indica si se generó el documento")
    ruta_documento_word: Optional[str] = Field(None, description="Ruta del documento Word generado")
    ruta_documento_pdf: Optional[str] = Field(None, description="Ruta del documento PDF generado")
    fecha_emision: datetime = Field(..., description="Fecha y hora de emisión")
    cliente: ClienteData = Field(..., description="Datos del cliente")
    cotizacion: CotizacionData = Field(..., description="Datos de la cotización")


@router.get(
    "/saludo",
    response_model=RumbiaResponse,
    status_code=status.HTTP_200_OK,
    summary="Saludo del agente RumbIA",
    description="Endpoint que devuelve un saludo personalizado del agente inteligente RumbIA"
)
async def saludo_rumbia() -> RumbiaResponse:
    """
    Endpoint principal que devuelve el saludo de RumbIA
    
    Returns:
        RumbiaResponse: Respuesta con el saludo del agente
    """
    return RumbiaResponse(
        message="¡Hola! Soy tu agente inteligente RumbIA 🤖",
        agent_name="RumbIA",
        timestamp=datetime.now(),
        status="active"
    )


@router.get(
    "/",
    response_model=RumbiaResponse,
    status_code=status.HTTP_200_OK,
    summary="Endpoint raíz de RumbIA",
    description="Endpoint principal que presenta al agente RumbIA"
)
async def root_rumbia() -> RumbiaResponse:
    """
    Endpoint raíz de RumbIA
    
    Returns:
        RumbiaResponse: Respuesta de presentación del agente
    """
    return RumbiaResponse(
        message="Soy RumbIA, tu agente inteligente. ¿En qué puedo ayudarte hoy?",
        agent_name="RumbIA",
        timestamp=datetime.now(),
        status="ready"
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Estado de salud del agente RumbIA",
    description="Verificar el estado de salud y disponibilidad del agente RumbIA"
)
async def health_check() -> HealthResponse:
    """
    Verificar el estado de salud del servicio RumbIA
    
    Returns:
        HealthResponse: Estado actual del servicio
    """
    return HealthResponse(
        status="healthy",
        message="RumbIA está funcionando correctamente",
        timestamp=datetime.now(),
        version="1.0.0"
    )


@router.get(
    "/info",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Información del agente RumbIA",
    description="Obtener información detallada sobre las capacidades del agente RumbIA"
)
async def info_rumbia() -> Dict[str, Any]:
    """
    Obtener información sobre el agente RumbIA
    
    Returns:
        Dict: Información detallada del agente
    """
    return {
        "agent_name": "RumbIA",
        "version": "1.0.0",
        "type": "Agente Inteligente Orquestador",
        "description": "Agente inteligente diseñado para orquestar servicios y asistir a los usuarios",
        "capabilities": [
            "Orquestación de servicios",
            "Procesamiento de lenguaje natural",
            "Asistencia inteligente",
            "Integración de APIs"
        ],
        "status": "active",
        "created_at": datetime.now(),
        "last_update": datetime.now()
    }


@router.post(
    "/emision-poliza",
    response_model=EmisionPolizaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Emisión de póliza de seguro",
    description="Endpoint para emitir una nueva póliza de seguro con los datos del cliente y la cotización"
)
async def emision_poliza(request: EmisionPolizaRequest) -> EmisionPolizaResponse:
    """
    Emisión de póliza de seguro
    
    Este endpoint procesa la emisión de una nueva póliza de seguro a partir de:
    - Datos del cliente (DNI, nombre, fecha de nacimiento, género, teléfono, correo)
    - Datos de la cotización (producto, parámetros, suma asegurada, etc.)
    
    Genera un archivo JSON en la carpeta db con formato RumbIA###.json
    
    Args:
        request: Datos del cliente y cotización para emitir la póliza
    
    Returns:
        EmisionPolizaResponse: Respuesta con el estado de la emisión y número de póliza
    """
    # Inicializar el servicio
    poliza_service = PolizaService()
    
    # Preparar datos del cliente
    datos_cliente = {
        "dni": request.cliente.dni,
        "nombre": request.cliente.nombre,
        "fechaNacimiento": request.cliente.fechaNacimiento.isoformat(),
        "genero": request.cliente.genero,
        "telefono": request.cliente.telefono,
        "correo": request.cliente.correo
    }
    
    # Preparar datos de cotización
    datos_cotizacion = {
        "producto": request.cotizacion.producto,
        "parametros": {
            "edad_actuarial": request.cotizacion.parametros.edad_actuarial,
            "sexo": request.cotizacion.parametros.sexo,
            "prima": request.cotizacion.parametros.prima
        },
        "id": request.cotizacion.id,
        "fecha_creacion": request.cotizacion.fecha_creacion.isoformat(),
        "porcentaje_devolucion": request.cotizacion.porcentaje_devolucion,
        "tasa_implicita": request.cotizacion.tasa_implicita,
        "suma_asegurada": request.cotizacion.suma_asegurada,
        "devolucion": request.cotizacion.devolucion,
        "prima_anual": request.cotizacion.prima_anual,
        "tabla_devolucion": request.cotizacion.tabla_devolucion
    }
    
    # Delegar al servicio la emisión de la póliza
    resultado = poliza_service.emitir_poliza(
        datos_cliente=datos_cliente,
        datos_cotizacion=datos_cotizacion,
        generar_documento=True  # Habilitado para generar PDF
    )
    
    # Construir mensaje de respuesta
    mensaje = f"Póliza emitida exitosamente para {request.cliente.nombre}"
    if resultado["documento_generado"]:
        if resultado["ruta_documento_pdf"]:
            mensaje += " - Documento PDF generado correctamente"
        else:
            mensaje += " - Documento generado (PDF no disponible)"
    
    # Construir y retornar la respuesta
    return EmisionPolizaResponse(
        status="success",
        message=mensaje,
        numero_poliza=resultado["numero_poliza"],
        id_poliza=resultado["id_poliza"],
        archivo_poliza=resultado["nombre_archivo"],
        documento_generado=resultado["documento_generado"],
        ruta_documento_word=resultado["ruta_documento_word"],
        ruta_documento_pdf=resultado["ruta_documento_pdf"],
        fecha_emision=resultado["fecha_emision"],
        cliente=request.cliente,
        cotizacion=request.cotizacion
    )
