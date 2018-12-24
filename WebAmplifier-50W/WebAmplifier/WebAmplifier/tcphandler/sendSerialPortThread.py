import threading, serial, time

import socketserver
from WebAmplifier import socketio as io
from WebAmplifier.conf import setting, modeControl
from WebAmplifier.api import crc
from WebAmplifier.data import receiveData, sendToFront,sendData
#接收网络数据帧
import struct
import random, time
from WebAmplifier.data.amplifierPanel import AmplifierPanel


class SendSerialPortThread(threading.Thread):
    '''
    轮询发送线程
    '''
    def __init__(self, serialPort):
        threading.Thread.__init__(self)
        self.serialPort = serialPort
    def run(self):
        #加快物理按钮和前端按钮的响应速度，提高读取发送速率
        boardList = [0x01, 0x02]
        amplifierPanel = AmplifierPanel()
        while True:
            for boardNum in boardList:
                sendbuf = amplifierPanel.getWorkInf(boardNum)
                self.serialPort.write(sendbuf)
                time.sleep(0.5)
                data = self.serialPort.read_all()
                self.parsingPacket(data)

                sendbuf = amplifierPanel.getAlarmInf(boardNum)
                self.serialPort.write(sendbuf)
                time.sleep(0.5)
                data = self.serialPort.read_all()
                self.parsingPacket(data)

                sendbuf = amplifierPanel.getCurrentInf(boardNum)
                self.serialPort.write(sendbuf)
                time.sleep(0.5)                
                data = self.serialPort.read_all()
                self.parsingPacket(data)

                sendbuf = amplifierPanel.GetTempInf(boardNum)
                self.serialPort.write(sendbuf)
                time.sleep(0.5)                
                data = self.serialPort.read_all()
                self.parsingPacket(data)

                sendbuf = amplifierPanel.continueReadGate(boardNum, 0, 7)
                self.serialPort.write(sendbuf)
                time.sleep(0.5)                
                data = self.serialPort.read_all()
                self.parsingPacket(data)

    def parsingPacket(self, data):
        recvBuf = struct.unpack("%dB"%len(data), data)
        resList = receiveData.sliceData(recvBuf)
        for res in resList:
            resData = receiveData.parseData(res)
            if resData['head'] != 0xA6:
                print("head error")
                break
            if crc.checkData(res[:-2], resData['crc']):
                if resData['data_tag'] == 0x02:
                    # 获取工作状态信息
                    control_data = receiveData.control_status_info(resData['data'])
                    sendToFront.send_ControlBoardButtonMode(control_data)
                    pass
                elif resData['data_tag'] == 0x03:
                    # 获取告警信息
                    pass
                elif resData['data_tag'] == 0x10:
                    # 获取电流信息
                    vol_boardB = receiveData.vol_boardB_info(resData['data'])
                    sendToFront.send_ElectricityStatus(vol_boardB, 1)
                    pass
                elif resData['data_tag'] == 0x11:
                    # 获取温度信息
                    temp_board_data = receiveData.get_temp_info(resData['data'])
                    sendToFront.send_TempStatus(0,temp_board_data)
                    pass
                elif resData['data_tag'] == 0x21:
                    # 获取连续栅压信息
                    gate_voltage_data = receiveData.gate_voltage_continuous_read_info(resData['data'])
                    sendToFront.send_GateVoltageStatus(gate_voltage_data)
                    pass                

            else:
                print("crc error")
                break
