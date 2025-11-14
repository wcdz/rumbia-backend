"""
Utilidades para generación de documentos
"""
import json
from pathlib import Path
from app.services import GenerateDocumentService


def generar_documento_desde_json(ruta_json: str) -> str:
    """
    Genera un documento Word desde un archivo JSON de póliza
    
    Args:
        ruta_json: Ruta al archivo JSON de la póliza
        
    Returns:
        str: Ruta del documento generado
    """
    # Leer el JSON
    with open(ruta_json, 'r', encoding='utf-8') as f:
        datos_poliza = json.load(f)
    
    # Generar el documento
    servicio = GenerateDocumentService()
    ruta_documento = servicio.generar_documento(datos_poliza)
    
    return ruta_documento


def generar_documentos_todas_polizas(directorio_db: str = "db") -> list:
    """
    Genera documentos para todas las pólizas en el directorio db
    
    Args:
        directorio_db: Ruta al directorio con los archivos JSON
        
    Returns:
        list: Lista de rutas de documentos generados
    """
    db_path = Path(directorio_db)
    documentos_generados = []
    
    # Buscar todos los archivos JSON de pólizas
    for json_file in db_path.glob("RumbIA*.json"):
        try:
            ruta_documento = generar_documento_desde_json(str(json_file))
            documentos_generados.append(ruta_documento)
            print(f"✅ Documento generado: {ruta_documento}")
        except Exception as e:
            print(f"❌ Error al generar documento para {json_file}: {e}")
    
    return documentos_generados

