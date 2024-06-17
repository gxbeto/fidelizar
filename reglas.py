from flask import Blueprint, request, jsonify
from extensions import db
from models import ReglaAsignacion

reglas_bp = Blueprint('reglas', __name__, url_prefix='/api/reglas')

@reglas_bp.route('', methods=['POST'])
def create_regla():
    data = request.json
    nueva_regla = ReglaAsignacion(
        limite_inferior=data['limite_inferior'],
        limite_superior=data['limite_superior'],
        monto_equivalencia=data['monto_equivalencia']
    )
    db.session.add(nueva_regla)
    db.session.commit()
    return jsonify({"mensaje": "Regla creada exitosamente"}), 201

@reglas_bp.route('', methods=['GET'])
def get_reglas():
    reglas = ReglaAsignacion.query.all()
    resultado = [{"id": regla.id, "limite_inferior": regla.limite_inferior, "limite_superior": regla.limite_superior, "monto_equivalencia": regla.monto_equivalencia} for regla in reglas]
    return jsonify(resultado)
