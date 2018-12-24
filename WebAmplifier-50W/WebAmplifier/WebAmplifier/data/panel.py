import struct
import threading
from WebAmplifier.api import crc
from WebAmplifier.conf import setting
class Panel():
    __lock = None
    dataBuffer = [0xA6]
    __data=[]
    __IP=''
    __pant = 0
    IP = [key for key, value in setting.clientSocketList.items()]
    def getIP(self):
        return self.__IP
    def __init__(self,__data=[],ip=''):
        self.__data=__data
        self.__IP = ip
        #在init函数里面初始化 则每个继承当前类的 对象都有一把属于自己的lock,操作当前对象的锁不影响其他对象的锁
        self.__lock = threading.Lock()
    def addCrc(self,dataBuffer):
        crc1 = crc.getCRC(dataBuffer, len(dataBuffer))
        dataBuffer += self.to2byte(crc1)
        return struct.pack("%dB" % (len(dataBuffer)), *dataBuffer)
    def to2byte(self,value):
        byteList = []
        byteList.append(value % 256)
        byteList.append(value // 256)
        return byteList
    def getVersionInf(self):
        '''
        获取软件版本信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0xF0)  # 数据标识符
        __data.append(0x01)  # 数据标识符
        return self.addCrc(__data)
    def addPant(self):
        '''
        每调用一次增加1次心跳
        :return:
        '''
        with self.__lock:
            self.__pant+=1
    def getPant(self):
        '''
        获取心跳值
        :return:
        '''
        return self.__pant
    def setPant(self,value):
        '''
        设置心跳值
        :param value:
        :return:
        '''
        with self.__lock:
            self.__pant = value
    def checkPant(self,maxPant=10):
        '''
        检查心跳值是否大于最大心跳值，大于返回true,并将心跳之重新设置为0
        :return: true/false
        '''
        isTrue = False
        if self.__pant>maxPant:
            isTrue = True
        return isTrue