'''

@author: wyndem
@Emil:   wyndem.wen@timevary.com
@FileName: control.py
@Time: 2018/8/20 15:05
@Software: PyCharm
@Description:  这是主控板的测试程序

'''
import random

from WebAmplifier.Test.client import *
from WebAmplifier.data.dataTool import addCrc

logging.warning('< - - - - - 主控板测试程序 - - - - - >')

@addCrc
def control(cdata):
    cdata = cdata[4]
    # 0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6,0x01,0x00,0x03,0x01]

    buf[3] = 1
    buf[4] = cdata
    if random.randint(0, 1):
        buf.append(0x00)
    else:
        buf.append(0x01)
    buf[3] += 1

    #配置和获取工作状态信息
    if cdata==0x02 or cdata==0x01 :
        buf[3]+=1
        buf.append(random.randint(1,7))

    #按键信息
    elif cdata==0x03:
        buf[3] += 1
        buf.append(random.randint(0,240))
    #获取功率信息
    elif cdata==0x04:
        for i in range(8):
            buf[3] += 2
            buf.append(random.randint(155, 255))
            buf.append(random.randint(155, 255))
    #配置获取A、B通道旋钮信息
    elif cdata==0x05 or cdata==0x06 or cdata==0x07 or cdata==0x08:
        for i in range(3):
            buf[3] += 1
            buf.append(random.randint(0, 100))
    #获取软件版本信息
    elif cdata==0xF0:
        for i in range(3):
            buf[3] += 1
            buf.append(random.randint(0, 100))
    return buf

start(control,getClinect())