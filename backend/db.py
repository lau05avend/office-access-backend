from models import db

def init_db(app):
    """Inicializa la base de datos creando todas las tablas"""
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada correctamente")
