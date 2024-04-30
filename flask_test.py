import socketio

# Create Flask-SocketIO server
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

if __name__ == "__main__":
    # Connect to the Flask-SocketIO server
    sio.connect('http://127.0.0.1:5000')

    while True:
        message = input("Enter a message to send to the server (or type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        sio.emit('message', message)

    # Disconnect from the server when finished
    sio.disconnect()