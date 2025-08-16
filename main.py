import pymysql
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Manejador para CORS
@app.route('/registrar-cliente', methods=['OPTIONS'])
def handle_options():
    response = jsonify({})
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'POST')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type')
    return response, 204

@app.route('/registrar-cliente', methods=['POST'])
def registrar_cliente():
    """Responde a las peticiones HTTP con un mensaje de éxito o fracaso."""
    request_json = request.get_json(silent=True)
    if not request_json:
        # Devuelve un error si no hay datos JSON
        response = jsonify({'success': False, 'error': 'No se recibieron datos JSON.'})
        response.headers.set('Access-Control-Allow-Origin', '*')
        return response, 400

    # Configura la conexión a la base de datos a través del Cloud SQL Auth Proxy
    INSTANCE_CONNECTION_NAME = "mi-po-backend-gcp:southamerica-west1:bd-mysql"
    
    try:
        conn = pymysql.connect(
            unix_socket=f'/cloudsql/{INSTANCE_CONNECTION_NAME}',
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            database=os.environ.get('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        # Devuelve un error si no se puede conectar a la BD
        response = jsonify({'success': False, 'error': f'Error de conexión a la BD: {e}'})
        response.headers.set('Access-Control-Allow-Origin', '*')
        return response, 500

    # Lógica para insertar los datos
    try:
        with conn.cursor() as cursor:
            # Obtener el customerNumber más alto y sumarle 1
            cursor.execute("SELECT MAX(customerNumber) AS max_id FROM customers")
            result = cursor.fetchone()
            new_customer_number = result['max_id'] + 1
            
            sql = "INSERT INTO customers (customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, city, country, creditLimit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            values = (
                new_customer_number,
                request_json.get('customerName'),
                request_json.get('contactLastName'),
                request_json.get('contactFirstName'),
                request_json.get('phone'),
                request_json.get('addressLine1'),
                request_json.get('city'),
                request_json.get('country'),
                request_json.get('creditLimit')
            )
            
            cursor.execute(sql, values)
        conn.commit()
        
        # Devuelve una respuesta de éxito con la cabecera CORS
        response = jsonify({'success': True, 'message': 'Cliente registrado.'})
        response.headers.set('Access-Control-Allow-Origin', '*')
        return response, 200

    except Exception as e:
        conn.rollback()
        # Devuelve una respuesta de error con la cabecera CORS
        response = jsonify({'success': False, 'error': f'Error al insertar datos: {e}'})
        response.headers.set('Access-Control-Allow-Origin', '*')
        return response, 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
