import os
import re
from flask import Flask, render_template, request, redirect, flash, url_for
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

# ============= CREAR TABLAS =============
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
