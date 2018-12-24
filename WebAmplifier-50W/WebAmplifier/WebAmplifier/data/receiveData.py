 # -*- coding: utf-8 -*-

#######################################################
# FileName: receiveData.py
# Description: 接收数据相关的API函数
# 
#######################################################

import copy
from WebAmplifier.syslog import systemlog
from WebAmplifier.data import staticData

def sliceData(buffer):
    """
    数据分析，分割数据帧，返回一个完整的数据帧list
    """
    resData = []
    tempData = []
    status = False
    indexData = 0
    lenIndex = 0
    for data in buffer:
        if not status:
            if data == 0xA6:
                tempData.append(data)
                status = True
                indexData = 1
            else:
                continue
        else:
            tempData.append(data)
            indexData += 1
            if indexData == 4:
                lenIndex = data
            if indexData == lenIndex + 6:
                status = False
                indexData = 0
                lenIndex = 0
                resData.append(copy.deepcopy(tempData))
                tempData.clear()
    return resData

def parseData(dataList):
    """
    解析数据帧信息，返回解析结果dict
    """
    resData = {}
    if len(dataList) < 5:
        return resData
    try:
        resData['head'] = dataList[0]
        resData['address'] = dataList[1]
        resData['func'] = dataList[2]
        data_len = resData['len'] = dataList[3]
        resData['crc'] = dataList[data_len + 4] + dataList[data_len + 5] * 256
        resData['data_tag'] = dataList[4]
        resData['data'] = [dataList[x] for x in range(5, data_len + 4)]
    except Exception:
        return None
    return resData

def get_software_version(datas):
    """
    各个模块，获取软件版本信息
    """
    try:
        data = {
            "big_version": datas[0],
            "small_version": datas[1],
            "dev_version": datas[2]
        }
    except Exception:
        data = None
    return data

def control_status_info(datas):
    """
    主控板，工作状态信息
    uint8_t		1字节		工作信息操作状态(Work_Status), 详细说明见附录
    Bit0		1位		    保留
    Bit1		1位		    射频开关: 0为关闭, 1为打开
    Bit2		1位		    保留
    Bit3~7				    保留
    """
    try:
        data = {
            "error": datas[0]    
        }
        if not data["error"]:
            data["RF_switch"] = datas[1] >> 1 & 0x01
        else:
            systemlog.log_warning(u"获取主控板工作状态信息失败，数据无效: " + str(datas))
    except Exception:
        data = None
    return data

def control_push_info(datas):
    """
    主控板，按键信息
    uint8_t		1字节		0x00(单次读成功)
				            0x01(单次读失败, 数据无效)
    Bit0		1字节		保留
    Bit1				    射频按键: 0为松开, 1为摁下
    Bit2				    保留
    Bit3~7				    保留
    """
    try:
        data = {
            "error": datas[0]
        }
        if not data["error"]:
            data["RF_button"] = datas[1] >> 1 & 0x01
        else:
            systemlog.log_warning(u"获取主控板按键信息失败，数据无效: " + str(datas))
    except Exception:
        data = None
    return data

def control_power_info(datas):
    """
    主控板，功率信息
    uint8_t		1字节		0x00(单次读成功)
				            0x01(单次读失败, 数据无效)
    uint16_t	0或2字节	输入功率.
    uint16_t	0或2字节	正向功率.
    uint16_t	0或2字节	反向功率.
    uint16_t	0或2字节	保留
    uint16_t	0或2字节	保留							
    uint16_t	0或2字节	保留
    uint16_t	0或2字节	保留
    uint16_t	0或2字节	保留
    """
    try:
        data = {
            "error": datas[0],
            "power_data": []
        }
        if not data["error"]:
            data["power_data"] = [datas[i] + datas[i + 1] * 256 for i in range(1, len(datas), 2)]
        else:
            systemlog.log_warning(u"获取主控板功率信息失败，数据无效: " + str(datas))
    except Exception:
        data = None
    return data

def warning_status_info(datas):
    """
    告警板，工作状态信息
    uint8_t		1字节		工作信息操作状态(Work_Status), 详细说明见附录							
    Bit0		1位  		保留							
    Bit1		1位		    射频开关: 0为关闭, 1为打开							
    Bit2		1位		    保留							
    Bit3~7				    保留							
    """
    try:
        data = {
            "error": datas[0]
        }
        if not data["error"]:
            data["RF_button"] = datas[1] >> 1 & 0x01
        else:
            systemlog.log_warning(u"获取告警板工作状态信息失败，数据无效: " + str(datas))
    except Exception:
        data = None
    return data

