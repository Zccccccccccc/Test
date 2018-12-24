'''

@author: wyndem
@Emil:   wyndem.wen@timevary.com
@FileName: gate.py
@Time: 2018/8/20 16:24
@Software: PyCharm
@Description: 栅压板

'''
import random

from WebAmplifier.Test.client import *
from WebAmplifier.data.dataTool import addCrc

logging.warning('< - - - - - 栅压板测试程序 - - - - - >')

#栅压板
@addCrc
def gate(cdata):
    # 0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6, 0x05, 0x00, 0x05, 0x01]
    buf[4] = cdata[4]
    buf[3] = 1
    #通道编号
    pasge=cdata[5]
    #单次度
    if cdata[4] == 0x01:
        buf[3] += 4
        buf.append(random.randint(0, 1))

        #栅压通道编号
        buf.append(pasge)
        # data1 = ''
        # data2=''
        # for x in range(8):
        #     data1 += str(random.randint(0, 1))
        #     data2 += str(random.randint(0, 1))
        #栅压通道电压值
        buf.append(random.randint(155, 255))
        buf.append(random.randint(155, 255))


    # 连续读栅压
    elif cdata[4]==0x02:
        #通道数量
        number=int(cdata[6])
        # 设置长度
        buf[3]+= 3
        buf.append(random.randint(0, 1))


        # 栅压通道编号
        buf.append(pasge)
        #栅压通道数量
        buf.append(number)

        if buf[5]==0x00:
            for i in range(number):
                # data = ''
                # for x in range(16):
                #     data += str(random.randint(0, 1))
                # buf.append(data)
                buf[3] +=2
                buf.append(random.randint(155, 255))
                buf.append(random.randint(155, 255))

    #单次写栅压
    elif cdata[4] == 0x03:

        #设置长度
        buf[3]=0x04
        buf.append(random.randint(0, 1))
        #栅压通道编号
        buf.append(pasge)
        #栅压通道电压值
        data = ''
        # for x in range(16):
        #     data += str(random.randint(0, 1))
        # buf.append(data)
        buf.append(random.randint(155, 255))
        buf.append(random.randint(155, 255))


    #连续写栅压
    elif cdata[4] == 0x04:

        # 设置长度
        buf[3] = 0x03
        # 通道数量
        number = int(cdata[6])

        buf.append(random.randint(0, 1))
        # 栅压起始通道编号
        buf.append(pasge)
        # 栅压通道数量
        buf.append(number)

    # 获取软件版本信息
    elif cdata == 0xF0:
        for i in range(3):
            buf[3] += 1
            buf.append(random.randint(0, 100))

    return buf

start(gate,getClinect())