from flask import Blueprint, request, jsonify
from extensions import db
from models import Cliente

clientes_bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')

@clientes_bp.route('', methods=['POST'])
def create_cliente():
    data = request.json
    nuevo_cliente = Cliente(
        nombre=data['nombre'],
        apellido=data['apellido'],
        numero_documento=data['numero_documento'],
        tipo_documento=data['tipo_documento'],
        nacionalidad=data['nacionalidad'],
        email=data['email'],
        telefono=data['telefono'],
        fecha_nacimiento=data['fecha_nacimiento']
    )
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente creado exitosamente"}), 201

@clientes_bp.route('', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    resultado = [{"id": cliente.id, "nombre": cliente.nombre, "apellido": cliente.apellido, "numero_documento": cliente.numero_documento, "tipo_documento": cliente.tipo_documento, "nacionalidad": cliente.nacionalidad, "email": cliente.email, "telefono": cliente.telefono, "fecha_nacimiento": cliente.fecha_nacimiento} for cliente in clientes]
    return jsonify(resultado)

@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    resultado = {"id": cliente.id, "nombre": cliente.nombre, "apellido": cliente.apellido, "numero_documento": cliente.numero_documento, "tipo_documento": cliente.tipo_documento, "nacionalidad": cliente.nacionalidad, "email": cliente.email, "telefono": cliente.telefono, "fecha_nacimiento": cliente.fecha_nacimiento}
    return jsonify(resultado)

@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.json
    cliente.nombre = data['nombre']
    cliente.apellido = data['apellido']
    cliente.numero_documento = data['numero_documento']
    cliente.tipo_documento = data['tipo_documento']
    cliente.nacionalidad = data['nacionalidad']
    cliente.email = data['email']
    cliente.telefono = data['telefono']
    cliente.fecha_nacimiento = data['fecha_nacimiento']
    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado exitosamente"})

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado exitosamente"})
