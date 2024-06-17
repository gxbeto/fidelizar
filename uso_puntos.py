from flask import Blueprint, request, jsonify
from extensions import db
from models import UsoPuntosCabecera, UsoPuntosDetalle

uso_puntos_bp = Blueprint('uso_puntos', __name__, url_prefix='/api/uso_puntos')

@uso_puntos_bp.route('', methods=['POST'])
def create_uso_puntos():
    data = request.json
    nuevo_uso = UsoPuntosCabecera(
        cliente_id=data['cliente_id'],
        puntaje_utilizado=data['puntaje_utilizado'],
        fecha=data['fecha'],
        concepto_uso_id=data['concepto_uso_id']
    )
    db.session.add(nuevo_uso)
    db.session.commit()

    detalles = data.get('detalles', [])
    for detalle in detalles:
        nuevo_detalle = UsoPuntosDetalle(
            cabecera_id=nuevo_uso.id,
            puntaje_utilizado=detalle['puntaje_utilizado'],
            bolsa_puntos_id=detalle['bolsa_puntos_id']
        )
        db.session.add(nuevo_detalle)
    db.session.commit()

    return jsonify({"mensaje": "Uso de puntos creado exitosamente"}), 201

@uso_puntos_bp.route('', methods=['GET'])
def get_uso_puntos():
    usos = UsoPuntosCabecera.query.all()
    resultado = [{"id": uso.id, "cliente_id": uso.cliente_id, "puntaje_utilizado": uso.puntaje_utilizado, "fecha": uso.fecha, "concepto_uso_id": uso.concepto_uso_id} for uso in usos]
    return jsonify(resultado)
