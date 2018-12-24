import threading

from WebAmplifier.syslog import systemlog
from WebAmplifier.data import sendData,sendToFront

import time

class CheckPanelThread(threading.Thread):
    '''
    检查板子失联线程
    '''
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            try:
                self.addPant()
                self.checkPant()
            except Exception as e:
                systemlog.log_error(e)
            time.sleep(1)
    def addPant(self):
        sendData.mainControlPanel.addPant()
        sendData.warningPanel.addPant()
        sendData.gatePanel.addPant()
        for i in range(0,6):
            sendData.drainPanel.addPant(i)
        for i in range(0,2):
            sendData.tempPanel.addPant(i)
        for i in range(0,3):
            sendData.fanPanel.addPant(i)
    def checkPant(self):
        if sendData.mainControlPanel.checkPant():
            #发送通知前端失联
            sendToFront.send_boardDisconnectWarning(1)
        if sendData.warningPanel.checkPant():
            sendToFront.send_boardDisconnectWarning(2)
        if sendData.gatePanel.checkPant():
            sendToFront.send_boardDisconnectWarning(5)
        for i in range(0, 6):
            if sendData.drainPanel.checkPant(i):
                sendToFront.send_boardDisconnectWarning(i+6)
        for i in range(0, 2):
            if sendData.tempPanel.checkPant(i):
                # 发送通知前端失联
                sendToFront.send_boardDisconnectWarning(3+i)
        for i in range(0, 3):
            if sendData.fanPanel.checkPant(i):#风扇板0-2
                sendToFront.send_boardDisconnectWarning(12+i)