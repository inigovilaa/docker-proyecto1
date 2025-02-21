from flask import Flask, jsonify, request
import socket
from prometheus_flask_exporter import PrometheusMetrics
import mysql.connector
import time
app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')


config = {
  'user': 'admin',
  'password': 'admin',
  'host': 'db',
  'port': 3306,
  'database': 'messages'
}
# Intentar conectarse con reintentos
while True:
    try:
        connection = mysql.connector.connect(**config)
        print("Conexion exitosa a MySQL")
        break  
    except mysql.connector.Error as err:
        print("Intentando conectar a MySQL")
        time.sleep(5)  # Esperar 5 segundos antes de reintentar

@app.route('/')
def hello():
	hostname = socket.gethostname()
	return "Hello, from server " + hostname + "!"

@app.route('/data')
def get_data():
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM messages;")  
  data = cursor.fetchall()
  cursor.close()
    
  return jsonify(data)
	
@app.route('/data/<num>', methods=['GET'])
def getDataInt(num):
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM messages WHERE clid = %s;", (num,))
  data = cursor.fetchall()
  cursor.close()
  
  return jsonify(data)

@app.route('/data', methods=['POST'])
def postData():
  data = request.get_json()  # Tomar JSON del request
  clid = data.get('clid')
  mess = data.get('mess')
  server_name = socket.gethostname() 

  if not clid or not mess:
      return jsonify({"error": "Faltan datos"}), 400

  cursor = connection.cursor()
  sql = "INSERT INTO messages (clid, mess, sid) VALUES (%s, %s, %s);"
  cursor.execute(sql, (clid, mess, server_name))
  connection.commit()
  cursor.close()

  return jsonify({"message": "Data added successfully"})

@app.route('/data/<int:num>', methods=['PUT'])
def putData(num):
  data = request.get_json()  
  mess = data.get('mess')
  server_name = socket.gethostname() 

  if not mess:
      return jsonify({"error": "Faltan datos"}), 400

  cursor = connection.cursor()
  sql = "UPDATE messages SET mess = %s WHERE clid = %s;"
  cursor.execute(sql, (mess, num))
  connection.commit()
  cursor.close()
  
  return jsonify("Data updated")

@app.route('/data/<num>', methods=['DELETE'])
def deleteData(num):
  cursor = connection.cursor()
  cursor.execute("DELETE FROM messages WHERE clid = %s;", (num,))
  connection.commit()
  cursor.close()
  
  return jsonify("Data deleted")


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
