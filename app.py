from flask import Flask
import socket
app = Flask(__name__)
my
@app.route('/')
def hello():
	hostname = socket.gethostname
	return "Hello, from server" + hostname

@app.route('/data', methods=['GET'])
def getData():
	
@app.route('/data', methods=['GET'], <num>)
def getDataInt():

@app.route('/data', methods=['POST'])
def postData():

@app.route('/data', methods=['PUT'], <num>)
def postData():


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)