# -*- coding: utf-8 -*-

"""
FileName: sendToFront.py
Description: 向前端发送数据
"""
from WebAmplifier import socketio
from WebAmplifier.syslog import systemlog
from WebAmplifier.api.knob import *
from WebAmplifier.data import staticData

def send_ControlBoardOpen(data):
    """
    向前端发送主控板开关状态，1为开，0为关
    message：S2F_ControlBoardOpen
    data：
    {
        "ControlBoradOpen"：xx
    }
    """
    print(data)

def send_ControlBoardMode(data):
    """
    向前端发送主控板模式状态，控制板状态可能和按钮状态不一致，需要上位机来维护
    ControlBoarMode，0为1000w，1为2000w
    A：0为关闭，1为打开
    B：0为关闭，1为打开
    message：S2F_ControlBoardMode
    data：
    {
        "ControlBoardMode": xx,
        "A": xx,
        "B": xx
    }
    """
    if data:
        if not data["error"]:
            res = {
                "ControlBoardMode": data["mode"],
                "A": data["A_status"],
                "B": data["B_status"]
            }
            socketio.emit("S2F_ControlBoardMode", res)
        else:
            systemlog.log_warning(u"读主控板按键信息失败，数据无效: " + str(data))

def send_ControlBoardButtonMode(data):
    """
    向前端发送主控板功放按钮模式状态，以按钮状态为基准
    ControlBoarMode，0为1000w，1为2000w
    A：0为关闭，1为打开
    B：0为关闭，1为打开
    message：S2F_ControlBoardMode
    data：
    {
        "ControlBoardMode": xx,
        "A": xx,
        "B": xx
    }
    """
    if data:
        if not data["error"]:
            res = {
                "ControlBoardMode": data["push_mode"],
                "A": data["A_push"],
                "B": data["B_push"]
            }
            socketio.emit("S2F_ControlBoardMode", res)
        else:
            systemlog.log_warning(u"读主控板按键信息失败，数据无效: " + str(data))

def send_ControlBoardPower(data):
    """
    向前端发送主控板功率模式状态，8路，power为功率
    message：S2F_ControlBoardPower
    data：
    {
        "Power": [xx, xx,...]
    }
    """
    if data:
        if not data["error"]:
            powerArray = getMainControlPanlPower(data["power_data"])
            res = {
                "Power": powerArray
            }
            socketio.emit("S2F_ControlBoardPower", res)
        else:
            systemlog.log_warning(u"读主控板功率信息失败，数据无效: " + str(data))

def send_ControlBoardLightWarning(data):
    """
    向前端发送主控板告警信息
    message: S2F_MainBoardWarning
    data：
    {
        "S2F_MainBoardWarning": xxx
    }
    MBW  cpld1 register1 16bit
    """
    if data:
        res = {
            "MainBoardWarning": data["work_status"]
        }
        socketio.emit("S2F_MainBoardWarning", res)

def send_ControlBoardSpin(data, path_num):
    """
    向前端发送主控板旋钮信息，包括增益、频率、功率，
    Path：0表示A路，1表示B路
    message：S2F_ControlBoardSpin
    data：
    {
        "Path": xxx,
        "Gain": xxx,
        "Frequrency": xxx,
        "Power": xxx
    }
    """
    print(data)
    if data:
        if not data["error"]:
            res = {
                #"Path": path_num,
                "Gain": v_to_gain(int(data['gain'])),
                "Frequency": v_to_freq(int(data['freq'])),
                "Power": v_to_power(int(data['power']),int(data['freq']))
            }
            staticData.CONFIG_CHKNOBINf[path_num] = res
            socketio.emit("S2F_ControlBoardSpin", res)
        else:
            systemlog.log_warning(u"读主控板旋钮信息失败，数据无效: " + str(data))


def send_WarningBoardMode(data):
    """
    向前端发送告警板状态，控制板状态可能和按钮状态不一致，需要上位机来维护
    ControlBoarMode，0为1000w，1为2000w
    A：0为关闭，1为打开
    B：0为关闭，1为打开
    message：S2F_ControlBoardMode
    data：
    {
        "ControlBoardMode": xx,
        "A": xx,
        "B": xx
    }
    """
    if data:
        if not data["error"]:
            res = {
                "ControlBoardMode": data["push_mode"],
                "A": data["A_push"],
                "B": data["B_push"]
            }
            socketio.emit("S2F_ControlBoardMode", res)
        else:
            systemlog.log_warning(u"读主控板按键信息失败，数据无效: " + str(data))


