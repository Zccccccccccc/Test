# -*- coding: utf-8 -*-

#######################################################
# FileName: initsystem.py
# Description: 服务启动后，初始化系统函数
#######################################################
import time
from WebAmplifier.conf import setting
from WebAmplifier.db import systemfunc
from WebAmplifier.tcphandler import targetThread, sendThread, checkPanelThread
from WebAmplifier.data import sendData
from WebAmplifier.tcphandler import readSerialPortThread, sendSerialPortThread
import serial

#初始化系统
def init_system():
    serialPort = init_dataSerialPort()
    init_dataSerialPortSend(serialPort)

#初始化串口
def init_dataSerialPort():
    # portName = input("输入串口如(COM1):")
    serialPort = serial.Serial()
    serialPort.port = "COM1"
    serialPort.baudrate = 115200
    serialPort.parity = serial.PARITY_NONE
    serialPort.stopbits = serial.STOPBITS_ONE
    serialPort.bytesize = serial.EIGHTBITS
    serialPort.open()
    return serialPort

#初始化串口数据发送线程
def init_dataSerialPortSend(serialPort):
    sendThread = sendSerialPortThread.SendSerialPortThread(serialPort)
    sendThread.start()
