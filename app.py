from flask import Flask, jsonify, request
import socket
from prometheus_flask_exporter import PrometheusMetrics
import mysql.connector
import time
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Información sobre la aplicación para métricas de Prometheus
metrics.info('app_info', 'Application info', version='1.0.3')

# Configuración de la conexión a la base de datos MySQL
config = {
  'user': 'admin99',
  'password': 'Admin9999',
  'host': os.getenv('DB_HOST', 'db'),  # Se obtiene el host desde variables de entorno
  'port': 3306,
  'database': 'messages'
}

def connectToSQL():
    """
    Establece una conexión con la base de datos MySQL con reintentos en caso de fallo
    
    Returns
    -------
        Objeto de conexión a la base de datos MySQL
    """
    while True:
        try:
            connection = mysql.connector.connect(**config)
            print("Conexion exitosa a MySQL")
            return connection
        except mysql.connector.Error:
            print("Intentando conectar a MySQL")
            time.sleep(5)  # Espera 5 segundos antes de reintentar

@app.route('/')
def hello():
    """
    Endpoint de prueba para verificar que el servidor está funcionando
    
    Returns
    -------
    str
        Mensaje de bienvenida con el ID del servidor
    """
    hostname = socket.gethostname()
    return f"Hello, from server {hostname}!\n"

@app.route('/data') #no hace falta poner el metodo porque por defecto es GET
def get_data():
    """
    Obtiene todos los registros de la tabla 'messages'
    
    Returns
    -------
        Lista con todos los registros de la tabla 'messages'
    """
    connection = connectToSQL()
    cursor = connection.cursor()
    query = "SELECT * FROM messages;"
    cursor.execute(query)  
    data = cursor.fetchall()
    cursor.close()
    return data #no hace falta jsonify porque en la query ya se hace

@app.route('/data/<int:id>')
def get_mess_by_id(id):
    """
    Obtiene un mensaje específico por su ID
    
    Parameters
    ----------
    id : int
        Identificador del mensaje
    
    Returns
    -------
        Lista con los datos del mensaje correspondiente al ID
    """
    connection = connectToSQL()
    cursor = connection.cursor()
    query = "SELECT * FROM messages WHERE clid = %s;"
    cursor.execute(query, (id,))
    data = cursor.fetchall()
    cursor.close()
    return data

@app.route('/data', methods=['POST'])
def postData():
    """
    Inserta un nuevo mensaje en la base de datos
    
    Returns
    -------
        Mensaje de éxito o error en formato JSON
    """
    connection = connectToSQL()
    data = request.get_json()
    clid = data.get('clid')
    mess = data.get('mess')
    server_name = socket.gethostname() 

    if not clid or not mess:
        return jsonify({"error": "Faltan datos, introduzca datos para clid y mess"}), 400
    
    if get_mess_by_id(clid):
        return jsonify({"error": "El id ya existe"}), 400

    cursor = connection.cursor()
    query = "INSERT INTO messages (clid, mess, sid) VALUES (%s, %s, %s);"
    cursor.execute(query, (clid, mess, server_name))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Data added successfully"})

@app.route('/data/<int:num>', methods=['PUT'])
def putData(num):
    """
    Actualiza el contenido de un mensaje existente identificado por su ID
    
    Parameters
    ----------
    num : int
        Identificador del mensaje a actualizar
    
    Returns
    -------
        Mensaje de éxito o error en formato JSON
    """
    connection = connectToSQL()
    data = request.get_json()  
    mess = data.get('mess')

    if not mess:
        return jsonify({"error": "Faltan datos para mess"}), 400
    
    if not get_mess_by_id(num):
        return jsonify({"error": "El id no existe"}), 400

    cursor = connection.cursor()
    query = "UPDATE messages SET mess = %s WHERE clid = %s;"
    cursor.execute(query, (mess, num))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Data updated successfully"})

@app.route('/data/<int:num>', methods=['DELETE'])
def deleteData(num):
    """
    Elimina un mensaje de la base de datos identificado por su ID
    
    Parameters
    ----------
    num : int
        Identificador del mensaje a eliminar
    
    Returns
    -------
    dict
        Mensaje de éxito o error en formato JSON
    """
    connection = connectToSQL()
    
    if not get_mess_by_id(num):
        return jsonify({"error": "El mensaje con ese id no existe"}), 400
    
    cursor = connection.cursor()
    cursor.execute("DELETE FROM messages WHERE clid = %s;", (num,))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Data deleted successfully"})


if __name__ == '__main__':
    # Inicia el servidor Flask en el puerto 80
    app.run(host='0.0.0.0', port=80)