def send_Warning(data):
    """
    根据告警信息，解析告警数据发送告警
    """
    send_GateBoardWarning(data)
    #send_TempBoardWarning(data)
    #send_FanBoardWarning(data)
    #send_MainBoardWarning(data)
    send_VolBoardAWarning(data)
    #send_VolBoardBWarning(data)
    send_OffsetBoardAWarning(data)
    #send_OffsetBoardBWarning(data)

def send_GateBoardWarning(data):
    """
    向前端发送栅压板告警信息
    message：S2F_GateBoardWarning
    data：
    {
        "GateBoardWarning": xx
    }
    GBW   cpld1 register1    19bit
    """
    if data:
        res = {
            "GateBoardWarning": data["register1"] >> 1 & 0x01
        }
        print("珊压警告：")
        print(res)
        socketio.emit("S2F_GateBoardWarning", res)

def send_TempBoardWarning(data):
    """
    向前端发送温度板告警信息
    message：S2F_TempBoardWarning
    data：
    {
        "TempBoardWarning": xx
    }
    TBW  cpld1 register1   18bit
    """
    if data:
        res = {
            "TempBoardWarning": data["cpld1_register1"] >> 18 & 0x01
        }
        print("温度警告：")
        print(res)
        socketio.emit("S2F_TempBoardWarning", res)

def send_FanBoardWarning(data):
    """
    向前端发送风扇板告警信息
    message：S2F_FanBoardWarning
    data：
    {
        "FanBoardWarning": xxx
    }
    FBW  cpld1 register1 17bit
    """
    if data:
        res = {
            "FanBoardWarning": data["cpld1_register1"] >> 17 & 0x01
        }
        print("风扇警告：")
        print(res)
        socketio.emit("S2F_FanBoardWarning", res)

def send_MainBoardWarning(data):
    """
    向前端发送主控板告警信息
    message: S2F_MainBoardWarning
    data：
    {
        "S2F_MainBoardWarning": xxx
    }
    MBW  cpld1 register1 16bit
    """
    if data:
        res = {
            "MainBoardWarning": data["cpld1_register1"] >> 16 & 0x01
        }
        print("主控警告：")
        print(res)
        socketio.emit("S2F_MainBoardWarning", res)

def send_VolBoardAWarning(data):
    """
    向前端发送检测板A告警，8路，数据为告警的通路的编号
    message: S2F_VolBoardAWarning
    data：
    {
        "S2F_VolBoardAWarning": [xx, xx, ...]
    }
    VBAW  cpld1 register1 0~7bit
    """
    if data:
        res = {
            "VolBoardAWarning": [i + 1 for i in range(0, 12) if data["register2"] >> i & 0x01]
        }
        socketio.emit("S2F_VolBoardAWarning", res)

def send_VolBoardBWarning(data):
    """
    向前端发送检测板B告警，8路，数据为告警的通路的编号
    message: S2F_VolBoardBWarning
    data：
    {
        "S2F_VolBoardBWarning": [xx, xx, ...]
    }
    VBBW   cpld1 register1  8~15bit
    """
    if data:
        res = {
            "VolBoardBWarning": [i + 1 for i in range(0, 8) if data["register2"] >> (i + 8) & 0x01]
        }
        socketio.emit("S2F_VolBoardBWarning", res)

def send_OffsetBoardAWarning(data):
    """
    向前端发送偏置板A告警，52路，数据为告警的通路的编号
    message: S2F_OffsetBoardAWarning
    data：
    {
        "S2F_OffsetBoardAWarning": [xx, xx, ...]
    }
    OBAW   cpld1 register2  32bit   cpld1 register3   0~18bit
    """
    print(11)
    print(data)
    if data:
        res = {
            "OffsetBoardAWarning": [i + 1 for i in range(0, 16) if data["register3"] >> i & 0x01]
        }
        res["OffsetBoardAWarning"].extend([i + 17 for i in range(0, 16) if data["register4"] >> i & 0x01])
        res["OffsetBoardAWarning"].extend([i + 33 for i in range(0, 16) if data["register5"] >> i & 0x01])
        res["OffsetBoardAWarning"].extend([i + 49 for i in range(0, 2) if data["register6"] >> i & 0x01])
        res["OffsetBoardAWarning"].extend([i + 51 for i in range(0, 16) if data["register7"] >> i & 0x01])
        res["OffsetBoardAWarning"].extend([i + 67 for i in range(0, 4) if data["register8"] >> i & 0x01])
        print("偏执版警告：")
        print(res)
        socketio.emit("S2F_OffsetBoardAWarning", res)

