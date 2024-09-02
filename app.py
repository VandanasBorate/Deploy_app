from flask import Flask, render_template , request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '73cdc1d0f6618859946c0f623fec1d227ee9c637f457901a'
socketio = SocketIO(app)

# Set to store all connected clients
clients = set()

@socketio.on('connect')
def handle_connect():
    clients.add(request.sid)
    print(f"New client connected: {request.sid}. Total clients: {len(clients)}")
    emit('message', 'Connected to the server!')

@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)
    print(f"Client disconnected: {request.sid}. Total connected clients: {len(clients)}")

@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    # Broadcast the incoming message to all connected clients except the sender
    for client_sid in clients:
        if client_sid != request.sid:
            emit('message', message, room=client_sid)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("Starting Flask WebSocket server on http://localhost:5000...")
    socketio.run(app, host="localhost", port=5000)
