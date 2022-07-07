from distutils.log import debug
from flask import Flask, request
from flask_socketio import SocketIO, emit
from threading import Timer
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
socketio = SocketIO(app, cors_allowed_origins="*")

clients = {}

@app.route('/')
def index():
    return "Hello World"

@socketio.on('connect')
def connected():
    global clients
    clients[request.sid] = {
        'joined_at': time.time(),
    }
    emit('message', 'Client connected')

@socketio.on('disconnect')
def disconnected():
    global clients
    del clients[request.sid]

@socketio.on('message')
def handleMsg(msg):
    emit('message', 'interval')
    print(msg, request.sid)

@socketio.event
def get_clients():
    global clients
    users = list(clients.keys())
    emit('clients', { 'users': users, 'count': len(users) })

@socketio.event
def get_time():
    emit('time', time.time())

@socketio.event
def get_since():
    global clients
    user = clients[request.sid]
    diff = round(time.time() - user['joined_at'], 2)
    emit('message', "Joined before {t}s".format(t=diff))

def handleInterval():
    global clients
    users = list(clients.keys())
    count = len(users)
    if count > 0:
        socketio.emit('message', 'connected')
    Timer(60, handleInterval).start()

Timer(60, handleInterval).start()

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    app.run()