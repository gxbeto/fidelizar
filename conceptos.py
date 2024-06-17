from flask import Blueprint, request, jsonify
from extensions import db
from models import ConceptoUso

conceptos_bp = Blueprint('conceptos', __name__, url_prefix='/api/conceptos')

@conceptos_bp.route('', methods=['POST'])
def create_concepto():
    data = request.json
    nuevo_concepto = ConceptoUso(
        descripcion=data['descripcion'],
        puntos_requeridos=data['puntos_requeridos']
    )
    db.session.add(nuevo_concepto)
    db.session.commit()
    return jsonify({"mensaje": "Concepto creado exitosamente"}), 201

@conceptos_bp.route('', methods=['GET'])
def get_conceptos():
    conceptos = ConceptoUso.query.all()
    resultado = [{"id": concepto.id, "descripcion": concepto.descripcion, "puntos_requeridos": concepto.puntos_requeridos} for concepto in conceptos]
    return jsonify(resultado)
