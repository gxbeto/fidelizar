from flask import Blueprint, request, jsonify
from extensions import db
from sqlalchemy import text

# 7. Consultas (GET)
# 	Este módulo contempla la consulta para el desarrollo de reportes.
# 	Las consultas a proveer son:
# 	consulta_uso_puntos: uso de puntos por: concepto de uso, fecha de uso, cliente
# 	consulta_bolsas: bolsa de puntos por: cliente, rango de puntos
# 	consulta_puntos_a_vencer: clientes con puntos a vencer en x días
# 	consulta_xnombre: consulta de clientes por: nombre (aproximación), apellido (aproximación), cumpleaños

consultas_bp = Blueprint('consultas', __name__, url_prefix='/api/consultas')

@consultas_bp.route('/uso_puntos', methods=['GET'])
def consulta_uso_puntos():
    concepto_uso = request.args.get('concepto_uso')
    fecha_uso = request.args.get('fecha_uso')
    cliente_id = request.args.get('cliente_id')
    formato = request.args.get('Formato', 'TXT').upper()

    query = text("""
    SELECT 
        u.id AS uso_puntos_id,
        u.cliente_id,
        c.nombre AS cliente_nombre,
        c.apellido AS cliente_apellido,
        u.fecha,
        u.puntaje_utilizado,
        cu.descripcion AS concepto_uso
    FROM 
        usopuntoscabecera u
    JOIN 
        cliente c ON u.cliente_id = c.id
    JOIN 
        conceptouso cu ON u.concepto_uso_id = cu.id
    WHERE 
        (:concepto_uso IS NULL OR cu.descripcion = :concepto_uso)
        AND (:fecha_uso IS NULL OR u.fecha = :fecha_uso)
        AND (:cliente_id IS NULL OR c.id = :cliente_id);
    """)

    results = db.session.execute(query, {'concepto_uso': concepto_uso, 'fecha_uso': fecha_uso, 'cliente_id': cliente_id}).fetchall()

    if formato == 'JSON':
        # Formatear salida en JSON
        response = []
        for row in results:
            response.append({
                "uso_puntos_id": row.uso_puntos_id,
                "cliente_id": row.cliente_id,
                "cliente_nombre": row.cliente_nombre,
                "cliente_apellido": row.cliente_apellido,
                "fecha": row.fecha,
                "puntaje_utilizado": row.puntaje_utilizado,
                "concepto_uso": row.concepto_uso
            })
        return jsonify(response), 200
    else:
        # Formatear salida en tabla de texto
        headers = ["uso_puntos_id", "cliente_id", "cliente_nombre", "cliente_apellido", "fecha", "puntaje_utilizado", "concepto_uso"]
        rows = [
            [row.uso_puntos_id, row.cliente_id, row.cliente_nombre, row.cliente_apellido, row.fecha, row.puntaje_utilizado, row.concepto_uso]
            for row in results
        ]

        # Calcular el ancho de cada columna
        column_widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]
        header_row = " | ".join(f"{header:{column_widths[i]}}" for i, header in enumerate(headers))
        separator_row = "-+-".join('-' * width for width in column_widths)
        data_rows = "\n".join(" | ".join(f"{str(item):{column_widths[i]}}" for i, item in enumerate(row)) for row in rows)

        response_str = f"{header_row}\n{separator_row}\n{data_rows}"

        return f"<pre>{response_str}</pre>", 200

@consultas_bp.route('/bolsas', methods=['GET'])
def consulta_bolsas():
    cliente_id = request.args.get('cliente_id')
    puntos_min = request.args.get('puntos_min')
    puntos_max = request.args.get('puntos_max')
    formato = request.args.get('Formato', 'TXT').upper()

    query = text("""
    SELECT 
        b.id AS bolsa_id,
        b.cliente_id,
        c.nombre AS cliente_nombre,
        c.apellido AS cliente_apellido,
        b.fecha_asignacion,
        b.fecha_caducidad,
        b.puntaje_asignado,
        b.puntaje_utilizado,
        b.saldo_puntos,
        b.monto_operacion
    FROM 
        bolsapuntos b
    JOIN 
        cliente c ON b.cliente_id = c.id
    WHERE 
        (:cliente_id IS NULL OR b.cliente_id = :cliente_id)
        AND (:puntos_min IS NULL OR b.saldo_puntos >= :puntos_min)
        AND (:puntos_max IS NULL OR b.saldo_puntos <= :puntos_max);
    """)

    results = db.session.execute(query, {'cliente_id': cliente_id, 'puntos_min': puntos_min, 'puntos_max': puntos_max}).fetchall()

    if formato == 'JSON':
        # Formatear salida en JSON
        response = []
        for row in results:
            response.append({
                "bolsa_id": row.bolsa_id,
                "cliente_id": row.cliente_id,
                "cliente_nombre": row.cliente_nombre,
                "cliente_apellido": row.cliente_apellido,
                "fecha_asignacion": row.fecha_asignacion,
                "fecha_caducidad": row.fecha_caducidad,
                "puntaje_asignado": row.puntaje_asignado,
                "puntaje_utilizado": row.puntaje_utilizado,
                "saldo_puntos": row.saldo_puntos,
                "monto_operacion": row.monto_operacion
            })
        return jsonify(response), 200
    else:
        # Formatear salida en tabla de texto
        headers = ["bolsa_id", "cliente_id", "cliente_nombre", "cliente_apellido", "fecha_asignacion", "fecha_caducidad", "puntaje_asignado", "puntaje_utilizado", "saldo_puntos", "monto_operacion"]
        rows = [
            [row.bolsa_id, row.cliente_id, row.cliente_nombre, row.cliente_apellido, row.fecha_asignacion, row.fecha_caducidad, row.puntaje_asignado, row.puntaje_utilizado, row.saldo_puntos, row.monto_operacion]
            for row in results
        ]

        # Calcular el ancho de cada columna
        column_widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]
        header_row = " | ".join(f"{header:{column_widths[i]}}" for i, header in enumerate(headers))
        separator_row = "-+-".join('-' * width for width in column_widths)
        data_rows = "\n".join(" | ".join(f"{str(item):{column_widths[i]}}" for i, item in enumerate(row)) for row in rows)

        response_str = f"{header_row}\n{separator_row}\n{data_rows}"

        return f"<pre>{response_str}</pre>", 200

