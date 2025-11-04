from flask import Blueprint, request, jsonify
from models import db, Visitante
from sqlalchemy.exc import IntegrityError

visitantes_bp = Blueprint('visitantes', __name__)

@visitantes_bp.route('/api/visitantes', methods=['POST'])
def registrar_visitante():
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['numero_identificacion', 'tipo_identificacion', 'nombres', 'apellidos', 'tipo_visitante']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'error': f'El campo {field} es requerido',
                    'status': 'error',
                    'status_code': 400
                }), 400
        
        # Validar tipo de visitante
        tipo_visitante = data['tipo_visitante']
        if tipo_visitante not in ['Empresarial', 'Personal']:
            return jsonify({
                'error': "El campo 'tipo_visitante' debe ser 'Empresarial' o 'Personal'",
                'status': 'error',
                'status_code': 400
            }), 400
        
        # Validar empresa si es visitante empresarial
        if tipo_visitante == 'Empresarial' and not data.get('empresa_representa'):
            return jsonify({
                'error': "El campo 'empresa_representa' es requerido para visitantes empresariales",
                'status': 'error',
                'status_code': 400
            }), 400
        
        # Verificar si ya existe un visitante con ese número de identificación
        visitante_existente = Visitante.query.filter_by(numero_identificacion=data['numero_identificacion']).first()
        if visitante_existente:
            return jsonify({
                'error': f"Ya existe un visitante registrado con el número de identificación {data['numero_identificacion']}",
                'status': 'error',
                'status_code': 409
            }), 409
        
        # Crear nuevo visitante usando ORM
        nuevo_visitante = Visitante(
            numero_identificacion=data['numero_identificacion'],
            tipo_identificacion=data['tipo_identificacion'],
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            tipo_visitante=tipo_visitante,
            empresa_representa=data.get('empresa_representa')
        )
        
        # Guardar en la base de datos
        db.session.add(nuevo_visitante)
        db.session.commit()
        
        return jsonify({
            'message': 'Visitante registrado exitosamente',
            'status': 'success',
            'status_code': 201,
            'data': nuevo_visitante.to_dict()
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        # Manejar error de duplicado en caso de que la validación previa falle
        if 'Duplicate entry' in str(e) or 'UNIQUE constraint' in str(e):
            return jsonify({
                'error': 'El número de identificación ya está registrado',
                'status': 'error',
                'status_code': 409
            }), 409
        return jsonify({
            'error': 'Error de integridad en la base de datos',
            'status': 'error',
            'status_code': 500
        }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Error en el servidor: {str(e)}',
            'status': 'error',
            'status_code': 500
        }), 500