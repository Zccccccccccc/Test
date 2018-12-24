'''

@author: wyndem
@Emil:   wyndem@qq.com
@FileName: currentInf.py
@Time: 2018/8/20 16:29
@Software: PyCharm
@Description: 欠压检测板

'''
import random

from WebAmplifier.Test.client import *
from WebAmplifier.data.dataTool import addCrc

logging.warning('< - - - - - 欠压检测板测试程序 - - - - - >')



# 压检测板
@addCrc
def currentInf(cdata):
    # 0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6,cdata[1], 0x00, 0x02, 0x01]

    #电流信息
    if cdata[4]==0x01:

        if random.randint(0, 1):
            # 读取失败,数据无效
            buf.append(0x01)
        else:
            #读取成功
            buf.append(0x00)
            buf[3] = 2
            for i in range(13):
                buf[3] += 2
                buf.append(random.randint(155, 255))
                buf.append(random.randint(155, 255))

    # 获取软件版本信息
    elif cdata == 0xF0:
        for i in range(3):
            buf[3] += 1
            buf.append(random.randint(0, 100))

    return buf
start(currentInf,getClinect())