@consultas_bp.route('/clientes', methods=['GET'])
def consulta_clientes():
    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    cumpleanos = request.args.get('cumpleanos')
    formato = request.args.get('Formato', 'TXT').upper()

    query = text("""
    SELECT 
        c.id AS cliente_id,
        c.nombre,
        c.apellido,
        c.numero_documento,
        c.tipo_documento,
        c.nacionalidad,
        c.email,
        c.telefono,
        c.fecha_nacimiento
    FROM 
        cliente c
    WHERE 
        (:nombre IS NULL OR c.nombre ILIKE '%' || :nombre || '%')
        AND (:apellido IS NULL OR c.apellido ILIKE '%' || :apellido || '%')
        AND (:cumpleanos IS NULL OR (EXTRACT(MONTH FROM c.fecha_nacimiento) = EXTRACT(MONTH FROM CAST(:cumpleanos AS DATE))
        AND EXTRACT(DAY FROM c.fecha_nacimiento) = EXTRACT(DAY FROM CAST(:cumpleanos AS DATE))));
    """)

    results = db.session.execute(query, {'nombre': nombre, 'apellido': apellido, 'cumpleanos': cumpleanos}).fetchall()

    if formato == 'JSON':
        # Formatear salida en JSON
        response = []
        for row in results:
            response.append({
                "cliente_id": row.cliente_id,
                "nombre": row.nombre,
                "apellido": row.apellido,
                "numero_documento": row.numero_documento,
                "tipo_documento": row.tipo_documento,
                "nacionalidad": row.nacionalidad,
                "email": row.email,
                "telefono": row.telefono,
                "fecha_nacimiento": row.fecha_nacimiento
            })
        return jsonify(response), 200
    else:
        # Formatear salida en tabla de texto
        headers = ["cliente_id", "nombre", "apellido", "numero_documento", "tipo_documento", "nacionalidad", "email", "telefono", "fecha_nacimiento"]
        rows = [
            [row.cliente_id, row.nombre, row.apellido, row.numero_documento, row.tipo_documento, row.nacionalidad, row.email, row.telefono, row.fecha_nacimiento]
            for row in results
        ]

        # Calcular el ancho de cada columna
        column_widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]
        header_row = " | ".join(f"{header:{column_widths[i]}}" for i, header in enumerate(headers))
        separator_row = "-+-".join('-' * width for width in column_widths)
        data_rows = "\n".join(" | ".join(f"{str(item):{column_widths[i]}}" for i, item in enumerate(row)) for row in rows)

        response_str = f"{header_row}\n{separator_row}\n{data_rows}"

        return f"<pre>{response_str}</pre>", 200


    dias = request.args.get('dias', type=int)
    formato = request.args.get('Formato', 'TXT').upper()

    query = text("""
    SELECT 
        c.id AS cliente_id,
        c.nombre,
        c.apellido,
        c.numero_documento,
        c.tipo_documento,
        c.nacionalidad,
        c.email,
        c.telefono,
        c.fecha_nacimiento,
        b.id AS bolsa_id,
        b.fecha_asignacion,
        b.fecha_caducidad,
        b.saldo_puntos
    FROM 
        cliente c
    JOIN 
        bolsapuntos b ON c.id = b.cliente_id
    WHERE 
        (b.fecha_caducidad IS NULL OR 
         b.fecha_caducidad BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL ':dias days')
        AND b.saldo_puntos > 0;
    """)

    results = db.session.execute(query, {'dias': dias}).fetchall()

    if formato == 'JSON':
        # Formatear salida en JSON
        response = []
        for row in results:
            response.append({
                "cliente_id": row.cliente_id,
                "nombre": row.nombre,
                "apellido": row.apellido,
                "numero_documento": row.numero_documento,
                "tipo_documento": row.tipo_documento,
                "nacionalidad": row.nacionalidad,
                "email": row.email,
                "telefono": row.telefono,
                "fecha_nacimiento": row.fecha_nacimiento,
                "bolsa_id": row.bolsa_id,
                "fecha_asignacion": row.fecha_asignacion,
                "fecha_caducidad": row.fecha_caducidad,
                "saldo_puntos": row.saldo_puntos
            })
        return jsonify(response), 200
    else:
        # Formatear salida en tabla de texto
        headers = ["cliente_id", "nombre", "apellido", "numero_documento", "tipo_documento", "nacionalidad", "email", "telefono", "fecha_nacimiento", "bolsa_id", "fecha_asignacion", "fecha_caducidad", "saldo_puntos"]
        rows = [
            [row.cliente_id, row.nombre, row.apellido, row.numero_documento, row.tipo_documento, row.nacionalidad, row.email, row.telefono, row.fecha_nacimiento, row.bolsa_id, row.fecha_asignacion, row.fecha_caducidad, row.saldo_puntos]
            for row in results
        ]

        # Calcular el ancho de cada columna
        column_widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]
        header_row = " | ".join(f"{header:{column_widths[i]}}" for i, header in enumerate(headers))
        separator_row = "-+-".join('-' * width for width in column_widths)
        data_rows = "\n".join(" | ".join(f"{str(item):{column_widths[i]}}" for i, item in enumerate(row)) for row in rows)

        response_str = f"{header_row}\n{separator_row}\n{data_rows}"

        return f"<pre>{response_str}</pre>", 200

