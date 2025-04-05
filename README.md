# Blueprint Reader API

API para procesar PDF de planos arquitectónicos y extraer datos estructurados.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Sistema operativo compatible (Windows/Linux/macOS)

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/franco-parra/blueprint-reader.git
cd blueprint-reader
```

2. Crear y activar un entorno virtual (recomendado):

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

El proyecto utiliza un archivo `.env` para la configuración. Se incluye un archivo `.env.example` que puedes copiar y modificar:

```bash
cp .env.example .env
```

### Variables de Entorno

- `FLASK_ENV`: Ambiente de ejecución (`development` o `production`)
- `PORT`: Puerto del servidor (por defecto: 5000)
- `HOST`: Host del servidor (por defecto: 0.0.0.0)
- `REFERENCE_PDF_PATH`: Ruta al archivo PDF de referencia
- `BLUEPRINT_DATA_PATH`: Ruta al archivo JSON con datos del plano
- `UPLOAD_FOLDER`: Directorio para archivos temporales
- `MAX_CONTENT_LENGTH`: Límite de tamaño de archivo en bytes (por defecto: 16MB)
- `ALLOWED_ORIGINS`: Orígenes permitidos para CORS (separados por comas)

### Configuración de CORS

La API está configurada con CORS para permitir solicitudes desde orígenes específicos. En el archivo `.env`, puedes configurar:

```env
ALLOWED_ORIGINS=http://localhost:3000,https://blueprint-reader.com
```

Para desarrollo local, puedes usar `*` para permitir todos los orígenes (no recomendado para producción).

## Ejecución

### Modo Desarrollo

1. Asegúrate de que `FLASK_ENV=development` en tu archivo `.env`
2. Ejecuta la aplicación:

```bash
python main.py
```

La aplicación estará disponible en `http://localhost:5000`

### Modo Producción

#### Windows (usando Waitress)

1. Configura `FLASK_ENV=production` en tu archivo `.env`
2. Ejecuta:

```bash
python main.py
```

#### Linux/macOS (usando Gunicorn)

1. Configura `FLASK_ENV=production` en tu archivo `.env`
2. Ejecuta:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Endpoints

### POST /parse-blueprint

Procesa un archivo PDF y devuelve los datos estructurados si coincide con el archivo de referencia. El procesamiento interno es netamente referencial y de integración con otros sistemas. En un futuro, se integrará con un modelo de machine learning para la extracción de datos.

**Parámetros:**

- `file`: Archivo PDF a procesar

**Respuesta Exitosa:**

```json
{
  "message": "Blueprint parsed successfully",
  "filename": "archivo.pdf",
  "data": {
    // Datos estructurados del plano
  }
}
```

## Mantenimiento

### Limpieza de Archivos Temporales

Los archivos temporales se eliminan automáticamente después del procesamiento. El directorio `uploads` se crea automáticamente al iniciar la aplicación.

### Actualización de Datos de Referencia

Para actualizar el archivo PDF de referencia o los datos estructurados:

1. Reemplaza el archivo correspondiente
2. Reinicia la aplicación

## Solución de Problemas

### Errores Comunes

1. **Archivo no encontrado**

   - Verifica las rutas en `.env`
   - Asegúrate de que los directorios existan

2. **Error de CORS**

   - Verifica `ALLOWED_ORIGINS` en `.env`
   - Asegúrate de que el origen esté incluido

3. **Archivo demasiado grande**
   - Ajusta `MAX_CONTENT_LENGTH` en `.env`

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