def warning_data_info(datas):
    """
    告警板，告警信息
    uint8_t		1字节		0x00(无告警, 数据组为空)							
				            0x01(有告警, 数据组有效)							
    uint16_t	0或20字节	详见附录 register 1							
    uint16_t				详见附录 register 2							
    uint16_t				详见附录 register 3							
    uint16_t				详见附录 register 4							
    uint16_t				详见附录 register 5							
    uint16_t				详见附录 register 6							
    uint16_t				详见附录 register 7							
    uint16_t				详见附录 register 8							
    uint16_t				详见附录 register 9							
    uint16_t				详见附录 register 10
    """
    # 检测标识符和告警标识符
    try:
        if datas[0] == 0x01:
            res_data = [datas[i] + datas[i + 1] * 256 for i in range(1, len(datas), 2)]
            data = {
                "register1": res_data[0], 
                "register2": res_data[1],
                "register3": res_data[2],
                "register4": res_data[3],
                "register5": res_data[4],
                "register6": res_data[5],
                "register7": res_data[6],
                "register8": res_data[7],
                "register9": res_data[8],
                "register10": res_data[9],
            }
        else:
            systemlog.log_warning(u"无告警信息" + str(datas))
            data = {}
    except Exception:
        data = None
    return data

def get_temp_info(datas):
    """
    获取温度信息
    uint8_t		1字节		0x00(单次读成功)							
				            0x01(单次读失败, 数据组为空)
    int16_t		0或32字节	1~16路的温度数据组(单位: 0.1度)							
    """
    try:
        data = {
            "error": datas[0],
            "temp_list": []
        }
        if not data["error"]:
            data["temp_list"] = [datas[i] + datas[i + 1] * 256 for i in range(1, len(datas), 2)]
        else:
            systemlog.log_warning(u"读取温度信息失败" + str(datas))
            data = {}
    except Exception:
        data = None
    return data

def gate_voltage_once_read_info(datas):
    """
    单次读栅压返回信息
    uint8_t		1字节		栅压状态(GATE_Status), 详细说明见附录							
    uint8_t		1字节		栅压通道编号(0~138)							
    uint16_t	2字节	    栅压通道电压值(-mV)
    """
    try:
        data = {
            "GATE_status": datas[0],
            "gate_num": datas[1],
            "gate_voltage": datas[2] + datas[3] * 256
        }
        if data["GATE_status"]:
            systemlog.log_warning(u"单次读栅压失败，数据无效: " + str(datas))
    except Exception:
        data = None
    return data

def gate_voltage_continuous_read_info(datas):
    """
    连续读栅压返回信息
    uint8_t		1字节		栅压状态(GATE_Status), 详细说明见附录							
    uint8_t		1字节		栅压起始通道编号(0~138)							
    uint8_t		1字节		栅压通道数量(n)							
    uint16_t	0或n*2字节	栅压通道电压值(-mV)数据组							
    """
    try:
        data = {
            "GATE_status": datas[0],
            "gate_num_start": datas[1],
            "gate_num": datas[2],
            "gate_voltage": []
        } 
        if not data['GATE_status']:
            data['gate_voltage'] = [datas[i] + datas[i + 1] * 256 for i in range(3, len(datas), 2)]
        else:
            systemlog.log_warning(u"连续读栅压信息失败，数据无效: " + str(datas))
    except Exception:
        data = None
    return data

def gate_voltage_once_write_info(datas):
    """
    单次写栅压返回信息
    uint8_t		1字节		栅压状态(GATE_Status), 详细说明见附录							
    uint8_t		1字节		栅压通道编号(0~138)							
    uint16_t	2字节		栅压通道电压值(-mV)							
    """
    try:
        data = {
            "GATE_status": datas[0],
            "gate_num": datas[1],
            "gate_voltage": datas[2] + datas[3] * 256
        }
        if data["GATE_status"]:
            systemlog.log_warning(u"单次写栅压失败，数据无效: " + str(datas))
    except Exception:
        data = None
    return data

