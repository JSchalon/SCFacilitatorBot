from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='static')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('main.html')

@socketio.on('message')
def handle_message(message):
    print(message)
    # Broadcast the received message to all clients
    socketio.emit('message', {'message': message}, namespace='/')

if __name__ == '__main__':
    socketio.run(app, debug=True)