def send_OffsetBoardBWarning(data):
    """
    向前端发送偏置板B告警，52路，数据为告警的通路的编号
    message: S2F_OffsetBoardBWarning
    data：
    {
        "S2F_OffsetBoardBWarning": [xx, xx, ...]
    }
    OBBW   cpld2 register1  32bit   cpld2 register2   0~18bit
    """
    if data:
        res = {
            "OffsetBoardBWarning": [i + 1 for i in range(0, 16) if data["register7"] >> i & 0x01]
        }
        res["OffsetBoardBWarning"].extend([i + 16 for i in range(0, 16) if data["register8"] >> i & 0x01])
        res["OffsetBoardBWarning"].extend([i + 32 for i in range(0, 16) if data["register9"] >> i & 0x01])
        res["OffsetBoardBWarning"].extend([i + 48 for i in range(0, 4) if data["register10"] >> i & 0x01])
        socketio.emit("S2F_OffsetBoardBWarning", res)

def send_FansStatus(data,tag):
    """
    向前端发送当前风扇信息，16路，1为工作，0为停止
    message：S2F_FansStatus
    data：
    {
        "FansStatus": [xx, xx, xx, xx, xx, xx]
    }
    """
    if tag == 2:
        end = 5
    else:
        end = 16
    if data:
        res = {
            "Tag" : tag ,
            "FansStatus": [data["values"] >> i & 0x01 for i in range(0, end)]
        }
        socketio.emit("S2F_FansStatus", res)
def send_FansRotatingStatus(data):
    """
    向前端发送当前风扇信息，6路，1为工作，0为停止
    message：S2F_FansRotatingStatus
    data：
    {
        "FansRotatingStatus": [xx, xx, xx, xx, xx, xx]
    }
    """
    if data:
        if not data["error"]:
            res = {
                "FansRotatingStatus": data["rotating_speed"]
            }
            socketio.emit("S2F_FansRotatingStatus", res)
        else:
            systemlog.log_warning(u"读风扇信息失败，数据无效: " + str(data))

def send_TempStatus(tag,data):
    """
    向前端发送当前温度信息，16路，数组表示16路不同的温度信息
    message：S2F_TemperatureStatus
    data：
    {
        "TemperatureStatus": [xx, ......]
    }
    """
    if data:
        res = {}
        res["Tag"] = tag
        resList = []
        for d in data["tempearture"]:
            if d > 32767:
                d = d - 32768
                resList.append(d * -0.1)
            else:
                resList.append(d * 0.1)
        res["TemperatureStatus"] = resList
        socketio.emit("S2F_TemperatureStatus", res)

def send_GateVoltageStatus(data):
    """
    向前端发送当前栅压信息，206路，分两组发送
    GateVoltageTage为0表示前103路，为1表示后103路
    message：S2F_GateVoltageStatus
    data：
    {
        "GateVoltageTag": xx,
        "GateVoltageStatus" [xx, xx, ...]
    }
    """
    res = {}
    if data:
        if data["gate_num_start"] == 0:
            res = {
                "GateVoltageTag": 0
            }
        elif data["gate_num_start"] == 70:
            res = {
                "GateVoltageTag": 1
            }
        res["GateVoltageStatus"] = data["gate_voltage"]
        socketio.emit("S2F_GateVoltageStatus", res)

def send_ElectricityStatus(data, ele_id):
    """
    向前端发送电流信息，13路
    message：S2F_ElectricityStatus
    data：
    {
        "ElectricityID": xx,
        "ElectricityStatus": [xx, xx, ...]
    }
    """
    if data:
        res = {
            "ElectricityID": ele_id,
            "ElectricityStatus": data["values"]
        }
        socketio.emit("S2F_ElectricityStatus", res)

def send_FirstElectricityStatu(data, ele_id):
    """
    向前端发送1级电流信息，13路
    message：S2F_ElectricityStatus
    data：
    {
        "ElectricityID": xx,
        "ElectricityStatus": xx
    }
    """
    if data:
        res = {
            "ElectricityID": ele_id,
            "ElectricityStatus": data["values"]
        }
        socketio.emit("S2F_FirstElectricityStatus", res)
def send_boardDisconnectWarning(data):
    """
    向前端发送失联板子的信息
    message：S2F_BoardDisconnectWarning
    data：
    {
    "BoardTag":  2
    }
    """
    if data:
        res = {
            "BoardTag": data
        }
        socketio.emit("S2F_BoardDisconnectWarning", res)
    else:
        systemlog.log_warning(u"发送失联信息失败，数据无效: " + str(data))
if __name__ == "__main__":
    #msg = [0x00, 0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00, 0x08, 0x00]
    #datas = receiveData.control_power_info(msg)
    #res = send_ControlBoardPower(datas)
    #print(res)

    msg = [0x01, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05]
    data = receiveData.temperature_info(msg)
    res = send_TempStatus(data)
    print(res)