def gate_voltage_continuous_write_info(datas):
    """
    连续写栅压返回信息
    uint8_t		1字节		栅压状态(GATE_Status), 详细说明见附录							
    uint8_t		1字节		栅压起始通道编号(0~138)							
    uint8_t		1字节		栅压通道数量(n)							
    uint8_t		1字节		旋钮状态(KNOB_Status), 详细说明见附录							
    """
    try:
        data = {
            "GATE_status": datas[0],
            "gate_num_start": datas[1],
            "gate_num": datas[2],
            "KNOB_status": datas[3]
        }
        if data["GATE_status"]:
            systemlog.log_warning(u"连续写栅压失败，数据无效: " + str(datas))
    except Exception:
        data = None
    return data

def gate_voltage_channel_configure_info(datas):
    """
    配置旋钮信息
    """
    pass


def get_gate_voltage_channel_configure_info(datas):
    """
    获取旋钮信息
    uint8_t		1字节		旋钮状态(KNOB_Status), 详细说明见附录							
    uint16_t	0或2字节	增益控制的电压值, 详见文档<2000W功放部分约定>							
    uint16_t	0或2字节	频率控制的电压值, 详见文档<2000W功放部分约定>							
    uint16_t	0或2字节	功率控制的电压值, 详见文档<2000W功放部分约定>
    """
    try:
        data = {
            "error": datas[0]
        }
        if not data["error"]:
            data["gain"] = datas[1] + datas[2] * 256
            data["freq"] = datas[3] + datas[4] * 256
            data["power"] = datas[5] + datas[6] * 256
        else:
            systemlog.log_warning(u"获取旋钮信息失败，数据无效" + str(datas))
    except Exception:
        data = None
    return data

def get_gate_voltage_DAC_info(datas):
    """
    获取DAC在位信息
    uint16_t	2字节		DAC设备01~16的在位信息. 对应于bit0~bit15. bit为高表示在位							
    uint16_t	2字节		DAC设备17~32的在位信息. 对应于bit0~bit15. bit为高表示在位
    """
    try:
        data = {
            "dac1": datas[0] + datas[1] * 256,
            "dac2": datas[2] + datas[3] * 256
        }
    except Exception:
        data = None
    return data

def vol_boardB_info(datas):
    """
    过欠压检测板数据处理
    uint8_t		1字节		0x00(单次读成功)							
				            0x01(单次读失败, 数据组为空)							
    uint16_t	0或26字节	1~13路的普通电流数据组(单位: mA), 详见文档<2000W功放部分约定>
    """
    try:
        data = {
            "error": datas[0],
            "values": []
        }
        if not data['error']:
            data['values'] = [datas[i] + datas[i + 1] * 256 for i in range(1, len(datas), 2)]
        else:
            systemlog.log_warning(u"获取过欠压信息失败，数据无效" + str(datas))
            data = {}
    except Exception:
        data = None
    return data

def get_fan_info(datas):
    """
    获取风扇信息
    uint8_t		1字节		0x00(单次读成功)							
				            0x01(单次读失败, 数据无效)							
    uint16_t	2字节		从Bit0~Bit15分别代表16个风扇的工作状态(0为停转, 1为工作).							
    """
    try:
        data = {
            "error": datas[0],
            "values": []
        }
        if not data['error']:
            data['values'] = datas[1] + datas[2] * 256
        else:
            systemlog.log_warning(u"获取风扇信息失败，数据无效" + str(datas))
            data = {}
    except Exception:
        data = None
    return data

def get_fan_rate_info(datas):
    """
    获取风扇转速信息
    uint8_t		1字节		0x00(单次读成功)
				            0x01(单次读失败, 数据组为空)
    uint8_t		0或16字节  (16个风扇,每个风扇1个字节)
                            0~100%的速度比例, 比例越大, 速度越快
    """
    try:
        data = {
            "error": datas[0],
            "values": []
        }
        if not data['error']:
            data['values'] = [datas[i] for i in range(1, len(datas))]
        else:
            systemlog.log_warning(u"获取风扇信息速度失败，数据无效" + str(datas))
            data = {}
    except Exception:
        data = None
    return data

if __name__ == "__main__":
    datas = [0x00, 0x01, 0xa6, 0x01, 0x00, 0x03, 0x01, 0x00, 0x01, 0x0a, 0x0b]
    res_list = sliceData(datas)
    for res in res_list:
        data_list = parseData(res)
        res = control_status_info(data_list['data'])
        print(res)
