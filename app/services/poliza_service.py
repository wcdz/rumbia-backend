"""
Servicio de Emisión de Pólizas
Contiene toda la lógica de negocio relacionada con la emisión de pólizas
"""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Directorio donde se guardarán las pólizas
DB_DIR = Path(__file__).parent.parent.parent / "db"


class PolizaService:
    """
    Servicio para gestionar la emisión de pólizas
    """
    
    @staticmethod
    def obtener_siguiente_id_poliza() -> int:
        """
        Obtiene el siguiente ID de póliza disponible.
        Busca los archivos existentes en la carpeta db con formato RumbIA###.json
        
        Returns:
            int: El siguiente ID disponible
        """
        # Asegurar que el directorio existe
        DB_DIR.mkdir(parents=True, exist_ok=True)
        
        # Buscar archivos con el patrón RumbIA###.json
        archivos = list(DB_DIR.glob("RumbIA*.json"))
        
        if not archivos:
            return 1
        
        # Extraer los IDs de los nombres de archivo
        ids = []
        patron = re.compile(r'RumbIA(\d+)\.json')
        
        for archivo in archivos:
            match = patron.match(archivo.name)
            if match:
                ids.append(int(match.group(1)))
        
        if not ids:
            return 1
        
        return max(ids) + 1
    
    @staticmethod
    def generar_numero_poliza(id_poliza: int, fecha: datetime) -> str:
        """
        Genera el número de póliza con formato POL-AAAAMMDD-HHMMSS-###
        
        Args:
            id_poliza: ID de la póliza
            fecha: Fecha de emisión
            
        Returns:
            str: Número de póliza generado
        """
        return f"POL-{fecha.strftime('%Y%m%d-%H%M%S')}-{id_poliza:03d}"
    
    @staticmethod
    def generar_nombre_archivo(id_poliza: int) -> str:
        """
        Genera el nombre del archivo de póliza
        
        Args:
            id_poliza: ID de la póliza
            
        Returns:
            str: Nombre del archivo (RumbIA###.json)
        """
        return f"RumbIA{id_poliza:03d}.json"
    
    @staticmethod
    def preparar_datos_poliza(
        id_poliza: int,
        numero_poliza: str,
        fecha_emision: datetime,
        datos_cliente: Dict[str, Any],
        datos_cotizacion: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepara los datos de la póliza para guardar en JSON
        
        Args:
            id_poliza: ID de la póliza
            numero_poliza: Número de póliza
            fecha_emision: Fecha de emisión
            datos_cliente: Datos del cliente
            datos_cotizacion: Datos de la cotización
            
        Returns:
            Dict: Datos estructurados de la póliza
        """
        return {
            "id_poliza": id_poliza,
            "numero_poliza": numero_poliza,
            "fecha_emision": fecha_emision.isoformat(),
            "cliente": {
                "dni": datos_cliente["dni"],
                "nombre": datos_cliente["nombre"],
                "fechaNacimiento": datos_cliente["fechaNacimiento"],
                "genero": datos_cliente["genero"],
                "telefono": datos_cliente["telefono"],
                "correo": datos_cliente["correo"]
            },
            "cotizacion": {
                "producto": datos_cotizacion["producto"],
                "parametros": {
                    "edad_actuarial": datos_cotizacion["parametros"]["edad_actuarial"],
                    "sexo": datos_cotizacion["parametros"]["sexo"],
                    "prima": datos_cotizacion["parametros"]["prima"]
                },
                "id": datos_cotizacion["id"],
                "fecha_creacion": datos_cotizacion["fecha_creacion"],
                "porcentaje_devolucion": datos_cotizacion["porcentaje_devolucion"],
                "tasa_implicita": datos_cotizacion["tasa_implicita"],
                "suma_asegurada": datos_cotizacion["suma_asegurada"],
                "devolucion": datos_cotizacion["devolucion"],
                "prima_anual": datos_cotizacion["prima_anual"],
                "tabla_devolucion": datos_cotizacion["tabla_devolucion"]
            },
            "status": "activa"
        }
    
    @staticmethod
    def guardar_poliza_json(nombre_archivo: str, datos_poliza: Dict[str, Any]) -> Path:
        """
        Guarda la póliza en un archivo JSON
        
        Args:
            nombre_archivo: Nombre del archivo
            datos_poliza: Datos de la póliza
            
        Returns:
            Path: Ruta completa del archivo guardado
        """
        ruta_archivo = DB_DIR / nombre_archivo
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_poliza, f, ensure_ascii=False, indent=2)
        
        return ruta_archivo
    
    def emitir_poliza(
        self,
        datos_cliente: Dict[str, Any],
        datos_cotizacion: Dict[str, Any],
        generar_documento: bool = True
    ) -> Dict[str, Any]:
        """
        Proceso completo de emisión de póliza
        
        Args:
            datos_cliente: Datos del cliente
            datos_cotizacion: Datos de la cotización
            generar_documento: Si se debe generar el documento Word (default: True)
            
        Returns:
            Dict: Información de la póliza emitida
        """
        # 1. Obtener el siguiente ID de póliza
        id_poliza = self.obtener_siguiente_id_poliza()
        
        # 2. Generar fecha actual
        fecha_actual = datetime.now()
        
        # 3. Generar número de póliza
        numero_poliza = self.generar_numero_poliza(id_poliza, fecha_actual)
        
        # 4. Generar nombre del archivo
        nombre_archivo = self.generar_nombre_archivo(id_poliza)
        
        # 5. Preparar datos de la póliza
        datos_poliza = self.preparar_datos_poliza(
            id_poliza=id_poliza,
            numero_poliza=numero_poliza,
            fecha_emision=fecha_actual,
            datos_cliente=datos_cliente,
            datos_cotizacion=datos_cotizacion
        )
        
        # 6. Guardar póliza en JSON
        ruta_archivo = self.guardar_poliza_json(nombre_archivo, datos_poliza)
        
        resultado = {
            "id_poliza": id_poliza,
            "numero_poliza": numero_poliza,
            "nombre_archivo": nombre_archivo,
            "fecha_emision": fecha_actual,
            "ruta_archivo": str(ruta_archivo),
            "documento_generado": False,
            "ruta_documento_word": None,
            "ruta_documento_pdf": None
        }
        
        # 7. Generar documento PDF (elimina el Word automáticamente)
        if generar_documento:
            try:
                from .generate_document_service import GenerateDocumentService
                doc_service = GenerateDocumentService()
                ruta_word, ruta_pdf = doc_service.generar_documento(
                    datos_poliza, 
                    generar_pdf=True, 
                    solo_pdf=True  # Solo mantener el PDF, eliminar el Word
                )
                resultado["documento_generado"] = True
                resultado["ruta_documento_word"] = None  # No se guarda el Word
                resultado["ruta_documento_pdf"] = ruta_pdf
            except Exception as e:
                print(f"⚠️ No se pudo generar el documento: {e}")
                # No falla la emisión si no se puede generar el documento
        
        # 8. Aquí se pueden agregar más acciones:
        # - Enviar notificaciones al cliente
        # - Integrar con sistemas externos
        # - Registrar en base de datos
        # - Enviar a cola de procesamiento
        
        return resultado

