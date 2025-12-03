import json
import pytest
import sys
import os

# Asegurar que podemos importar los módulos del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy.exc import IntegrityError

from models import Visitante, db

def test_registrar_visitante_valido(test_client, init_database):
    """Test para registrar un visitante válido"""
    # Datos del visitante a registrar
    nuevo_visitante = {
        'numero_identificacion': '11223344',
        'tipo_identificacion': 'DNI',
        'nombres': 'María',
        'apellidos': 'González',
        'tipo_visitante': 'Personal'
    }
    
    # Realizar la solicitud POST
    response = test_client.post(
        '/api/visitantes',
        data=json.dumps(nuevo_visitante),
        content_type='application/json'
    )
    
    # Verificar la respuesta
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['message'] == 'Visitante registrado exitosamente'
    assert 'data' in data
    assert data['data']['nombres'] == 'María'
    assert data['data']['apellidos'] == 'González'

def test_registrar_visitante_sin_campos_obligatorios(test_client, init_database):
    """Test para validar que se requieren los campos obligatorios"""
    # Datos del visitante sin campos obligatorios
    visitante_invalido = {
        'numero_identificacion': '11223344',
        # Falta tipo_identificacion
        'nombres': 'María',
        'apellidos': 'González',
        'tipo_visitante': 'Personal'
    }
    
    response = test_client.post(
        '/api/visitantes',
        data=json.dumps(visitante_invalido),
        content_type='application/json'
    )
    
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'El campo tipo_identificacion es requerido' in data['error']

def test_registrar_visitante_empresarial_sin_empresa(test_client, init_database):
    """Test para validar que los visitantes empresariales requieren el campo empresa_representa"""
    visitante_empresarial = {
        'numero_identificacion': '20123456789',
        'tipo_identificacion': 'RUC',
        'nombres': 'Empresa',
        'apellidos': 'S.A.',
        'tipo_visitante': 'Empresarial'
        # Falta empresa_representa
    }
    
    response = test_client.post(
        '/api/visitantes',
        data=json.dumps(visitante_empresarial),
        content_type='application/json'
    )
    
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'El campo \'empresa_representa\' es requerido para visitantes empresariales' in data['error']

def test_registrar_visitante_duplicado(test_client, init_database):
    """Test para evitar la creación de visitantes duplicados"""
    # Insertar un visitante primero
    visitante = {
        'numero_identificacion': '98765432',
        'tipo_identificacion': 'DNI',
        'nombres': 'Carlos',
        'apellidos': 'López',
        'tipo_visitante': 'Personal'
    }
    
    # Primera inserción (debería funcionar)
    response1 = test_client.post(
        '/api/visitantes',
        data=json.dumps(visitante),
        content_type='application/json'
    )
    assert response1.status_code == 201
    
    # Segunda inserción con el mismo número de identificación (debería fallar)
    response2 = test_client.post(
        '/api/visitantes',
        data=json.dumps(visitante),
        content_type='application/json'
    )
    
    data = json.loads(response2.data)
    assert response2.status_code == 409
    assert data['status'] == 'error'
    assert 'visitante registrado' in data['error']

def test_tipo_visitante_invalido(test_client, init_database):
    """Test para validar que el tipo de visitante sea válido"""
    visitante_invalido = {
        'numero_identificacion': '11223344',
        'tipo_identificacion': 'DNI',
        'nombres': 'Ana',
        'apellidos': 'Martínez',
        'tipo_visitante': 'Invitado'  # Tipo inválido
    }
    
    response = test_client.post(
        '/api/visitantes',
        data=json.dumps(visitante_invalido),
        content_type='application/json'
    )
    
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert "El campo 'tipo_visitante' debe ser 'Empresarial' o 'Personal'" in data['error']


def test_registrar_visitante_integrity_error(test_client, init_database, monkeypatch):
    class DummyQuery:
        def filter_by(self, **kwargs):
            return self

        def first(self):
            return None

    monkeypatch.setattr(Visitante, 'query', DummyQuery())

    def raise_integrity():
        raise IntegrityError('stmt', 'params', Exception('Duplicate entry'))

    monkeypatch.setattr(db.session, 'commit', raise_integrity)

    visitante = {
        'numero_identificacion': '44556677',
        'tipo_identificacion': 'DNI',
        'nombres': 'Pedro',
        'apellidos': 'Ramírez',
        'tipo_visitante': 'Personal'
    }

    response = test_client.post(
        '/api/visitantes',
        data=json.dumps(visitante),
        content_type='application/json'
    )

    data = json.loads(response.data)
    assert response.status_code == 409
    assert data['status'] == 'error'
    assert 'identificación ya está registrado' in data['error']


def test_registrar_visitante_unexpected_error(test_client, init_database, monkeypatch):
    class FailingQuery:
        def filter_by(self, **kwargs):
            raise RuntimeError('db down')

    monkeypatch.setattr(Visitante, 'query', FailingQuery())

    visitante = {
        'numero_identificacion': '99887766',
        'tipo_identificacion': 'DNI',
        'nombres': 'Lucía',
        'apellidos': 'Soto',
        'tipo_visitante': 'Personal'
    }

    response = test_client.post(
        '/api/visitantes',
        data=json.dumps(visitante),
        content_type='application/json'
    )

    data = json.loads(response.data)
    assert response.status_code == 500
    assert data['status'] == 'error'
    assert 'Error en el servidor' in data['error']

