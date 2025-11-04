from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Visitante(db.Model):
    __tablename__ = "visitantes"
    
    id_visitante = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_identificacion = db.Column(db.String(20), nullable=False)
    tipo_identificacion = db.Column(db.String(10), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    tipo_visitante = db.Column(db.Enum('Empresarial', 'Personal', name='tipo_visitante_enum'), nullable=False)
    empresa_representa = db.Column(db.String(100), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convierte el modelo a diccionario para JSON"""
        return {
            'id_visitante': self.id_visitante,
            'numero_identificacion': self.numero_identificacion,
            'tipo_identificacion': self.tipo_identificacion,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'tipo_visitante': self.tipo_visitante,
            'empresa_representa': self.empresa_representa,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }
    
    def __repr__(self):
        return f'<Visitante {self.nombres} {self.apellidos}>'