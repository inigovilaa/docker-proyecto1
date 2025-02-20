from flask import Flask, jsonify, request
import socket
import mysql.connector
import time
app = Flask(__name__)

config = {
  'user': 'root',
  'password': 'root',
  'host': 'db',
  'port': 3306,
  'database': 'messages'
}
# Intentar conectarse con reintentos
for i in range(10):  # 10 intentos
    try:
        connection = mysql.connector.connect(**config)
        print(" Conexión exitosa a MySQL")
        break
    except mysql.connector.Error as err:
        print(f" Intentando conectar a MySQL... (Intento {i+1}/10)")
        time.sleep(5)  # Esperar 5 segundos antes de reintentar
else:
    print(" No se pudo conectar a MySQL después de varios intentos")
    exit(1)
@app.route('/')
def hello():
	hostname = socket.gethostname()
	return "Hello, from server" + hostname + "!"

@app.route('/data')
def get_data():
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM messages;")  
  data = cursor.fetchall()
  cursor.close()
    
  return jsonify(data)
	
@app.route('/data/<int:num>', methods=['GET'])
def getDataInt():
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM messages WHERE clid = %s;", (num))
  data = cursor.fetchall()
  cursor.close()
  
  return jsonify(data)

@app.route('/data', methods=['POST'])
def postData():
  data = request.get_json()  # Tomar JSON del request
  clid = data.get('clid')
  mess = data.get('mess')
  server_name = socket.gethostname()  # Nombre del servidor

  if not clid or not mess:
      return jsonify({"error": "Faltan datos"}), 400

  cursor = connection.cursor()
  sql = "INSERT INTO mensajes (clid, mess, server_name) VALUES (%s, %s, %s);"
  cursor.execute(sql, (clid, mess, server_name))
  connection.commit()
  cursor.close()

  return jsonify({"message": "Data added successfully"})

@app.route('/data/<int:num>', methods=['PUT'])
def putData():
  data = request.get_json()  # Tomar JSON del request
  mess = data.get('mess')
  server_name = socket.gethostname()  # Nombre del servidor

  if not mess:
      return jsonify({"error": "Faltan datos"}), 400

  cursor = connection.cursor()
  sql = "UPDATE messages SET message = %s WHERE id = %s;"
  cursor.execute(sql, (num, mess))
  connection.commit()
  cursor.close()
  
  return jsonify("Data updated")

@app.route('/data/<int:num>', methods=['DELETE'])
def deleteData():
  cursor = connection.cursor()
  cursor.execute("DELETE FROM messages WHERE id = %s;", (num))
  connection.commit()
  cursor.close()
  
  return jsonify("Data deleted")


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)