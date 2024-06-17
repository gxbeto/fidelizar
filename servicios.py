# 8. Servicios
# 	- carga de puntos (POST):se recibe el identificador de cliente y el monto
# 	de la operación, y se asigna los puntos (genera datos con la estructura
# 	del punto 5)
	
# 	- utilizar puntos (POST):se recibe el identificador del cliente y el identificador del 
# 	concepto de uso y se descuenta dicho puntaje al cliente registrando el uso de puntos 
# 	(genera datos con la estructura del punto 6 y actualiza la del punto 5) 
# 	o además debe enviar un correo electrónico al cliente como comprobante 
	
# 	- consultar cuantos puntos equivale a un monto X (GET):
# 	es un servicio informativo que devuelve la cantidad de puntos equivalente al monto 
# 	proporcionado como parámetro utilizando la configuración del punto 3


from flask import Blueprint, request, jsonify
from extensions import db
from models import BolsaPuntos, Cliente, ConceptoUso

servicios_bp = Blueprint('servicios', __name__, url_prefix='/api/servicios')

@servicios_bp.route('/cargar_puntos', methods=['POST'])
def cargar_puntos():
    """Servicio para cargar puntos"""
    data = request.json
    cliente_id = data['cliente_id']
    monto_operacion = data['monto_operacion']

    # Aquí deberías implementar la lógica para calcular los puntos basados en las reglas
    # Por ahora, asumimos una lógica simple
    puntos_asignados = monto_operacion // 1000  # Ejemplo: 1 punto por cada 1000 unidades de monto

    nueva_bolsa = BolsaPuntos(
        cliente_id=cliente_id,
        fecha_asignacion=data['fecha_asignacion'],
        fecha_caducidad=data['fecha_caducidad'],
        puntaje_asignado=puntos_asignados,
        puntaje_utilizado=0,
        saldo_puntos=puntos_asignados,
        monto_operacion=monto_operacion
    )
    db.session.add(nueva_bolsa)
    db.session.commit()
    return jsonify({"mensaje": "Puntos cargados exitosamente"}), 201

@servicios_bp.route('/utilizar_puntos', methods=['POST'])
def utilizar_puntos():
    """Servicio para utilizar puntos"""
    data = request.json
    cliente_id = data['cliente_id']
    concepto_uso_id = data['concepto_uso_id']
    puntos_a_utilizar = data['puntos_a_utilizar']

    # Aquí deberías implementar la lógica para utilizar los puntos siguiendo el esquema FIFO
    # Por ahora, asumimos una lógica simple
    bolsas = BolsaPuntos.query.filter_by(cliente_id=cliente_id).order_by(BolsaPuntos.fecha_asignacion).all()

    puntos_restantes = puntos_a_utilizar
    for bolsa in bolsas:
        if bolsa.saldo_puntos >= puntos_restantes:
            bolsa.puntaje_utilizado += puntos_restantes
            bolsa.saldo_puntos -= puntos_restantes
            puntos_restantes = 0
            break
        else:
            puntos_restantes -= bolsa.saldo_puntos
            bolsa.puntaje_utilizado += bolsa.saldo_puntos
            bolsa.saldo_puntos = 0
    
    if puntos_restantes > 0:
        return jsonify({"mensaje": "No hay suficientes puntos para utilizar"}), 400

    db.session.commit()

    nueva_cabecera = UsoPuntosCabecera(
        cliente_id=cliente_id,
        puntaje_utilizado=puntos_a_utilizar,
        fecha=data['fecha'],
        concepto_uso_id=concepto_uso_id
    )
    db.session.add(nueva_cabecera)
    db.session.commit()

    return jsonify({"mensaje": "Puntos utilizados exitosamente"}), 201

@servicios_bp.route('/consultar_puntos', methods=['GET'])
def consultar_puntos():
    """Servicio para consultar puntos por monto"""
    monto = request.args.get('monto', type=int)

    # Aquí deberías implementar la lógica para calcular los puntos basados en las reglas
    # Por ahora, asumimos una lógica simple
    puntos_equivalentes = monto // 1000  # Ejemplo: 1 punto por cada 1000 unidades de monto

    return jsonify({"puntos_equivalentes": puntos_equivalentes}), 200
