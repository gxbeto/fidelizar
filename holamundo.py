""" from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/holamundo', methods=['GET'])
def holamundo():
    return jsonify({"mensaje": "bueeeeeeno por fin funciona!!!!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=9092) """


from app import db

def test_connection():
    try:
        # Ejecuta una consulta simple para probar la conexión
        result = db.engine.execute("SELECT 1")
        for row in result:
            print("Conexión a la base de datos exitosa:", row)
        return True
    except Exception as e:
        print("Error al conectar a la base de datos:", str(e))
        return False

if __name__ == '__main__':
    print("test_connection:")
    test_connection()

