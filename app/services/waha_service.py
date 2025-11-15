"""
Servicio de WhatsApp WAHA
Contiene toda la lógica para enviar mensajes, imágenes y archivos por WhatsApp
"""

import base64
import requests
from typing import Dict, Any, Optional
from pathlib import Path


class WahaService:
    """
    Servicio para enviar mensajes por WhatsApp usando WAHA API
    """

    def __init__(
        self, 
        base_url: Optional[str] = None, 
        session_id: Optional[str] = None,
        use_mock: bool = False,
        usar_numero_hardcodeado: bool = True,
        api_key: Optional[str] = None
    ):
        """
        Inicializa el servicio de WAHA

        Args:
            base_url: URL base del servicio WAHA
            session_id: ID de la sesión de WhatsApp
            use_mock: Si es True, usa modo simulación en lugar de llamadas reales
            usar_numero_hardcodeado: Si es True, usa número hardcodeado. Si es False, usa el número del cliente
            api_key: API Key para autenticación con WAHA
        """
        self.base_url = base_url or "https://waha-197831323053.us-central1.run.app"
        self.session_id = session_id or "rumbia"
        self.is_mock = use_mock
        self.usar_numero_hardcodeado = usar_numero_hardcodeado
        self.api_key = api_key or "aeea8b07bf994b6d888a92cc2ba38c20"
        # Número hardcodeado como fallback
        self.numero_hardcodeado = "51970941145"
        
        # Headers para las peticiones HTTP
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }

    def _obtener_numero_destino(self, numero_destino: str) -> str:
        """
        Determina qué número usar según la configuración
        
        Args:
            numero_destino: Número proporcionado
            
        Returns:
            str: Número a usar (hardcodeado o el proporcionado)
        """
        if self.usar_numero_hardcodeado:
            return self.numero_hardcodeado
        return numero_destino if numero_destino else self.numero_hardcodeado

    def enviar_mensaje(self, numero_destino: str, mensaje: str) -> Dict[str, Any]:
        """
        Envía un mensaje de texto por WhatsApp

        Args:
            numero_destino: Número de teléfono destino (formato: 51999999999)
            mensaje: Texto del mensaje a enviar

        Returns:
            Dict: Respuesta del servicio WAHA
        """
        # Determinar qué número usar
        numero_final = self._obtener_numero_destino(numero_destino)
        
        if self.is_mock:
            print(f"📱 [MOCK] Enviando mensaje a {numero_final}")
            print(f"Mensaje:\n{mensaje}")
            return {
                "success": True,
                "message_id": f"mock_{numero_final}_text",
                "timestamp": "2024-01-01T00:00:00Z",
                "status": "sent",
            }

        try:
            endpoint = f"{self.base_url}/api/sendText"
            payload = {
                "session": self.session_id,
                "chatId": f"{numero_final}@c.us",
                "text": mensaje,
                "reply_to": None
            }
            
            print(f"📱 Enviando mensaje a {numero_final}")
            print(f"   Endpoint: {endpoint}")
            print(f"   Payload: {payload}")
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=30)
            
            # Si hay error, mostrar detalles
            if response.status_code != 200:
                print(f"   ⚠️ Status Code: {response.status_code}")
                print(f"   ⚠️ Response: {response.text}")
            
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "response": result
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al enviar mensaje: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Detalle del error: {error_detail}")
                except:
                    print(f"   Respuesta: {e.response.text}")
            return {
                "success": False,
                "error": str(e)
            }

    def enviar_imagen_desde_base64(
        self,
        numero_destino: str,
        imagen_base64: str,
        caption: Optional[str] = None,
        filename: str = "imagen.png",
    ) -> Dict[str, Any]:
        """
        Envía una imagen por WhatsApp desde base64

        Args:
            numero_destino: Número de teléfono destino (formato: 51999999999)
            imagen_base64: Imagen codificada en base64
            caption: Texto adicional que acompaña la imagen
            filename: Nombre del archivo

        Returns:
            Dict: Respuesta del servicio WAHA
        """
        # Determinar qué número usar
        numero_final = self._obtener_numero_destino(numero_destino)
        
        if self.is_mock:
            print(f"📱 [MOCK] Enviando imagen a {numero_final}")
            print(f"Archivo: {filename}")
            if caption:
                print(f"Caption: {caption}")
            print(f"Tamaño base64: {len(imagen_base64)} caracteres")
            return {
                "success": True,
                "message_id": f"mock_{numero_final}_image",
                "timestamp": "2024-01-01T00:00:00Z",
                "status": "sent",
            }

        try:
            endpoint = f"{self.base_url}/api/sendImage"
            
            # Determinar mimetype basado en la extensión
            mimetype = "image/jpeg"
            if filename.lower().endswith('.png'):
                mimetype = "image/png"
            elif filename.lower().endswith('.gif'):
                mimetype = "image/gif"
            
            payload = {
                "session": self.session_id,
                "chatId": f"{numero_final}@c.us",
                "file": {
                    "mimetype": mimetype,
                    "filename": filename,
                    "data": imagen_base64
                },
                "caption": caption
            }
            
            print(f"📱 Enviando imagen a {numero_final} (base64: {len(imagen_base64)} chars)")
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "response": result
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al enviar imagen: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Detalle del error: {error_detail}")
                except:
                    print(f"   Respuesta: {e.response.text}")
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            print(f"❌ Error al enviar imagen: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def enviar_imagen_desde_ruta(
        self, numero_destino: str, ruta_imagen: str, caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envía una imagen por WhatsApp desde una ruta de archivo usando base64

        Args:
            numero_destino: Número de teléfono destino
            ruta_imagen: Ruta del archivo de imagen
            caption: Texto adicional que acompaña la imagen

        Returns:
            Dict: Respuesta del servicio WAHA
        """
        try:
            path = Path(ruta_imagen)
            
            if not path.exists():
                return {
                    "success": False,
                    "error": f"Archivo no encontrado: {ruta_imagen}"
                }
            
            # Leer archivo y convertir a base64
            with open(path, "rb") as f:
                imagen_bytes = f.read()
                imagen_base64 = base64.b64encode(imagen_bytes).decode("utf-8")

            # Usar el método enviar_imagen_desde_base64
            return self.enviar_imagen_desde_base64(
                numero_destino=numero_destino,
                imagen_base64=imagen_base64,
                caption=caption,
                filename=path.name,
            )
        except Exception as e:
            print(f"❌ Error al leer imagen: {e}")
            return {"success": False, "error": str(e)}

    def enviar_documento(
        self, numero_destino: str, ruta_documento: str, caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envía un documento (PDF, Word, etc.) por WhatsApp usando base64

        Args:
            numero_destino: Número de teléfono destino (formato: 51999999999)
            ruta_documento: Ruta del archivo del documento
            caption: Texto adicional que acompaña el documento

        Returns:
            Dict: Respuesta del servicio WAHA
        """
        try:
            # Determinar qué número usar
            numero_final = self._obtener_numero_destino(numero_destino)
            
            path = Path(ruta_documento)

            if not path.exists():
                return {
                    "success": False,
                    "error": f"Archivo no encontrado: {ruta_documento}",
                }

            # Leer archivo y convertir a base64
            with open(path, "rb") as f:
                documento_bytes = f.read()
                documento_base64 = base64.b64encode(documento_bytes).decode("utf-8")

            if self.is_mock:
                print(f"📱 [MOCK] Enviando documento a {numero_final}")
                print(f"Archivo: {path.name}")
                print(f"Tamaño: {len(documento_bytes)} bytes")
                if caption:
                    print(f"Caption: {caption}")
                return {
                    "success": True,
                    "message_id": f"mock_{numero_final}_document",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "status": "sent",
                }

            # Determinar mimetype basado en la extensión
            mimetype = "application/pdf"
            if path.suffix.lower() == '.docx':
                mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif path.suffix.lower() == '.doc':
                mimetype = "application/msword"
            elif path.suffix.lower() == '.txt':
                mimetype = "text/plain"

            endpoint = f"{self.base_url}/api/sendFile"
            payload = {
                "session": self.session_id,
                "chatId": f"{numero_final}@c.us",
                "caption": caption,
                "file": {
                    "mimetype": mimetype,
                    "filename": path.name,
                    "data": documento_base64
                }
            }

            print(f"📱 Enviando documento '{path.name}' a {numero_final} (base64: {len(documento_base64)} chars)")
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=60)
            response.raise_for_status()

            result = response.json()
            return {
                "success": True,
                "response": result
            }

        except requests.exceptions.RequestException as e:
            print(f"❌ Error al enviar documento: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Detalle del error: {error_detail}")
                except:
                    print(f"   Respuesta: {e.response.text}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            print(f"❌ Error al enviar documento: {e}")
            return {"success": False, "error": str(e)}

    def enviar_paquete_bienvenida_poliza(
        self,
        numero_destino: str,
        ruta_imagen_html: Optional[str] = None,
        ruta_pdf_poliza: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Envía el paquete completo de bienvenida de póliza:
        1. Mensaje de bienvenida
        2. Imagen del HTML (opcional)
        3. PDF de la póliza (opcional)

        Args:
            numero_destino: Número de teléfono del cliente
            ruta_imagen_html: Ruta de la imagen del HTML enviado por correo
            ruta_pdf_poliza: Ruta del PDF de la póliza

        Returns:
            Dict: Resumen de los envíos realizados
        """
        resultados = {
            "numero_destino": numero_destino,
            "mensaje_enviado": False,
            "imagen_enviada": False,
            "pdf_enviado": False,
            "errores": [],
        }

        # 1. Enviar mensaje de bienvenida
        mensaje_bienvenida = """*Aseguraste tu futuro ✨*

Gracias por comprar tu seguro Rumbo 🤩

Revisa tu bandeja de entrada, te enviaremos tu póliza contratada 📩

Si tienes dudas o consultas, escríbenos por aquí o entra a interseguro.pe 💙"""

        try:
            resultado_mensaje = self.enviar_mensaje(numero_destino, mensaje_bienvenida)
            resultados["mensaje_enviado"] = resultado_mensaje.get("success", False)
            if not resultado_mensaje.get("success"):
                resultados["errores"].append(
                    f"Mensaje: {resultado_mensaje.get('error', 'Unknown error')}"
                )
        except Exception as e:
            resultados["errores"].append(f"Mensaje: {str(e)}")

        # 2. Enviar imagen del HTML (si existe)
        if ruta_imagen_html:
            try:
                resultado_imagen = self.enviar_imagen_desde_ruta(
                    numero_destino=numero_destino,
                    ruta_imagen=ruta_imagen_html,
                    caption="Vista previa de tu póliza",
                )
                resultados["imagen_enviada"] = resultado_imagen.get("success", False)
                if not resultado_imagen.get("success"):
                    resultados["errores"].append(
                        f"Imagen: {resultado_imagen.get('error', 'Unknown error')}"
                    )
            except Exception as e:
                resultados["errores"].append(f"Imagen: {str(e)}")

        # 3. Enviar PDF de la póliza (si existe)
        if ruta_pdf_poliza:
            try:
                resultado_pdf = self.enviar_documento(
                    numero_destino=numero_destino,
                    ruta_documento=ruta_pdf_poliza,
                    caption="Tu póliza Rumbo",
                )
                resultados["pdf_enviado"] = resultado_pdf.get("success", False)
                if not resultado_pdf.get("success"):
                    resultados["errores"].append(
                        f"PDF: {resultado_pdf.get('error', 'Unknown error')}"
                    )
            except Exception as e:
                resultados["errores"].append(f"PDF: {str(e)}")

        # Determinar éxito general
        resultados["success"] = (
            resultados["mensaje_enviado"]
            and (not ruta_imagen_html or resultados["imagen_enviada"])
            and (not ruta_pdf_poliza or resultados["pdf_enviado"])
        )

        return resultados
