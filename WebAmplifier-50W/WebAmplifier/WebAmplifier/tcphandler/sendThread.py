import threading

from WebAmplifier.syslog import systemlog
from WebAmplifier.tcphandler import threadfunc
import time

class SendDataThread(threading.Thread):
    '''
    轮询发送线程
    '''
    def __init__(self,defList):
        threading.Thread.__init__(self)
        self.defList = defList
    def run(self):
        #加快物理按钮和前端按钮的响应速度，提高读取发送速率
        btnSendData = list(self.defList.keys())[0]
        while True:
            try:
                for k , v in self.defList.items():
                    conn = threadfunc.get_ActiveSocket(v)
                    if conn:
                        conn.send(k)
                        time.sleep(0.1)
                    btnSock = threadfunc.get_ActiveSocket(self.defList.get(btnSendData))
                    if btnSock:
                        btnSock.send(btnSendData)
                        time.sleep(0.1)
            except Exception as e:
                systemlog.log_error(e)