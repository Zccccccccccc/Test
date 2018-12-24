'''

@author: wyndem
@Emil:   wyndem.wen@timevary.com
@FileName: fan.py
@Time: 2018/8/20 16:17
@Software: PyCharm
@Description: 风扇

'''
import random

from WebAmplifier.Test.client import *
from WebAmplifier.data.dataTool import addCrc

logging.warning('< - - - - - 风扇测试程序 - - - - - >')

#风扇
@addCrc
def fan(cdata):
    cdata=cdata[4]
    #0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6, 0x03, 0x00, 0x03, 0x01]
    buf[4]=cdata
    buf[3]=1
    # 获取风扇信息
    if cdata == 0x01:
        buf[3] += 3
        buf.append(random.randint(0, 1))
        buf.append(random.randint(1, 31))
        buf.append(0)

        # 获取风扇转速信息
    elif cdata == 0x02:
        buf[3] += 1
        buf.append(random.randint(0, 1))
        for i in range(random.randint(1, 6)):
            buf[3] += 1
            buf.append(random.randint(0, 3))

    # 获取软件版本信息
    elif cdata == 0xF0:
        for i in range(3):
            buf[3] += 1
            buf.append(random.randint(0, 100))

    return buf

start(fan,getClinect())