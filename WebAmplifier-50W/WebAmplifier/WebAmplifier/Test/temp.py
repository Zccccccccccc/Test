'''

@author: wyndem
@Emil:   wyndem.wen@timevary.com
@FileName: temp.py
@Time: 2018/8/20 16:20
@Software: PyCharm
@Description: 温度

'''
import random


from WebAmplifier.Test.client import *
from WebAmplifier.data.dataTool import addCrc

logging.warning('< - - - - - 温度板测试程序 - - - - - >')


#温度
@addCrc
def temp(cdata):
    cdata=cdata[4]
    # 0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6, 0x04, 0x00, 0x02, 0x01]
    buf[4] = cdata
    buf[3] = 1
    if cdata == 0x01:
        buf[3] += 1
        if random.randint(0,1):
            buf.append(0x01)
        else:
            buf.append(0x00)
            # 有警告
            for x in range(103):
                buf[3]+=1
                buf.append(random.randint(155, 255))
    # 获取软件版本信息
    elif cdata == 0xF0:
        for i in range(3):
            buf[3] += 1
            buf.append(random.randint(0, 100))
        return buf

start(temp,getClinect())