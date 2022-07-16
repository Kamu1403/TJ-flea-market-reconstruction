# -*- coding: UTF-8 -*-

from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4321, debug=True)
