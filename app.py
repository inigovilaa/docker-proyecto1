from flask import Flask
import socket
import mysql.connector
app = Flask(__name__)

config = {
  'user': 'root',
  'password': 'root',
  'host': 'db',
  'port': '3306',
  'database': 'messages'
}
connection = mysql.connector.connect(**config)

@app.route('/')
def hello():
	hostname = socket.gethostname
	return "Hello, from server" + hostname

@app.route('/data')
def get_data():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM messages;")  
    data = cursor.fetchall()
    cursor.close()
    
    return jsonify(data)
	
@app.route('/data', methods=['GET'], <num>)
def getDataInt():

@app.route('/data', methods=['POST'])
def postData():

@app.route('/data', methods=['PUT'], <num>)
def postData():


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)