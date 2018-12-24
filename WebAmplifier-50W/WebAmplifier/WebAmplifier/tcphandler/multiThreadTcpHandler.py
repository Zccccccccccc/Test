# -*- coding: utf-8 -*-

#######################################################
# FileName: multiThreadTcpHandler.py
# Description: 多线程tcp IO多路复用，实现tcp数据接收--测试
#######################################################

import socketserver
from WebAmplifier import socketio as io
from WebAmplifier.conf import setting, modeControl
from WebAmplifier.api import crc
from WebAmplifier.data import receiveData, sendToFront,sendData
#接收网络数据帧
import struct
import random, time

class MultiThreadTcpHandler(socketserver.BaseRequestHandler):

    def setup(self):
        # 加入客户端socket队列
        if str(self.client_address[0].strip()) in setting.clientSocketList:
            setting.clientSocketList[str(self.client_address[0].strip())] = self.request

    def handle(self):

        while True:
            data = self.request.recv(1024)
            if not data:
                break
            recvBuf = struct.unpack("%dB"%len(data), data)
            resList = receiveData.sliceData(recvBuf)
            for res in resList:
                resData = receiveData.parseData(res)
                if resData['head'] != 0xA6:
                    print("head error")
                    break
                if crc.checkData(res[:-2], resData['crc']):
                    if resData['address'] == 0x00:
                        #广播
                        pass
                    elif resData['address'] == 0x01:
                        #主控板
                        sendData.mainControlPanel.setPant(0)#设置心跳为0
                        if resData['data_tag'] == 0x01:
                            # 配置工作状态信息
                            pass
                        elif resData['data_tag'] == 0x02:
                            # 获取工作状态信息
                            control_data = receiveData.control_status_info(resData['data'])
                        elif resData['data_tag'] == 0x03:
                            # 按键信息
                            control_data = receiveData.control_push_info(resData['data'])
                            if modeControl.recive_data(control_data):
                                modeControl.send_mode_status_to_front()
                            else:
                                print("按键信息 error") 
                        elif resData['data_tag'] == 0x04:
                            # 功率信息
                            control_data = receiveData.control_power_info(resData['data'])
                            sendToFront.send_ControlBoardPower(control_data)
                        elif resData['data_tag'] == 0x05:
                            # 配置工作状态信息，告警信息
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            control_data = receiveData.get_software_version(resData['data'])
                        else:
                            print("control data tag error")
                    elif resData['address'] == 0x02:
                        #告警板
                        sendData.warningPanel.setPant(0)#设置心跳为0
                        if resData['data_tag'] == 0x01:
                            # 配置工作状态信息
                            pass
                        elif resData['data_tag'] == 0x02:
                            # 获取工作状态信息
                            warning_data = receiveData.warning_status_info(resData['data'])
                        elif resData['data_tag'] == 0x03:
                            # 告警信息
                            warning_data = receiveData.warning_data_info(resData['data'])
                            sendToFront.send_Warning(warning_data)
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            warning_data = receiveData.get_software_version(resData['data'])
                        else:
                            print("warning data tag error")
                    elif resData['address'] == 0x03:
                        #温度检测板1
                        sendData.tempPanel.setPant(0,0)
                        if resData['data_tag'] == 0x01:
                            #获取温度信息
                            temp_board_data = receiveData.get_temp_info(resData['data'])
                            sendToFront.send_TempStatus(0,temp_board_data)
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            temp_board_data = receiveData.get_software_version(resData['data'])
                        else:
                            print("fan data tag error")
                    elif resData['address'] == 0x04:
                        #温度检测板2
                        sendData.tempPanel.setPant(1,0)
                        if resData['data_tag'] == 0x01:
                            #获取温度信息
                            temp_board_data = receiveData.get_temp_info(resData['data'])
                            sendToFront.send_TempStatus(1, temp_board_data)
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            temp_board_data = receiveData.get_software_version(resData['data'])
                        else:
                            print("fan data tag error")
                    elif resData['address'] == 0x05:
                        #栅压板
                        sendData.gatePanel.setPant(0)#设置心跳为0
                        if resData['data_tag'] == 0x01:
                            # 单次读栅压
                            gate_voltage_data = receiveData.gate_voltage_once_read_info(resData['data'])
                        elif resData['data_tag'] == 0x02:
                            # 连续读栅压
                            gate_voltage_data = receiveData.gate_voltage_continuous_read_info(resData['data'])
                            sendToFront.send_GateVoltageStatus(gate_voltage_data)
                        elif resData['data_tag'] == 0x03:
                            # 单次写栅压
                            gate_voltage_data = receiveData.gate_voltage_once_write_info(resData['data'])
                        elif resData['data_tag'] == 0x04:
                            # 连续写栅压
                            gate_voltage_data = receiveData.gate_voltage_continuous_write_info(resData['data'])
                        elif resData['data_tag'] == 0x05:
                            # 配置旋钮信息
                            gate_voltage_data = receiveData.gate_voltage_channel_configure_info(resData['data'])
                        elif resData['data_tag'] == 0x06:
                            # reserved
                            pass
                        elif resData['data_tag'] == 0x07:
                            # 获取旋钮信息
                            gate_voltage_data = receiveData.get_gate_voltage_channel_configure_info(resData['data'])
                            sendToFront.send_ControlBoardSpin(gate_voltage_data, 0)
                        elif resData['data_tag'] == 0x08:
                            # reserved
                            pass
                        elif resData['data_tag'] == 0x09:
                            # 获取DAC在位信息
                            gate_voltage_data = receiveData.get_gate_voltage_DAC_info(resData['data'])
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            gate_voltage_data = receiveData.get_software_version(resData['data'])
                        else:
                            print("gate voltage data tag error")
                    elif resData['address'] == 0x06:
                        #过欠压检测板1
                        sendData.drainPanel.setPant(0,0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取电流信息
                            vol_boardB = receiveData.vol_boardB_info(resData['data'])
                            sendToFront.send_ElectricityStatus(vol_boardB, 1)
                        elif resData['data_tag'] == 0x02:
                            #reserved
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            vol_boardB = receiveData.get_software_version(resData['data'])
                        else:
                            print("voltage boardB_1 data tag error")
                    elif resData['address'] == 0x07:
                        #过欠压检测板2
                        sendData.drainPanel.setPant(1,0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取电流信息
                            vol_boardB = receiveData.vol_boardB_info(resData['data'])
                            sendToFront.send_ElectricityStatus(vol_boardB, 2)
                        elif resData['data_tag'] == 0x02:
                            #reserved
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            vol_boardB = receiveData.get_software_version(resData['data'])
                        else:
                            print("voltage boardB_2 data tag error")
                    elif resData['address'] == 0x08:
                        #过欠压检测板3
                        sendData.drainPanel.setPant(2, 0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取电流信息
                            vol_boardB = receiveData.vol_boardB_info(resData['data'])
                            sendToFront.send_ElectricityStatus(vol_boardB, 3)
                        elif resData['data_tag'] == 0x02:
                            #reserved
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            vol_boardB = receiveData.get_software_version(resData['data'])
                        else:
                            print("voltage boardB_3 data tag error")
                    elif resData['address'] == 0x09:
                        #过欠压检测板4
                        sendData.drainPanel.setPant(3, 0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取电流信息
                            vol_boardB = receiveData.vol_boardB_info(resData['data'])
                            sendToFront.send_ElectricityStatus(vol_boardB, 4)
                        elif resData['data_tag'] == 0x02:
                            #reserved
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            vol_boardB = receiveData.get_software_version(resData['data'])
                        else:
                            print("voltage boardB_4 data tag error")
                    elif resData['address'] == 0x0A:
                        #过欠压检测板5
                        sendData.drainPanel.setPant(4, 0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取电流信息
                            vol_boardB = receiveData.vol_boardB_info(resData['data'])
                            sendToFront.send_ElectricityStatus(vol_boardB, 5)
                        elif resData['data_tag'] == 0x02:
                            #reserved
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            vol_boardB = receiveData.get_software_version(resData['data'])
                        else:
                            print("voltage boardB_5 data tag error")
                    elif resData['address'] == 0x0B:
                        #过欠压检测板6
                        sendData.drainPanel.setPant(5, 0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取电流信息
                            vol_boardB = receiveData.vol_boardB_info(resData['data'])
                            sendToFront.send_ElectricityStatus(vol_boardB, 6)
                        elif resData['data_tag'] == 0x02:
                            #reserved
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            vol_boardB = receiveData.get_software_version(resData['data'])
                        else:
                            print("voltage boardB_6 data tag error")
                    elif resData['address'] == 0x0C:
                        #风扇检测板1
                        sendData.fanPanel.setPant(0, 0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取风扇信息
                            fan_data = receiveData.get_fan_info(resData['data'])
                            sendToFront.send_FansStatus(fan_data,0)
                        elif resData['data_tag'] == 0x02:
                            #获取风扇转速信息
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            fan_data = receiveData.get_fan_rate_info(resData['data'])
                        else:
                            print("voltage fan_1 data tag error")
                    elif resData['address'] == 0x0D:
                        #风扇检测板2
                        sendData.fanPanel.setPant(1, 0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取风扇信息
                            fan_data = receiveData.get_fan_info(resData['data'])
                            sendToFront.send_FansStatus(fan_data, 1)
                        elif resData['data_tag'] == 0x02:
                            #获取风扇转速信息
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            fan_data = receiveData.get_fan_rate_info(resData['data'])
                        else:
                            print("voltage fan_2 data tag error")
                    elif resData['address'] == 0x0E:
                        #风扇检测板3
                        sendData.fanPanel.setPant(2, 0)  # 设置心跳为0
                        if resData['data_tag'] == 0x01:
                            #获取风扇信息
                            fan_data = receiveData.get_fan_info(resData['data'])
                            sendToFront.send_FansStatus(fan_data, 2)
                        elif resData['data_tag'] == 0x02:
                            #获取风扇转速信息
                            pass
                        elif resData['data_tag'] == 0xF0:
                            # 获取软件版本信息
                            fan_data = receiveData.get_fan_rate_info(resData['data'])
                        else:
                            print("voltage fan_3 data tag error")
                    else:
                        print("mode number error")
                        break
                else:
                    print("crc error")
                    break
            #发送
            #self.request.sendall(self.data)

    def finish(self):
        del setting.clientSocketList[str(self.client_address[0].strip())]
        io.emit('amplifier_status', 0)
