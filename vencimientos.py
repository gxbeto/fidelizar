from flask import Blueprint, request, jsonify
from extensions import db
from models import VencimientoPuntos

vencimientos_bp = Blueprint('vencimientos', __name__, url_prefix='/api/vencimientos')

@vencimientos_bp.route('', methods=['POST'])
def create_vencimiento():
    data = request.json
    nuevo_vencimiento = VencimientoPuntos(
        fecha_inicio=data['fecha_inicio'],
        fecha_fin=data['fecha_fin'],
        dias_duracion=data['dias_duracion']
    )
    db.session.add(nuevo_vencimiento)
    db.session.commit()
    return jsonify({"mensaje": "Vencimiento creado exitosamente"}), 201

@vencimientos_bp.route('', methods=['GET'])
def get_vencimientos():
    vencimientos = VencimientoPuntos.query.all()
    resultado = [{"id": vencimiento.id, "fecha_inicio": vencimiento.fecha_inicio, "fecha_fin": vencimiento.fecha_fin, "dias_duracion": vencimiento.dias_duracion} for vencimiento in vencimientos]
    return jsonify(resultado)
