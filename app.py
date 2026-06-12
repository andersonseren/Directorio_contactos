import os
import re
import unittest
from io import StringIO
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

# ============= RUTA DE PRUEBAS FUNCIONALES =============
@app.route('/test')
def run_functional_tests():
    """Ejecuta el caso de prueba funcional y devuelve los resultados."""
    class FunctionalTestCase(unittest.TestCase):
        def setUp(self):
            self.app = app.test_client()
            self.app.testing = True
            # Limpiar datos de prueba previos
            with app.app_context():
                Contacto.query.filter(Contacto.nombre.like('Test_%')).delete()
                db.session.commit()

        def tearDown(self):
            with app.app_context():
                Contacto.query.filter(Contacto.nombre.like('Test_%')).delete()
                db.session.commit()

        def test_home_page(self):
            """a) Home Page – Index"""
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Contactos', response.data)

        def test_registration_page(self):
            """b) Registro de usuario (GET) - Corregido: busca 'Registrar' en lugar de 'Registro'"""
            response = self.app.get('/registro')
            self.assertEqual(response.status_code, 200)
            # En la plantilla el enlace y el título usan "Registrar", no "Registro"
            self.assertIn(b'Registrar', response.data)

        def test_registration_submit(self):
            """b) Registro de usuario (POST)"""
            data = {
                'nombre': 'Test_Funcional',
                'telefono': '123456789',
                'correo': 'test@example.com'
            }
            response = self.app.post('/registro', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Contacto registrado exitosamente', response.data)

        def test_embedded_search(self):
            """c) Consulta de información embebida en página 2"""
            # Asegurar que existe el contacto de prueba
            with app.app_context():
                if not Contacto.query.filter_by(nombre='Test_Funcional').first():
                    c = Contacto(nombre='Test_Funcional', telefono='123456789', correo='test@example.com')
                    db.session.add(c)
                    db.session.commit()
            # Búsqueda en /contactos?busqueda=Test
            response = self.app.get('/contactos?busqueda=Test_Funcional')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test_Funcional', response.data)
            self.assertIn(b'123456789', response.data)

        def test_register_from_main_module(self):
            """d) Registro desde el módulo principal"""
            with app.app_context():
                nuevo = Contacto(
                    nombre='Test_ModuloPrincipal',
                    telefono='987654321',
                    correo='modulo@example.com'
                )
                db.session.add(nuevo)
                db.session.commit()
                consulta = Contacto.query.filter_by(nombre='Test_ModuloPrincipal').first()
                self.assertIsNotNone(consulta)
                self.assertEqual(consulta.telefono, '987654321')

        def test_query_from_main_module(self):
            """e) Consulta desde el módulo principal"""
            with app.app_context():
                c = Contacto(nombre='Test_Query', telefono='111222333', correo='query@example.com')
                db.session.add(c)
                db.session.commit()
                encontrado = Contacto.query.filter(Contacto.nombre.like('%Query%')).all()
                self.assertTrue(len(encontrado) > 0)
                self.assertEqual(encontrado[0].correo, 'query@example.com')

    # Ejecutar pruebas y capturar resultados
    suite = unittest.TestLoader().loadTestsFromTestCase(FunctionalTestCase)
    stream = StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)

    # Construir informe JSON
    tests_info = []
    for test_case, reason in result.failures:
        tests_info.append({'test': str(test_case), 'status': 'FAIL', 'reason': reason})
    for test_case, reason in result.errors:
        tests_info.append({'test': str(test_case), 'status': 'ERROR', 'reason': reason})

    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total - failures - errors

    return jsonify({
        'total_tests': total,
        'passed': passed,
        'failures': failures,
        'errors': errors,
        'details': tests_info
    })

# ============= CREAR TABLAS =============
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
