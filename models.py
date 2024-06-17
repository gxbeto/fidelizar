from extensions import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    numero_documento = db.Column(db.String(50))
    tipo_documento = db.Column(db.String(50))
    nacionalidad = db.Column(db.String(50))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)

class ConceptoUso(db.Model):
    __tablename__ = 'conceptouso'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255))
    puntos_requeridos = db.Column(db.Integer)

class ReglaAsignacion(db.Model):
    __tablename__ = 'reglaasignacion'
    id = db.Column(db.Integer, primary_key=True)
    limite_inferior = db.Column(db.Integer)
    limite_superior = db.Column(db.Integer)
    monto_equivalencia = db.Column(db.Integer)

class VencimientoPuntos(db.Model):
    __tablename__ = 'vencimientopuntos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    dias_duracion = db.Column(db.Integer)

class BolsaPuntos(db.Model):
    __tablename__ = 'bolsapuntos'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    fecha_asignacion = db.Column(db.Date)
    fecha_caducidad = db.Column(db.Date)
    puntaje_asignado = db.Column(db.Integer)
    puntaje_utilizado = db.Column(db.Integer)
    saldo_puntos = db.Column(db.Integer)
    monto_operacion = db.Column(db.Numeric)

class UsoPuntosCabecera(db.Model):
    __tablename__ = 'usopuntoscabecera'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    puntaje_utilizado = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    concepto_uso_id = db.Column(db.Integer, db.ForeignKey('conceptouso.id'))

class UsoPuntosDetalle(db.Model):
    __tablename__ = 'usopuntosdetalle'
    id = db.Column(db.Integer, primary_key=True)
    cabecera_id = db.Column(db.Integer, db.ForeignKey('usopuntoscabecera.id'))
    puntaje_utilizado = db.Column(db.Integer)
    bolsa_puntos_id = db.Column(db.Integer, db.ForeignKey('bolsapuntos.id'))
