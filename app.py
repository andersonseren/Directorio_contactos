import os
import re
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
# Usa PostgreSQL en producción (Render), SQLite en desarrollo local
database_url = os.getenv('DATABASE_URL')
if database_url:
    # En producción (Render)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # En desarrollo local (sin PostgreSQL)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactos.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui')

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# ============= MODELO =============
class Contacto(db.Model):
    __tablename__ = 'contactos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Contacto {self.nombre}>'

# ============= FUNCIONES AUXILIARES =============
def validar_email(email):
    """Valida que el email tenga un formato válido"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

# ============= RUTAS =============

@app.route('/')
def index():
    """Página principal"""
    total_contactos = Contacto.query.count()
    return render_template('index.html', total_contactos=total_contactos)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Formulario de registro de contactos"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        telefono = request.form.get('telefono', '').strip()
        correo = request.form.get('correo', '').strip()
        
        # Validaciones
        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return redirect(url_for('registro'))
        
        if not telefono:
            flash('El teléfono es obligatorio', 'error')
            return redirect(url_for('registro'))
        
        if not correo:
            flash('El correo es obligatorio', 'error')
            return redirect(url_for('registro'))
        
        if not validar_email(correo):
            flash('El correo no tiene un formato válido', 'error')
            return redirect(url_for('registro'))
        
        # Guardar en la base de datos
        try:
            nuevo_contacto = Contacto(nombre=nombre, telefono=telefono, correo=correo)
            db.session.add(nuevo_contacto)
            db.session.commit()
            flash('Contacto registrado exitosamente', 'success')
            return redirect(url_for('contactos'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar el contacto', 'error')
            return redirect(url_for('registro'))
    
    return render_template('registro.html')

@app.route('/contactos')
def contactos():
    """Listar todos los contactos"""
    busqueda = request.args.get('busqueda', '').strip()
    
    if busqueda:
        contactos_list = Contacto.query.filter(
            Contacto.nombre.ilike(f'%{busqueda}%')
        ).all()
    else:
        contactos_list = Contacto.query.all()
    
    return render_template('contactos.html', contactos=contactos_list, busqueda=busqueda)

# ============= RUTA DE PRUEBAS FUNCIONALES (INFORME HTML DESCRIPTIVO) =============
@app.route('/test')
def run_functional_tests():
    """Ejecuta pruebas funcionales y muestra un informe claro en HTML."""

    # Limpiar datos de prueba anteriores
    with app.app_context():
        Contacto.query.filter(Contacto.nombre.like('Test_%')).delete()
        db.session.commit()

    # Lista para almacenar los resultados de cada prueba
    resultados = []

    # ------------------------------------------------------------
    # PRUEBA A: Home Page - Index
    # ------------------------------------------------------------
    with app.test_client() as cliente:
        response = cliente.get('/')
        test_paso = response.status_code == 200 and b'Contactos' in response.data
        resultados.append({
            'id': 'A',
            'nombre': 'Home Page - Index',
            'descripcion': 'Verifica que la página principal cargue correctamente y contenga "Contactos".',
            'resultado': f'Código {response.status_code}, contiene "Contactos"' if test_paso else f'Código {response.status_code}, NO contiene "Contactos"',
            'estado': 'PASÓ ✅' if test_paso else 'FALLÓ ❌',
            'paso': test_paso
        })

    # ------------------------------------------------------------
    # PRUEBA B: Registro de usuario (GET) - Página 2
    # ------------------------------------------------------------
    with app.test_client() as cliente:
        response = cliente.get('/registro')
        test_paso = response.status_code == 200 and b'Registrar' in response.data
        resultados.append({
            'id': 'B',
            'nombre': 'Registro de usuario (página 2)',
            'descripcion': 'Muestra el formulario de registro con el enlace "Registrar".',
            'resultado': f'Código {response.status_code}, contiene "Registrar"' if test_paso else f'Código {response.status_code}, NO contiene "Registrar"',
            'estado': 'PASÓ ✅' if test_paso else 'FALLÓ ❌',
            'paso': test_paso
        })

    # ------------------------------------------------------------
    # PRUEBA B (POST): Envío del formulario de registro
    # ------------------------------------------------------------
    with app.test_client() as cliente:
        data = {
            'nombre': 'Test_Funcional',
            'telefono': '123456789',
            'correo': 'test@example.com'
        }
        response = cliente.post('/registro', data=data, follow_redirects=True)
        test_paso = response.status_code == 200 and b'Contacto registrado exitosamente' in response.data
        resultados.append({
            'id': 'B2',
            'nombre': 'Registro de usuario (POST)',
            'descripcion': 'Envía datos válidos y espera confirmación de registro exitoso.',
            'resultado': f'Código {response.status_code}, mensaje de éxito presente' if test_paso else f'Código {response.status_code}, mensaje de éxito ausente',
            'estado': 'PASÓ ✅' if test_paso else 'FALLÓ ❌',
            'paso': test_paso
        })

    # ------------------------------------------------------------
    # PRUEBA C: Consulta embebida en página 2 (búsqueda)
    # ------------------------------------------------------------
    with app.test_client() as cliente:
        # Aseguramos que el contacto exista
        with app.app_context():
            if not Contacto.query.filter_by(nombre='Test_Funcional').first():
                c = Contacto(nombre='Test_Funcional', telefono='123456789', correo='test@example.com')
                db.session.add(c)
                db.session.commit()

        response = cliente.get('/contactos?busqueda=Test_Funcional')
        test_paso = response.status_code == 200 and b'Test_Funcional' in response.data and b'123456789' in response.data
        resultados.append({
            'id': 'C',
            'nombre': 'Consulta embebida en página 2',
            'descripcion': 'Busca "Test_Funcional" y verifica que aparezca en la tabla con su teléfono.',
            'resultado': f'Código {response.status_code}, datos encontrados en la página' if test_paso else f'Código {response.status_code}, datos no encontrados',
            'estado': 'PASÓ ✅' if test_paso else 'FALLÓ ❌',
            'paso': test_paso
        })

    # ------------------------------------------------------------
    # PRUEBA D: Registro desde el módulo principal (directo con modelo)
    # ------------------------------------------------------------
    with app.app_context():
        try:
            nuevo = Contacto(
                nombre='Test_ModuloPrincipal',
                telefono='987654321',
                correo='modulo@example.com'
            )
            db.session.add(nuevo)
            db.session.commit()
            consulta = Contacto.query.filter_by(nombre='Test_ModuloPrincipal').first()
            test_paso = consulta is not None and consulta.telefono == '987654321'
            resultados.append({
                'id': 'D',
                'nombre': 'Registro desde el módulo principal',
                'descripcion': 'Crea un contacto directamente con el modelo y verifica que se guardó.',
                'resultado': 'Contacto guardado y recuperado correctamente' if test_paso else 'El contacto no se guardó o no se recuperó',
                'estado': 'PASÓ ✅' if test_paso else 'FALLÓ ❌',
                'paso': test_paso
            })
        except Exception as e:
            resultados.append({
                'id': 'D',
                'nombre': 'Registro desde el módulo principal',
                'descripcion': 'Crea un contacto directamente con el modelo.',
                'resultado': f'Error inesperado: {str(e)}',
                'estado': 'ERROR ⚠️',
                'paso': False
            })

    # ------------------------------------------------------------
    # PRUEBA E: Consulta desde el módulo principal
    # ------------------------------------------------------------
    with app.app_context():
        try:
            c = Contacto(nombre='Test_Query', telefono='111222333', correo='query@example.com')
            db.session.add(c)
            db.session.commit()
            encontrados = Contacto.query.filter(Contacto.nombre.like('%Query%')).all()
            test_paso = len(encontrados) > 0 and encontrados[0].correo == 'query@example.com'
            resultados.append({
                'id': 'E',
                'nombre': 'Consulta desde el módulo principal',
                'descripcion': 'Inserta y luego consulta usando filtros con like.',
                'resultado': f'Se encontraron {len(encontrados)} registro(s), correo correcto' if test_paso else f'No se encontró el registro o correo incorrecto',
                'estado': 'PASÓ ✅' if test_paso else 'FALLÓ ❌',
                'paso': test_paso
            })
        except Exception as e:
            resultados.append({
                'id': 'E',
                'nombre': 'Consulta desde el módulo principal',
                'descripcion': 'Inserta y consulta usando filtros.',
                'resultado': f'Error inesperado: {str(e)}',
                'estado': 'ERROR ⚠️',
                'paso': False
            })

    # Limpiar datos de prueba después de las pruebas
    with app.app_context():
        Contacto.query.filter(Contacto.nombre.like('Test_%')).delete()
        db.session.commit()

    # Si se solicita JSON expresamente, se devuelve el formato original
    if request.headers.get('Accept') == 'application/json' or request.args.get('format') == 'json':
        total = len(resultados)
        pasadas = sum(1 for r in resultados if r['paso'])
        return jsonify({
            'total_tests': total,
            'passed': pasadas,
            'failures': total - pasadas,
            'errors': 0,
            'details': [r for r in resultados if not r['paso']]
        })

    # Construir HTML descriptivo
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resultados de Pruebas Funcionales</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">🧪 Pruebas Funcionales del Directorio de Contactos</h1>
            <div class="card shadow">
                <div class="card-body">
                    <table class="table table-striped align-middle">
                        <thead class="table-dark">
                            <tr>
                                <th>Prueba</th>
                                <th>Descripción</th>
                                <th>Resultado concreto</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    for r in resultados:
        html += f"""
                            <tr>
                                <td><strong>{r['id']}: {r['nombre']}</strong></td>
                                <td>{r['descripcion']}</td>
                                <td>{r['resultado']}</td>
                                <td><span class="badge {'bg-success' if r['paso'] else 'bg-danger'} fs-6">{r['estado']}</span></td>
                            </tr>
        """
    total = len(resultados)
    pasadas = sum(1 for r in resultados if r['paso'])
    html += f"""
                        </tbody>
                    </table>
                    <div class="alert alert-info mt-3">
                        <strong>Resumen:</strong> {pasadas} de {total} pruebas pasaron correctamente.
                    </div>
                    <a href="/test?format=json" class="btn btn-outline-secondary btn-sm">Ver JSON</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# ============= CREAR TABLAS =============
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
