# -*- coding: UTF-8 -*-

from app import app,socketio


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    socketio.run(app,port=4321, debug=True)
