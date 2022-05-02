from flask import session, request
from flask_socketio import emit, join_room, leave_room
from .. import socketio

room_dict = {}


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    sender = session.get('name')
    receiver = session.get('receiver')
    room = sender + receiver
    reroom = receiver + sender
    sid = request.sid
    if (room not in room_dict):
        room_dict[room] = sid
        room_dict[reroom] = sid
    print(room_dict)
    join_room(room_dict[room])
    emit('status', {'msg': session.get('name') + ' has entered the room.'},
         room=room_dict[room])


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    sender = session.get('name')
    receiver = session.get('receiver')
    room = sender + receiver
    print(room_dict)
    emit('message', {'msg': session.get('name') + ':' + message['msg']},
         room=room_dict[room])


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    sender = session.get('name')
    receiver = session.get('receiver')
    room = sender + receiver
    print(room_dict)
    leave_room(receiver)
    emit('status', {'msg': session.get('name') + ' has left the room.'},
         room=room_dict[room])
