from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from flask_login import LoginManager,login_user,current_user
from PingDB import get_user,save_user
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

socketio = SocketIO(app, manage_session=False)
login_manager=LoginManager(app)
login_manager.init_app(app)



@app.route('/', methods=['GET', 'POST'])
def button():
    return render_template('button.html')







@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    return render_template('newuser.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    messaage=''
    if request.method == 'POST':
        username= request.form.get('username')
        password= request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input=password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            message='Failed to Login : enter correct information'

    return render_template('login.html' , messaage=messaage)








@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
















@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))



@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)






@login_manager.user_loader
def load_user(username):
    return get_user(username)

if __name__ == '__main__':
    socketio.run(app)