# -*- coding: utf-8 -*-

#######################################################
# FileName: targetThread.py
# Description: 目标点接收线程
#######################################################

from socketserver import ThreadingTCPServer
import threading
import socketserver

from WebAmplifier.tcphandler import multiThreadTcpHandler
from WebAmplifier.syslog import systemlog

class targetPointThread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.tcpHandler = None
        self.port = port
        self.threadTcpHander = multiThreadTcpHandler.MultiThreadTcpHandler
    def run(self):
        try:
            self.tcpHandler = socketserver.ThreadingTCPServer(("0.0.0.0", self.port), self.threadTcpHander)
            self.tcpHandler.daemon_threads = True
            self.tcpHandler.serve_forever()
        except Exception as e:
            systemlog.log_error(e)