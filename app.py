from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def hello():
    hostname = socket.gethostname()
    return 'Hello, from server ' + hostname

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
