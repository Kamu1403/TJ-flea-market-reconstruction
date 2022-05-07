#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from app import socketio
from app import database


@socketio.on('joined', namespace='/chat')
def joined(message):
    pass

@socketio.on('text', namespace='/chat')
def text(message):
    pass


@socketio.on('left', namespace='/chat')
def left(message):
    pass
