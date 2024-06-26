from flask import Flask, render_template
from flask_socketio import SocketIO
import json

app = Flask(__name__, template_folder='static')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('main.html')

@socketio.on('message')
def handle_message(message):
    print(message)
    json_object = json.loads(message)
    if  (json_object.get("type") == "animate" or json_object.get("type") == "display" or json_object.get("type") == "question") and json_object.get("msg"):
    # Broadcast the received message to all clients
        socketio.emit('message', json_object, namespace='/')

if __name__ == '__main__':
    socketio.run(app, debug=True)