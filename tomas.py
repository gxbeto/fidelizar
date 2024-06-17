from flask import Blueprint, jsonify

tomas_bp = Blueprint('tomas', __name__)

@tomas_bp.route('/mensaje', methods=['GET'])
def obtener_mensaje():
    return jsonify({"mensaje": "Si no lo veo, no lo creo"}), 200
