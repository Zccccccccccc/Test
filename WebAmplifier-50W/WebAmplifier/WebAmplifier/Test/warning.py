'''

@author: wyndem
@Emil:   wyndem.wen@timevary.com
@FileName: warning.py
@Time: 2018/8/20 16:08
@Software: PyCharm
@Description: 这是告警版测试程序

'''
import random

from WebAmplifier.Test.client import *
from WebAmplifier.data.dataTool import addCrc

logging.warning('< - - - - - 告警板测试程序 - - - - - >')


#告警板
@addCrc
def warning(cdata):
    cdata=cdata[4]
    # 0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6,0x02,0x00,0x03,cdata]
    buf[3]=1

    #获取告警信息
    if cdata == 0x03:
        if random.randint(0,1):
            #无警告
            buf.append(0x00)
            buf[3]+=1
        else:
            buf.append(0x01)
            buf[3] += 1
            #有警告
            for t in range(5):
                for rx in [random.randint(155,255) % 256,random.randint(155,255) // 256, random.randint(155,255) % 256, random.randint(155,255) // 256]:
                    buf[3] += 1
                    buf.append(rx)

    #配置、获取工作状态信息
    elif cdata==0x01 or cdata==0x02:
        buf[3] += 2
        if random.randint(0, 1):
            buf.append(0x01)
        else:
            buf.append(0x00)
        buf.append(random.randint(1, 7))
    #获取软件版本信息
    elif cdata==0xF0:
        for i in range(3):
            buf[3] += 1
            buf.append(random.randint(0, 100))
    return buf

start(warning,getClinect())