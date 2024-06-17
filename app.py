from flask import Flask, jsonify
from sqlalchemy import text
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/fidelizacion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db.init_app(app)

# Importar y registrar Blueprints
from clientes import clientes_bp
from conceptos import conceptos_bp
from reglas import reglas_bp
from vencimientos import vencimientos_bp
from bolsas import bolsas_bp
from uso_puntos import uso_puntos_bp
from consultas import consultas_bp
from servicios import servicios_bp

app.register_blueprint(clientes_bp)
app.register_blueprint(conceptos_bp, url_prefix='/api/conceptos')
app.register_blueprint(reglas_bp, url_prefix='/api/reglas')
app.register_blueprint(vencimientos_bp, url_prefix='/api/vencimientos')
app.register_blueprint(bolsas_bp, url_prefix='/api/bolsas')
app.register_blueprint(uso_puntos_bp, url_prefix='/api/uso_puntos')
app.register_blueprint(consultas_bp, url_prefix='/api/consultas')
app.register_blueprint(servicios_bp, url_prefix='/api/servicios')

# Ruta para probar la conexión a la base de datos
@app.route('/api/test_db', methods=['GET'])
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            for row in result:
                return jsonify({"mensaje": "Conexión a la base de datos exitosa"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=9092)
