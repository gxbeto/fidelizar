from flask import Blueprint, request, jsonify
from extensions import db
from models import BolsaPuntos

bolsas_bp = Blueprint('bolsas', __name__, url_prefix='/api/bolsas')

@bolsas_bp.route('', methods=['POST'])
def create_bolsa():
    data = request.json
    nueva_bolsa = BolsaPuntos(
        cliente_id=data['cliente_id'],
        fecha_asignacion=data['fecha_asignacion'],
        fecha_caducidad=data['fecha_caducidad'],
        puntaje_asignado=data['puntaje_asignado'],
        puntaje_utilizado=data['puntaje_utilizado'],
        saldo_puntos=data['saldo_puntos'],
        monto_operacion=data['monto_operacion']
    )
    db.session.add(nueva_bolsa)
    db.session.commit()
    return jsonify({"mensaje": "Bolsa creada exitosamente"}), 201

@bolsas_bp.route('', methods=['GET'])
def get_bolsas():
    bolsas = BolsaPuntos.query.all()
    resultado = [{"id": bolsa.id, "cliente_id": bolsa.cliente_id, "fecha_asignacion": bolsa.fecha_asignacion, "fecha_caducidad": bolsa.fecha_caducidad, "puntaje_asignado": bolsa.puntaje_asignado, "puntaje_utilizado": bolsa.puntaje_utilizado, "saldo_puntos": bolsa.saldo_puntos, "monto_operacion": bolsa.monto_operacion} for bolsa in bolsas]
    return jsonify(resultado)
