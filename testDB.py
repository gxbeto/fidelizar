from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/fidelizacion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

def test_connection():
    with app.app_context():
        try:
            # Usa el contexto de conexión de SQLAlchemy
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                for row in result:
                    print("Conexión a la base de datos exitosa:", row)
            return True
        except Exception as e:
            print("Error al conectar a la base de datos:", str(e))
            return False

if __name__ == '__main__':
    test_connection()

