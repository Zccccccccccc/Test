"""
This script runs the WebAmplifier application using a development server.
"""

from os import environ
from WebAmplifier import socketio, app
from WebAmplifier.conf import initsystem
from WebAmplifier.syslog import systemlog



if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.logger.addHandler(systemlog.log_init())
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    initsystem.init_system()
    socketio.run(app, HOST, PORT, use_reloader=False)