# -*- coding: utf-8 -*-

"""
开关控制模式：
在Mode模式切换时，将AB通道关闭，检测到按钮或者前端发送的切换mode，
先变换当前状态，再发送x00配置到主控板和偏置板。

前端A以通道为2000W模式总开关，但服务端需要同时打开或关闭AB通道发送1XX
"""

from WebAmplifier.conf import setting
from WebAmplifier.data import sendData
from WebAmplifier import socketio

def recive_data(datas):
    """
    获取到按钮信息
    datas = {
        "push_mode": xx,
        "A_push": xx,
        "B_push": xx
    }

    修改服务器状态，并向主控板和告警板发送状态
    """
    if not datas["error"]:
        if datas["RF_button"]:
            setting.MODE_STATUS = ~setting.MODE_STATUS & 0x07 ^ 0x05   #修改A通道位
    return send_data(setting.MODE_STATUS)

def send_mode_status_to_front():
    """
    向前端发送同步后的状态
    """
    res = {
        "A": setting.MODE_STATUS & 0x02,
    }
    socketio.emit("S2F_ControlBoardMode", res)

def send_data(sendStr):
    """
    向主控板和告警板发送数据
    """
    if not sendStr == None:
        try:
            sockRequest = setting.clientSocketList[sendData.mainControlPanel.getIP()]
            if sockRequest:
                sendBuf = sendData.mainControlPanel.setWorkInf(sendStr)
                sockRequest.send(sendBuf)
            sockRequest = setting.clientSocketList[sendData.warningPanel.getIP()]
            if sockRequest:
                sendBuf = sendData.warningPanel.setWorkInf(sendStr)
                sockRequest.send(sendBuf)
            return True
        except Exception:
            return False
    return False

if __name__ == "__main__":
    datas = {
        "error": 0,
        "push_mode": 1,
        "A_push": 1,
        "B_push": 0
    }
    bool_mode_change(datas)