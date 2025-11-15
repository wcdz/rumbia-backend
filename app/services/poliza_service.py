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
        Genera el número de póliza con formato RumbIA###
        
        Args:
            id_poliza: ID de la póliza
            fecha: Fecha de emisión (no se usa, se mantiene por compatibilidad)
            
        Returns:
            str: Número de póliza generado (ej: RumbIA001)
        """
        return f"RumbIA{id_poliza:03d}"
    
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
        datos_cotizacion: Dict[str, Any],
        periodo_pago_primas: int = 7
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
            "periodo_pago_primas": periodo_pago_primas,
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
        generar_documento: bool = True,
        periodo_pago_primas: int = 7
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
            datos_cotizacion=datos_cotizacion,
            periodo_pago_primas=periodo_pago_primas
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
        
        # 7. Generar documento PDF (si falla, mantiene el Word)
        if generar_documento:
            try:
                from .generate_document_service import GenerateDocumentService
                doc_service = GenerateDocumentService()
                ruta_word, ruta_pdf = doc_service.generar_documento(
                    datos_poliza, 
                    generar_pdf=True, 
                    solo_pdf=False  # Mantener Word si no se puede generar PDF
                )
                resultado["documento_generado"] = True
                
                if ruta_pdf:
                    # Si se generó el PDF, usarlo y eliminar el Word
                    resultado["ruta_documento_word"] = None
                    resultado["ruta_documento_pdf"] = ruta_pdf
                    print(f"✅ PDF generado: {ruta_pdf}")
                else:
                    # Si no se generó el PDF, usar el Word
                    resultado["ruta_documento_word"] = ruta_word
                    resultado["ruta_documento_pdf"] = None
                    print(f"⚠️ PDF no disponible, usando Word: {ruta_word}")
            except Exception as e:
                print(f"⚠️ No se pudo generar el documento: {e}")
                # No falla la emisión si no se puede generar el documento
        
        # 8. Generar imagen del HTML del email
        resultado["ruta_imagen_html"] = None
        try:
            from .email_service import EmailService
            email_service = EmailService()
            html_content = email_service.generar_html_email(datos_poliza)
            
            # Convertir HTML a imagen JPEG usando html2image
            from pathlib import Path
            import os
            
            # Crear nombre de archivo para la imagen
            nombre_imagen_jpg = f"{numero_poliza}_email.jpg"
            ruta_jpg = DB_DIR / "documentos" / nombre_imagen_jpg
            
            # Convertir HTML a JPEG usando html2image
            try:
                from html2image import Html2Image
                from PIL import Image, ImageChops
                
                # Configurar html2image
                hti = Html2Image(output_path=str(DB_DIR / "documentos"))
                
                # Generar imagen desde HTML string
                hti.screenshot(
                    html_str=html_content,
                    save_as=nombre_imagen_jpg,
                    size=(800, 1200)  # Ancho x Alto en píxeles
                )
                
                # Recortar bordes negros automáticamente
                try:
                    img = Image.open(ruta_jpg)
                    
                    # Convertir a RGB si es necesario
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Convertir imagen a array para análisis más preciso
                    import numpy as np
                    img_array = np.array(img)
                    
                    # Detectar bordes no negros (píxeles con suma RGB > 30)
                    # Suma de canales RGB por píxel
                    sum_rgb = img_array.sum(axis=2)
                    
                    # Encontrar filas y columnas que no son negras
                    rows_with_content = np.where(sum_rgb.sum(axis=1) > 30 * img_array.shape[1])[0]
                    cols_with_content = np.where(sum_rgb.sum(axis=0) > 30 * img_array.shape[0])[0]
                    
                    if len(rows_with_content) > 0 and len(cols_with_content) > 0:
                        # Obtener coordenadas del contenido
                        top = rows_with_content[0]
                        bottom = rows_with_content[-1] + 1
                        left = cols_with_content[0]
                        right = cols_with_content[-1] + 1
                        
                        # Recortar la imagen
                        img_cropped = img.crop((left, top, right, bottom))
                        # Guardar imagen recortada
                        img_cropped.save(ruta_jpg, 'JPEG', quality=90)
                        print(f"✅ Imagen recortada de {img.size} a {img_cropped.size}")
                    else:
                        print(f"⚠️ No se detectó contenido para recortar")
                    
                except ImportError:
                    print(f"⚠️ numpy no disponible, instalando...")
                    import subprocess
                    subprocess.run(['pip', 'install', 'numpy'], check=True)
                except Exception as e:
                    print(f"⚠️ No se pudo recortar la imagen: {e}")
                    import traceback
                    traceback.print_exc()
                    # Continuar con la imagen sin recortar
                
                resultado["ruta_imagen_html"] = str(ruta_jpg)
                print(f"✅ HTML convertido a JPEG: {ruta_jpg}")
                
            except ImportError as e:
                print(f"⚠️ html2image no disponible: {e}")
                print(f"   Instala con: pip install html2image")
                resultado["ruta_imagen_html"] = None
            except Exception as e:
                print(f"⚠️ Error al convertir HTML a imagen: {e}")
                resultado["ruta_imagen_html"] = None
                
        except Exception as e:
            print(f"⚠️ No se pudo procesar el HTML: {e}")
        
        # 9. Enviar email con la póliza adjunta
        resultado["email_enviado"] = False
        # Usar PDF si existe, si no, usar Word
        archivo_adjunto = resultado.get("ruta_documento_pdf") or resultado.get("ruta_documento_word")
        if generar_documento and archivo_adjunto:
            try:
                from .email_service import EmailService
                email_service = EmailService()
                email_enviado = email_service.enviar_email_bienvenida_poliza(
                    datos_poliza=datos_poliza,
                    ruta_pdf=archivo_adjunto  # Puede ser PDF o Word
                )
                resultado["email_enviado"] = email_enviado
                if email_enviado:
                    print(f"✅ Email enviado a {datos_cliente['correo']}")
            except Exception as e:
                print(f"⚠️ No se pudo enviar el email: {e}")
                # No falla la emisión si no se puede enviar el email
        
        # 9. Enviar notificación por WhatsApp usando WAHA
        resultado["whatsapp_enviado"] = False
        resultado["whatsapp_detalles"] = None
        
        # Usar PDF si existe, si no, usar Word
        if generar_documento and archivo_adjunto:
            try:
                from .waha_service import WahaService
                # Usar servicio real con número del cliente (no hardcodeado)
                waha_service = WahaService(usar_numero_hardcodeado=False)
                
                # Formatear el número de teléfono (limpiar y formatear)
                telefono = datos_cliente.get("telefono", "")
                telefono_original = telefono  # Guardar para log
                # Limpiar el número: remover espacios, guiones, paréntesis y signos +
                telefono = telefono.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
                # Asegurar que tenga código de país 51
                if telefono and not telefono.startswith("51"):
                    telefono = f"51{telefono}"
                
                print(f"📞 Teléfono procesado: {telefono_original} -> {telefono}")
                
                # Enviar paquete completo por WhatsApp
                nombre_cliente = datos_cliente.get("nombre", "Cliente")
                resultado_whatsapp = waha_service.enviar_paquete_bienvenida_poliza(
                    numero_destino=telefono,
                    nombre_cliente=nombre_cliente,
                    ruta_imagen_html=resultado.get("ruta_imagen_html"),  # HTML guardado
                    ruta_pdf_poliza=archivo_adjunto  # Puede ser PDF o Word
                )
                
                resultado["whatsapp_enviado"] = resultado_whatsapp.get("success", False)
                resultado["whatsapp_detalles"] = resultado_whatsapp
                
                if resultado["whatsapp_enviado"]:
                    print(f"✅ WhatsApp enviado a {telefono}")
                else:
                    print(f"⚠️ No se pudo enviar WhatsApp: {resultado_whatsapp.get('errores', [])}")
            except Exception as e:
                print(f"⚠️ Error al enviar WhatsApp: {e}")
                # No falla la emisión si no se puede enviar el WhatsApp
        
        return resultado

