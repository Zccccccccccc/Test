import math
import random
import socket
import struct
import threading
import logging



'''

    这是测试服务端：默认端口9999

'''

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='print-info.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s： %(asctime)s ---%(filename)s(%(name)s)---->  %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

m_sCrc_ta = [
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
    0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
    0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
    0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
    0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
    0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
    0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
    0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
    0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
    0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
    0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
    0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
    0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
    0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
    0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
    0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
    0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
    0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
    0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
    0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
    0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
    0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
    0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
    0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
    0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
    0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
    0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
    0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
    0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040
     ]



def getCRC(valueData, nLength):
    valueIndex = 0
    crcValue = 0

    for i in range(0, nLength):
        valueIndex = int(crcValue & 0xFF) ^ valueData[i] & 0xFF
        crcValue1 = int(int(crcValue / math.pow(2, 8)) & 0xFF)
        crcValue = crcValue1 ^ m_sCrc_ta[valueIndex]

        if crcValue >= 65536:
            crcValue = crcValue % 65536

    return crcValue




def fw(c):
    clinect_data=con.recv(1024*1024*2)
    #获取到客户端的数据
    clinect_data= struct.unpack("%dB" % len(clinect_data), clinect_data)
    #判断帧头段
    if len(clinect_data) > 0 and clinect_data[0] == 0xA6:
        #告警板
        if clinect_data[1]==0x02:
            #clinect_data[4] 获取告警板的数据标识符
            logging.warning('进入到告警板')
            buf=warning(clinect_data[4])
        #风扇板
        elif clinect_data[1]==0x03:
            logging.warning('进入到风扇板')
            buf=fan(clinect_data[4])
        #温度检测
        elif clinect_data[1]==0x04:
            logging.warning('进入到温度检测')
            buf=temp(clinect_data[4])
        #栅压板
        elif clinect_data[1]==0x05:
            logging.warning('进入到栅压板')
            buf=gate(clinect_data)
        #压检测板
        elif clinect_data[1] <=13:
            logging.warning('进入到压检测板')
            buf=currentInf(clinect_data)

    logging.info('未加crc的数据为：%s' % buf)
    #crc
    checRes=getCRC(buf,len(buf))
    buf.append(checRes % 256)
    buf.append(checRes // 256)
    logging.info('发送的数据为：%s'%buf)

    #转换数据格式发送
    res = struct.pack("%dB" % (len(buf)), *buf)
    c.send(res)
    #c.close()


#告警板
def warning(cdata):
    buf = [0xA6,0x02,0x00,0x02,0x01]
    #判断标识符
    if cdata == 0x01:
        if random.randint(0,1):
            #无警告
            buf.append(0x00)
        else:
            buf.append(0x01)
            #有警告
            for t in range(5):
                for rx in [random.randint(155,255),random.randint(155,255), random.randint(155,255), random.randint(155,255)]:
                    buf.append(rx)
            buf[3]=22
        return buf

#风扇
def fan(cdata):
    #0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6, 0x03, 0x00, 0x02, 0x01]
    # 判断标识符
    if cdata == 0x01:
        if random.randint(0, 1):
            buf.append(0x00)
        else:
            buf.append(0x01)
        buf.append(random.randint(155,255))

        return buf

#温度
def temp(cdata):
    # 0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6, 0x04, 0x00, 0x01, 0x01]
    if cdata == 0x01:
        if random.randint(0,1):
            buf.append(0x01)
        else:
            # 有警告
            for x in range(103):
                buf.append(random.randint(155, 255))
            buf[3]=102

        return buf

#栅压板
def gate(cdata):
    # 0:段头 1:地址段 2:功能段 3:数据长度段 4:数据标识
    buf = [0xA6, 0x05, 0x00, 0x05, 0x01]
    #通道编号
    pasge=cdata[5]
    #单次度
    if cdata[4] == 0x01:
        if random.randint(0,1):
            #读取失败,数据无效
            buf.append(0x01)
        else:
            # 读取成功
            buf.append(0x00)

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
        #数据标识
        buf[4]=0x02
        #通道数量
        number=int(cdata[6])

        if random.randint(0,1):
            #连续读取失败,数据为空
            buf.append(0x01)
            #设置长度
            buf[3]=0x03
        else:
            #读取成功
            buf.append(0x00)
            # 设置长度
            buf[3] = number*2

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
                buf.append(random.randint(155, 255))
                buf.append(random.randint(155, 255))

    #单次写栅压
    elif cdata[4] == 0x03:
        #设置长度
        buf[3]=0x04
        if random.randint(0, 1):
            # 读取失败,数据无效
            buf.append(0x01)
        else:
            buf.append(0x00)
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
        buf[3] = 0x04
        # 通道数量
        number = int(cdata[6])

        if random.randint(0, 1):
            # 读取失败,数据无效
            buf.append(0x01)
        else:
            buf.append(0x00)
        # 栅压起始通道编号
        buf.append(pasge)
        # 栅压通道数量
        buf.append(number)

    return buf


# 压检测板
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

            for i in range(13):
                buf.append(random.randint(155, 255))
                buf.append(random.randint(155, 255))
            buf[3]=28

    return buf
if __name__ == '__main__':
    ip_port = ('127.0.0.1', 9999)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定
    sk.bind(ip_port)
    # 设置最多链接数
    sk.listen(5)
    logging.info('服务器启动成功..')
    while True:
        con, addr = sk.accept()
        logging.info('客户端地址：%s'% str(addr))
        t = threading.Thread(target=fw, args=(con,))
        t.start()