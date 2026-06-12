# 📞 Directorio de Contactos

Aplicación web simple para registrar y consultar contactos utilizando Flask y PostgreSQL.

## 📋 Contenido del Proyecto

```
directorio_contactos/
├── app.py                 # Aplicación principal de Flask
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración para Render
├── .env.example          # Ejemplo de variables de entorno
├── README.md             # Este archivo
├── templates/
│   ├── base.html         # Plantilla base con navegación
│   ├── index.html        # Página principal
│   ├── registro.html     # Formulario de registro
│   └── contactos.html    # Listado de contactos
└── static/
    └── style.css         # Estilos CSS
```

## 🚀 Ejecución Local

### Requisitos Previos
- Python 3.8+
- PostgreSQL instalado y corriendo
- pip (gestor de paquetes de Python)

### Paso 1: Crear la Base de Datos en PostgreSQL

Abre tu terminal/consola de PostgreSQL y ejecuta:

```sql
CREATE DATABASE directorio_contactos;
```

### Paso 2: Clonar o Descargar el Proyecto

```bash
cd /ruta/del/proyecto/directorio_contactos
```

### Paso 3: Crear un Archivo .env

Copia el archivo `.env.example` a `.env` y modifica los valores:

```bash
cp .env.example .env
```

Luego edita `.env` con tus datos:

```
DATABASE_URL=postgresql://tu_usuario:tu_contraseña@localhost:5432/directorio_contactos
SECRET_KEY=tu_clave_secreta_muy_segura
```

**Ejemplo:**
```
DATABASE_URL=postgresql://postgres:1234@localhost:5432/directorio_contactos
SECRET_KEY=clave_super_secreta_12345
```

### Paso 4: Crear un Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 5: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📲 Uso de la Aplicación

### Página Principal (/)
- Muestra el nombre de la aplicación
- Cantidad total de contactos registrados
- Acceso a las opciones principales

### Registrar Contacto (/registro)
1. Completa el formulario con:
   - **Nombre Completo**: Requerido
   - **Teléfono**: Requerido
   - **Correo**: Requerido y debe ser válido
2. Haz clic en "Registrar Contacto"
3. Si es exitoso, serás redirigido al listado de contactos

### Ver Contactos (/contactos)
- Muestra todos los contactos en una tabla
- Puedes buscar contactos por nombre
- Los datos incluyen: ID, Nombre, Teléfono y Correo

## 🌐 Despliegue en Render.com

### Paso 1: Preparar el Repositorio

1. Inicializa un repositorio Git si aún no lo has hecho:
```bash
git init
git add .
git commit -m "Initial commit"
```

2. Sube tu código a GitHub:
   - Crea un repositorio nuevo en GitHub
   - Sigue las instrucciones para subirlo

### Paso 2: Crear una Base de Datos PostgreSQL en Render

1. Ve a [Render.com](https://render.com)
2. Inicia sesión o crea una cuenta
3. En el dashboard, haz clic en **"New +"** → **"PostgreSQL"**
4. Completa la configuración:
   - **Name**: directorio_contactos
   - **Database**: directorio_contactos
   - **User**: postgres (o personalizado)
   - **Region**: Elige tu región
5. Haz clic en **"Create Database"**
6. Espera a que se crear completamente
7. Copia la **Internal Database URL** que aparecerá

### Paso 3: Crear la Aplicación Web

1. Ve a [Render.com](https://render.com)
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Completa la configuración:
   - **Name**: directorio-contactos (o tu preferencia)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Region**: Elige tu región

### Paso 4: Configurar Variables de Entorno

1. En la página de tu Web Service en Render
2. Ve a la sección **"Environment"**
3. Agrega las siguientes variables:

```
DATABASE_URL = (copia la Internal Database URL de PostgreSQL)
SECRET_KEY = (genera una clave segura, ej: algunaclavemuycomplejayaleatoria123456)
```

### Paso 5: Desplegar

1. Haz clic en **"Create Web Service"**
2. Render construirá y desplegará automáticamente tu aplicación
3. Espera a que el estatus cambie a "Live"
4. Tu aplicación estará disponible en la URL proporcionada por Render

## 📝 Archivos Explicados

### app.py
Aplicación principal que contiene:
- Configuración de Flask y SQLAlchemy
- Modelo `Contacto` para la base de datos
- Rutas: `/` (inicio), `/registro` (formulario), `/contactos` (listado)
- Validaciones básicas de email
- Manejo de errores

### requirements.txt
Dependencias necesarias:
- `Flask`: Framework web
- `Flask-SQLAlchemy`: ORM para la base de datos
- `SQLAlchemy`: Toolkit SQL
- `psycopg2-binary`: Driver PostgreSQL para Python
- `python-dotenv`: Para cargar variables de .env
- `Gunicorn`: Servidor WSGI para producción

### Procfile
Configura el comando para ejecutar en Render:
```
web: gunicorn app:app
```

### Templates

**base.html**: Plantilla base con:
- Barra de navegación
- Manejo de mensajes flash
- Footer

**index.html**: Página principal con:
- Descripción de la app
- Contador de contactos
- Botones de acceso rápido

**registro.html**: Formulario con campos para:
- Nombre completo
- Teléfono
- Correo electrónico
- Validación en el lado del cliente

**contactos.html**: Listado con:
- Tabla responsiva
- Búsqueda por nombre
- Enlaces para llamadas y correos

### static/style.css
Estilos personalizados usando Bootstrap 5 incluyendo:
- Colores consistentes
- Responsive design
- Animaciones suaves
- Diseño limpio y moderno

## 🔧 Troubleshooting

### Error: "No module named 'flask'"
**Solución**: Asegúrate de instalar las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "psycopg2: connection failed"
**Solución**: Verifica que:
1. PostgreSQL está corriendo
2. Las credenciales en `.env` son correctas
3. La base de datos existe

### Error: "No such file or directory: .env"
**Solución**: Crea el archivo `.env` basado en `.env.example`:
```bash
cp .env.example .env
```

### Render dice "Application failed to start"
**Solución**: Revisa los logs en Render y verifica:
1. DATABASE_URL está correctamente configurada
2. Las dependencias en requirements.txt son correctas
3. El Procfile tiene el contenido correcto

## 📚 Tecnologías Utilizadas

- **Backend**: Python, Flask 2.3
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, CSS3
- **Servidor**: Gunicorn
- **Hosting**: Render.com

## ✅ Funcionalidades Implementadas

✓ Página principal con información de la app
✓ Registro de contactos con validación
✓ Consulta de contactos con búsqueda
✓ Integración con PostgreSQL
✓ Interfaz responsiva
✓ Mensajes de éxito/error
✓ Preparado para Render.com
✓ Código limpio y fácil de entender

## 📄 Licencia

Proyecto académico - Uso libre para propósitos educativos.

---

**Autor**: Directorio de Contactos - Proyecto Académico
**Versión**: 1.0
**Fecha**: Junio 2024
