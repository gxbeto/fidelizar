from datetime import datetime
from app import db
from models import BolsaPuntos

def update_expired_points():
    now = datetime.now().date()
    bolsas = BolsaPuntos.query.filter(BolsaPuntos.fecha_caducidad < now).all()
    for bolsa in bolsas:
        if bolsa.saldo_puntos > 0:
            bolsa.puntaje_utilizado += bolsa.saldo_puntos
            bolsa.saldo_puntos = 0
    db.session.commit()
    print("Actualización de puntos vencidos completada")

if __name__ == '__main__':
    with app.app_context():
        update_expired_points()
