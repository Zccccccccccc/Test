# -*- coding: utf-8 -*-

#######################################################
# FileName: sockethandler.py
# Description: socketio处理事件
#######################################################

import threading
import time

from flask_socketio import send, emit
from WebAmplifier import socketio
from WebAmplifier.conf import setting, modeControl
from WebAmplifier.syslog import systemlog
from WebAmplifier.data import sendData
from WebAmplifier.data.gatePanel import GatePanel

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    systemlog.log_debug(e)

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    systemlog.log_debug(e)

#前端请求连接事件
@socketio.on('connect_event')
def connect_event(msg):
    systemlog.log_debug(str(msg['data']) + "连接成功")


#前端请求断开事件
@socketio.on('disconnect')
def disconnect_event():
    systemlog.log_debug("断开连接")  #功能未实现

#连接心跳，保证长时间连接
@socketio.on('response_event')
def leave_event():
    print('链接了')
    pass


#前端设置功放模式，工作状态
@socketio.on('F2S_ControlBoardMode')
def setControlBoardMode(msg):
    sockRequest = setting.clientSocketList[sendData.mainControlPanel.getIP()]
    if sockRequest:
        sendBuf = sendData.mainControlPanel.setWorkInf(str(msg['B']) + str(msg['A'])  +str(msg['ControlBoardMode']))
        sockRequest.send(sendBuf)
    sockRequest = setting.clientSocketList[sendData.warningPanel.getIP()]
    if sockRequest:
        sendBuf = sendData.warningPanel.setWorkInf(str(msg['B']) + str(msg['A'])  +str(msg['ControlBoardMode']))
        sockRequest.send(sendBuf)



#前端设置虚拟旋钮信息
@socketio.on('F2S_SetControlBoardSpin')
def setControlBoardSpin(msg):
    sockRequest = setting.clientSocketList[sendData.gatePanel.getIP()]
    if sockRequest:
        sendBuf = GatePanel().ConfigAchKnobInf(int(msg['Gain']), float(msg['Frequency']), int(msg['Power']))
        sockRequest.send(sendBuf)
    pass

#前端调节栅压（调试使用）
@socketio.on('F2S_GateVoltageStatus')
def setGateVoltageStatus(msg):
    sockRequest = setting.clientSocketList[sendData.gatePanel.getIP()]
    if sockRequest:
        sendBuf = GatePanel().SingleWriteGate(msg['GateVoltagePath'], msg['GateVoltage'])
        sockRequest.send(sendBuf)
    pass

#切换A通道开关
@socketio.on("F2S_ControlBoardSwitchAPath")
def setControlBoardSwitchAPath():
    setting.MODE_STATUS = ~setting.MODE_STATUS & 0x07 ^ 0x05   #修改A通道位
    modeControl.send_data(setting.MODE_STATUS)


#前端连续调节139路栅压（调试使用）
@socketio.on('F2S_ContinueGateVoltageStatus')
def setContinueGateVoltageStatus(msg):
    sockRequest = setting.clientSocketList[sendData.gatePanel.getIP()]
    if sockRequest:
        sendBuf = GatePanel().ContinueWriteGate(msg['Tag'], msg["List"])
        sockRequest.send(sendBuf)
    pass

