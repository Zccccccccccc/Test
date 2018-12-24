"""
The flask application package.
"""

from flask import Flask, render_template
from flask_socketio import SocketIO
import sys, os

#增加对pyinstaller生成exe的支持
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    socketio = SocketIO(app)
else:
    app = Flask(__name__)
    socketio = SocketIO(app)

from WebAmplifier import views
from WebAmplifier.tcphandler import sockethandler


