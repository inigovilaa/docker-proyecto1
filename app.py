from flask import Flask, jsonify, request
import socket
from prometheus_flask_exporter import PrometheusMetrics
import mysql.connector
import time
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.3')


config = {
  'user': 'admin99',
  'password': 'Admin9999',
  'host': os.getenv('DB_HOST', 'db'),
  'port': 3306,
  'database': 'messages'
}

# Intentar conectarse con reintentos
def connectToSQL():
    while True:
        try:
            connection = mysql.connector.connect(**config)
            print("Conexion exitosa a MySQL")
            break  
        except mysql.connector.Error as err:
            print("Intentando conectar a MySQL")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar
    return connection

@app.route('/')
def hello():
	hostname = socket.gethostname()
	return "Hello, from server " + hostname + "!\n"


@app.route('/data') #no hace falta poner el metodo porque por defecto es GET
def get_data():
  connection = connectToSQL()
  
  cursor = connection.cursor()
  query = "SELECT * FROM messages;"
  cursor.execute(query)  
  data = cursor.fetchall()
  cursor.close()
    
  return data #no hace falta jsonify porque en la query ya se hace

@app.route('/data/<int:id>')
def get_mess_by_id(id):
  connection = connectToSQL()

  cursor = connection.cursor()
  query = "SELECT * FROM messages WHERE clid = %s;"
  cursor.execute(query, (id,))
  data = cursor.fetchall()
  cursor.close()
    
  return data

@app.route('/data', methods=['POST'])
def postData():
  connection = connectToSQL()
  data = request.get_json()  # Tomar JSON del request
  clid = data.get('clid')
  mess = data.get('mess')
  server_name = socket.gethostname() 

  if not clid or not mess:
      return jsonify({"error": "Faltan datos, introduzca datos para clid y mess"}), 400
  
  if get_mess_by_id(clid) != []:
    return jsonify({"error": "El id ya existe"}), 400

  cursor = connection.cursor()
  query = "INSERT INTO messages (clid, mess, sid) VALUES (%s, %s, %s);"
  cursor.execute(query, (clid, mess, server_name))
  connection.commit()
  cursor.close()

  return jsonify({"message": "Data added successfully"})

@app.route('/data/<int:num>', methods=['PUT'])
def putData(num):
  connection = connectToSQL()

  data = request.get_json()  
  mess = data.get('mess')

  if not mess:
      return jsonify({"error": "Faltan datos"}), 400
  
  if get_mess_by_id(num) == []:
    return jsonify({"error": "El id no existe"}), 400

  cursor = connection.cursor()
  query = "UPDATE messages SET mess = %s WHERE clid = %s;"
  cursor.execute(query, (mess, num))
  connection.commit()
  cursor.close()
  
  return jsonify({"message": "Data updated successfully"})

@app.route('/data/<int:num>', methods=['DELETE'])
def deleteData(num):
  connection = connectToSQL()

  if get_mess_by_id(num) == []:
    return jsonify({"error": "El mensaje con ese id no existe"}), 400
  

  cursor = connection.cursor()
  cursor.execute("DELETE FROM messages WHERE clid = %s;", (num,))
  connection.commit()
  cursor.close()
  
  return jsonify({"message": "Data deleted successfully"})


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
