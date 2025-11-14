# 📄 Servicio de Generación de Documentos Word y PDF

## 🎯 Descripción

El servicio `GenerateDocumentService` genera automáticamente documentos Word personalizados para cada póliza emitida y **los convierte a PDF**, utilizando la plantilla ubicada en `assets/condicionado_particular/rumbo_plantilla_sme.docx`.

---

## 📦 Instalación de Dependencias

Para usar este servicio, instala las siguientes dependencias:

```bash
pip install python-docx==1.1.0
pip install docx2pdf==0.1.8
```

O instala todas las dependencias actualizadas:

```bash
pip install -r requirements.txt
```

### ⚠️ Requisitos para Conversión a PDF

**Opción 1: Microsoft Word instalado (Recomendado en Windows)**
- `docx2pdf` usa MS Word a través de COM automation
- Funciona automáticamente si tienes Word instalado

**Opción 2: LibreOffice (Alternativa gratuita)**
- Descarga e instala [LibreOffice](https://www.libreoffice.org/download/download/)
- El servicio lo detectará automáticamente si está en las rutas estándar

---

## 🗂️ Estructura de Archivos

```
rumbia-backend/
├── assets/
│   └── condicionado_particular/
│       └── rumbo_plantilla_sme.docx     ← Plantilla Word
├── db/
│   ├── RumbIA001.json                   ← Datos de póliza (JSON)
│   └── documentos/
│       ├── RumbIA001_Condicionado_Particular.docx  ← Documento Word
│       └── RumbIA001_Condicionado_Particular.pdf   ← Documento PDF ✨
└── app/
    └── services/
        └── generate_document_service.py  ← Servicio de generación
```

---

## 🔧 Marcadores en la Plantilla Word

Para que el servicio funcione correctamente, la plantilla Word debe contener los siguientes marcadores usando **comillas angulares francesas** `«»`:

### Datos de la Póliza
- `«numeroPoliza»` - Número de póliza (ejemplo: RumbIA001)

### Datos del Cliente
- `«clienteNumeroDocumento»` - DNI del cliente
- `«clienteNombre»` - Nombre completo del cliente
- `«clienteFechaNacimiento»` - Fecha de nacimiento
- `«clienteGenero»` - Género (Masculino/Femenino)
- `«clienteTelefono»` - Teléfono de contacto
- `«clienteEmail»` - Correo electrónico
- `«clienteEdadActuarial»` - Edad actuarial

### Datos de la Cotización
- `«periodoPagoPrimas»` - Período de pago (Mensual)
- `«sumaAsegurada»` - Suma asegurada (formato: S/ 25,000.00)
- `«primaAnual»` - Prima anual
- `«primaMensual»` - Prima mensual
- `«devolucion»` - Monto de devolución
- `«producto»` - Nombre del producto (RUMBO)
- `«tasaImplicita»` - Tasa implícita (%)
- `«porcentajeDevolucion»` - Porcentaje de devolución (%)

### Fechas
- `«fechaEmisionPoliza»` - Fecha de emisión (formato: DD/MM/YYYY)
- `«fechaHoraEmisionPoliza»` - Fecha y hora de emisión (formato: DD/MM/YYYY HH:MM:SS)
- `«fechaHoraInicioVigencia»` - Inicio de vigencia (fecha actual a las 00:00:00)
- `«fechaHoraFinVigencia»` - Fin de vigencia (último día del mes a las 23:59:59)

---

## 🚀 Uso del Servicio

### Integración Automática con Emisión de Póliza

Cuando emites una póliza a través del endpoint `/emision-poliza`, el documento se genera automáticamente:

```python
POST /api/v1/rumbia/emision-poliza
```

**Respuesta:**
```json
{
  "status": "success",
  "message": "Póliza emitida exitosamente para Juan Pérez - Documentos Word y PDF generados correctamente",
  "numero_poliza": "POL-20251114-153022-001",
  "id_poliza": 1,
  "archivo_poliza": "RumbIA001.json",
  "documento_generado": true,
  "ruta_documento_word": "C:/path/to/db/documentos/RumbIA001_Condicionado_Particular.docx",
  "ruta_documento_pdf": "C:/path/to/db/documentos/RumbIA001_Condicionado_Particular.pdf",
  "fecha_emision": "2025-11-14T15:30:22.123456",
  ...
}
```

### Uso Programático del Servicio

```python
from app.services import GenerateDocumentService
import json

# Cargar datos de póliza desde JSON
with open('db/RumbIA001.json', 'r', encoding='utf-8') as f:
    datos_poliza = json.load(f)

# Generar documentos Word y PDF
servicio = GenerateDocumentService()
ruta_word, ruta_pdf = servicio.generar_documento(datos_poliza, generar_pdf=True)

print(f"✅ Documento Word: {ruta_word}")
print(f"✅ Documento PDF: {ruta_pdf}")
```

### Generar Documentos para Todas las Pólizas

```python
from app.utils.document_utils import generar_documentos_todas_polizas

# Generar documentos para todas las pólizas en db/
documentos = generar_documentos_todas_polizas()

for doc in documentos:
    print(f"✅ Generado: {doc}")
```

---

## 📋 Mapeo de Datos

| Campo JSON | Marcador en Word | Ejemplo |
|-----------|------------------|---------|
| `id_poliza` | `«numeroPoliza»` | RumbIA001 |
| `cliente.dni` | `«clienteNumeroDocumento»` | 12345678 |
| `cliente.nombre` | `«clienteNombre»` | Juan Pérez |
| `cliente.fechaNacimiento` | `«clienteFechaNacimiento»` | 1990-05-15 |
| `cliente.genero` | `«clienteGenero»` | Masculino |
| `cliente.telefono` | `«clienteTelefono»` | +51987654321 |
| `cliente.correo` | `«clienteEmail»` | juan@example.com |
| `cotizacion.parametros.edad_actuarial` | `«clienteEdadActuarial»` | 35 |
| `cotizacion.suma_asegurada` | `«sumaAsegurada»` | S/ 25,000.00 |
| `cotizacion.prima_anual` | `«primaAnual»` | S/ 2,500.00 |
| `fecha_emision` | `«fechaEmisionPoliza»` | 14/11/2025 |

---

## 🎨 Características del Servicio

✅ **Generación dual**: Crea automáticamente Word y PDF en una sola operación

✅ **Reemplazo inteligente**: Busca y reemplaza marcadores en:
  - Párrafos
  - Tablas
  - Encabezados
  - Pies de página

✅ **Formato de fechas**: Convierte automáticamente fechas ISO a formato legible

✅ **Cálculo de vigencias**: Calcula automáticamente inicio y fin de vigencia

✅ **Formato de montos**: Formatea valores monetarios con separadores de miles

✅ **Conversión automática a PDF**: Detecta y usa MS Word o LibreOffice

✅ **Fallback inteligente**: Si falla docx2pdf, intenta con LibreOffice

✅ **Manejo de errores**: No interrumpe la emisión de póliza si falla la generación del documento

---

## 🔍 Ejemplo de Plantilla Word

En tu documento Word, usa los marcadores así:

```
CONDICIONADO PARTICULAR DE LA PÓLIZA «numeroPoliza»

DATOS DEL ASEGURADO
Nombre: «clienteNombre»
DNI: «clienteNumeroDocumento»
Fecha de Nacimiento: «clienteFechaNacimiento»
Género: «clienteGenero»

DATOS DE LA PÓLIZA
Suma Asegurada: «sumaAsegurada»
Prima Anual: «primaAnual»
Fecha de Emisión: «fechaEmisionPoliza»
Vigencia Desde: «fechaHoraInicioVigencia»
Vigencia Hasta: «fechaHoraFinVigencia»
```

---

## 🐛 Solución de Problemas

### Error: "Module 'docx' not found"
```bash
pip install python-docx==1.1.0
```

### Error: "Module 'docx2pdf' not found"
```bash
pip install docx2pdf==0.1.8
```

### PDF no se genera (Word sí se genera)
**Causa común**: No tienes MS Word instalado

**Solución 1**: Instalar LibreOffice (gratuito)
1. Descargar de https://www.libreoffice.org/download/download/
2. Instalar en la ruta por defecto
3. Reiniciar el servicio

**Solución 2**: Usar MS Word
- Asegúrate de tener Microsoft Word instalado
- En Windows, `docx2pdf` usará Word automáticamente

### Error: "Plantilla no encontrada"
Verifica que el archivo exista en:
```
assets/condicionado_particular/rumbo_plantilla_sme.docx
```

### Los marcadores no se reemplazan
- Asegúrate de que los marcadores usen comillas angulares francesas `«marcador»`
- Los nombres deben coincidir exactamente (case-sensitive)
- Evita espacios dentro de las comillas angulares
- Para escribir «» en Word: Alt+0171 para «  y Alt+0187 para »

### El PDF se ve diferente al Word
- Esto es normal, cada conversor puede formatear ligeramente diferente
- Revisa la plantilla para asegurar formato compatible
- Usa estilos nativos de Word en lugar de formato manual

---

## 📝 Notas Importantes

1. **Formato de marcadores**: Siempre usa `«nombreMarcador»` (comillas angulares francesas)
2. **Atajos de teclado**: En Word, usa Alt+0171 para « y Alt+0187 para »
3. **Nombres exactos**: Los nombres de marcadores son sensibles a mayúsculas
4. **Backup de plantilla**: Mantén una copia de seguridad de la plantilla original
5. **Permisos**: Asegúrate de tener permisos de escritura en `db/documentos/`

---

## 🎯 Próximas Mejoras

- [x] Generación de PDF además de Word ✅
- [ ] Firma digital de documentos
- [ ] Envío automático por email
- [ ] Plantillas personalizables por producto
- [ ] Generación de anexos adicionales
- [ ] Compresión de documentos en ZIP
- [ ] Watermark en PDFs
- [ ] Cifrado de documentos sensibles

---

**¡El servicio está listo para generar documentos Word y PDF profesionales automáticamente! 🚀📄**