@consultas_bp.route('/puntos_a_vencer', methods=['GET'])
def consulta_puntos_a_vencer():
    dias = request.args.get('dias', type=int)
    formato = request.args.get('Formato', 'TXT').upper()

    if dias is not None:
        query = text("""
        SELECT 
            c.id AS cliente_id,
            c.nombre,
            c.apellido,
            c.numero_documento,
            c.tipo_documento,
            c.nacionalidad,
            c.email,
            c.telefono,
            c.fecha_nacimiento,
            b.id AS bolsa_id,
            b.fecha_asignacion,
            b.fecha_caducidad,
            b.saldo_puntos
        FROM 
            cliente c
        JOIN 
            bolsapuntos b ON c.id = b.cliente_id
        WHERE 
            (b.fecha_caducidad IS NULL OR 
             b.fecha_caducidad BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL ':dias days')
            AND b.saldo_puntos > 0;
        """)
        results = db.session.execute(query, {'dias': dias}).fetchall()
    else:
        query = text("""
        SELECT 
            c.id AS cliente_id,
            c.nombre,
            c.apellido,
            c.numero_documento,
            c.tipo_documento,
            c.nacionalidad,
            c.email,
            c.telefono,
            c.fecha_nacimiento,
            b.id AS bolsa_id,
            b.fecha_asignacion,
            b.fecha_caducidad,
            b.saldo_puntos
        FROM 
            cliente c
        JOIN 
            bolsapuntos b ON c.id = b.cliente_id
        WHERE 
            b.saldo_puntos > 0;
        """)
        results = db.session.execute(query).fetchall()

    if formato == 'JSON':
        # Formatear salida en JSON
        response = []
        for row in results:
            response.append({
                "cliente_id": row.cliente_id,
                "nombre": row.nombre,
                "apellido": row.apellido,
                "numero_documento": row.numero_documento,
                "tipo_documento": row.tipo_documento,
                "nacionalidad": row.nacionalidad,
                "email": row.email,
                "telefono": row.telefono,
                "fecha_nacimiento": row.fecha_nacimiento,
                "bolsa_id": row.bolsa_id,
                "fecha_asignacion": row.fecha_asignacion,
                "fecha_caducidad": row.fecha_caducidad,
                "saldo_puntos": row.saldo_puntos
            })
        return jsonify(response), 200
    else:
        # Formatear salida en tabla de texto
        headers = ["cliente_id", "nombre", "apellido", "numero_documento", "tipo_documento", "nacionalidad", "email", "telefono", "fecha_nacimiento", "bolsa_id", "fecha_asignacion", "fecha_caducidad", "saldo_puntos"]
        rows = [
            [row.cliente_id, row.nombre, row.apellido, row.numero_documento, row.tipo_documento, row.nacionalidad, row.email, row.telefono, row.fecha_nacimiento, row.bolsa_id, row.fecha_asignacion, row.fecha_caducidad, row.saldo_puntos]
            for row in results
        ]

        # Calcular el ancho de cada columna
        column_widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]
        header_row = " | ".join(f"{header:{column_widths[i]}}" for i, header in enumerate(headers))
        separator_row = "-+-".join('-' * width for width in column_widths)
        data_rows = "\n".join(" | ".join(f"{str(item):{column_widths[i]}}" for i, item in enumerate(row)) for row in rows)

        response_str = f"{header_row}\n{separator_row}\n{data_rows}"

        return f"<pre>{response_str}</pre>", 200
