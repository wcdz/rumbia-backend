"""
Servicio de Envío de Emails
Maneja el envío de correos electrónicos con plantillas HTML
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import calendar


class EmailService:
    """
    Servicio para enviar emails usando plantillas HTML
    """
    
    def __init__(self):
        """Inicializa el servicio de email con configuración"""
        from app.core.config import get_settings
        
        self.base_path = Path(__file__).parent.parent.parent
        self.plantilla_path = self.base_path / "assets" / "plantilla_correo" / "BienvenidaRumbo.html"
        
        # Cargar configuración desde settings
        settings = get_settings()
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
        self.from_name = settings.FROM_NAME
    
    def obtener_ultimo_dia_mes_futuro(self, fecha: datetime, anos_agregar: int) -> datetime:
        """
        Obtiene el último día del mes en una fecha futura
        
        Args:
            fecha: Fecha base
            anos_agregar: Años a agregar
            
        Returns:
            datetime: Fecha del último día del mes futuro
        """
        # Calcular año y mes futuro
        ano_futuro = fecha.year + anos_agregar
        mes_futuro = fecha.month
        
        # Obtener último día del mes
        ultimo_dia = calendar.monthrange(ano_futuro, mes_futuro)[1]
        
        return fecha.replace(year=ano_futuro, day=ultimo_dia)
    
    def preparar_datos_email(self, datos_poliza: Dict[str, Any]) -> Dict[str, str]:
        """
        Prepara los datos para reemplazar en la plantilla de email
        
        Args:
            datos_poliza: Datos completos de la póliza
            
        Returns:
            Dict: Diccionario con los marcadores y sus valores
        """
        # Parsear fecha de emisión
        fecha_emision = datetime.fromisoformat(datos_poliza["fecha_emision"])
        
        # Generar número de póliza en formato RumbIA###
        id_poliza = datos_poliza["id_poliza"]
        numero_poliza = f"RumbIA{id_poliza:03d}"
        
        # Obtener periodo de pago en años (por defecto usamos la longitud de la tabla de devolución)
        # o un valor fijo si no está disponible
        import json as json_module
        tabla_devolucion_str = datos_poliza["cotizacion"].get("tabla_devolucion", "[]")
        tabla_devolucion = json_module.loads(tabla_devolucion_str) if isinstance(tabla_devolucion_str, str) else tabla_devolucion_str
        periodo_pago_primas = len(tabla_devolucion) if tabla_devolucion else 7
        
        # Calcular prima mensual
        prima_anual = datos_poliza["cotizacion"]["prima_anual"]
        prima_mensual = prima_anual / 10
        
        # Formatear fechas
        fecha_emision_str = fecha_emision.strftime("%d/%m/%Y")
        
        # Calcular fecha fin (último día del mes actual + periodo_pago_primas años)
        fecha_fin = self.obtener_ultimo_dia_mes_futuro(fecha_emision, periodo_pago_primas)
        fecha_fin_str = fecha_fin.strftime("%d/%m/%Y")
        
        # Formatear montos
        devolucion = datos_poliza["cotizacion"]["devolucion"]
        
        return {
            "#!Id_nombrecliente!#": datos_poliza["cliente"]["nombre"],
            "#!Id_numeropoliza!#": numero_poliza,
            "#!Id_periodo!#": f"{periodo_pago_primas} años",
            "#!Id_Monto_devolucion!#": f"S/ {devolucion:,.2f}",
            "#!Id_montoprima!#": f"S/ {prima_mensual:,.2f}",
            "#!Id_fechaemision!#": fecha_emision_str,
            "#!Id_fechafin!#": fecha_fin_str
        }
    
    def generar_html_email(self, datos_poliza: Dict[str, Any]) -> str:
        """
        Genera el HTML del email reemplazando los marcadores
        
        Args:
            datos_poliza: Datos completos de la póliza
            
        Returns:
            str: HTML del email con los datos reemplazados
        """
        # Leer la plantilla HTML
        with open(self.plantilla_path, 'r', encoding='utf-8') as f:
            html_template = f.read()
        
        # Preparar los datos
        marcadores = self.preparar_datos_email(datos_poliza)
        
        # Reemplazar todos los marcadores
        html_email = html_template
        for marcador, valor in marcadores.items():
            html_email = html_email.replace(marcador, str(valor))
        
        return html_email
    
    def enviar_email(
        self,
        destinatario: str,
        asunto: str,
        html_content: str,
        archivo_adjunto: Optional[str] = None,
        password_pdf: Optional[str] = None
    ) -> bool:
        """
        Envía un email con contenido HTML y opcionalmente un archivo adjunto
        
        Args:
            destinatario: Email del destinatario
            asunto: Asunto del email
            html_content: Contenido HTML del email
            archivo_adjunto: Ruta al archivo a adjuntar (opcional)
            password_pdf: Contraseña del PDF (opcional, se menciona en el email)
            
        Returns:
            bool: True si se envió exitosamente, False en caso contrario
        """
        try:
            # Crear mensaje
            mensaje = MIMEMultipart('alternative')
            mensaje['From'] = f"{self.from_name} <{self.from_email}>"
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto
            
            # Agregar contenido HTML
            parte_html = MIMEText(html_content, 'html', 'utf-8')
            mensaje.attach(parte_html)
            
            # Agregar archivo adjunto si existe
            if archivo_adjunto and Path(archivo_adjunto).exists():
                with open(archivo_adjunto, 'rb') as adjunto:
                    parte_adjunto = MIMEBase('application', 'octet-stream')
                    parte_adjunto.set_payload(adjunto.read())
                
                encoders.encode_base64(parte_adjunto)
                
                filename = Path(archivo_adjunto).name
                parte_adjunto.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                
                mensaje.attach(parte_adjunto)
            
            # Conectar al servidor SMTP y enviar
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as servidor:
                servidor.starttls()
                servidor.login(self.smtp_user, self.smtp_password)
                servidor.send_message(mensaje)
            
            print(f"✅ Email enviado exitosamente a {destinatario}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar email: {e}")
            return False
    
    def enviar_email_bienvenida_poliza(
        self,
        datos_poliza: Dict[str, Any],
        ruta_pdf: Optional[str] = None
    ) -> bool:
        """
        Envía el email de bienvenida con la póliza adjunta
        
        Args:
            datos_poliza: Datos completos de la póliza
            ruta_pdf: Ruta al PDF de la póliza (opcional)
            
        Returns:
            bool: True si se envió exitosamente
        """
        # Generar HTML del email
        html_content = self.generar_html_email(datos_poliza)
        
        # Obtener email del cliente
        email_cliente = datos_poliza["cliente"]["correo"]
        nombre_cliente = datos_poliza["cliente"]["nombre"]
        dni_cliente = datos_poliza["cliente"]["dni"]
        
        # Asunto del email
        asunto = f"¡Bienvenido a Rumbo! - Póliza RumbIA{datos_poliza['id_poliza']:03d}"
        
        # Enviar email
        return self.enviar_email(
            destinatario=email_cliente,
            asunto=asunto,
            html_content=html_content,
            archivo_adjunto=ruta_pdf,
            password_pdf=dni_cliente
        )

