from WebAmplifier.data.panel import Panel
import threading

class TempPanel(Panel):#温度
    '''
    温度检测板
    '''
    def __init__(self):
        self.__data = self.dataBuffer.copy()
        self.__IP = self.IP[2:4]
        self.__pant = [0, 0]
        self.__lock = threading.Lock()
    def getIP(self,index):
        '''
        温度检测板ip
        :param index:start 2 end 4
        :return:ip
        '''
        if index > 1:
            index = 1
        elif index <0:
            index = 0
        return self.__IP[index]
    def getTempInf(self, index):#获取温度信息
        '''
        获取温度信息
        :param index: 0~1
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x03 + index)
        __data.append(0x00)  # 功能段
        __data.append(0x02)  # 数据长度
        __data.append(0x01)  # 数据标识符（单次读）
        __data.append(0x01)  # 数据任意值
        return self.addCrc(__data)
    def getVersionInf(self,index=1):
        '''
        获取版本信息
        :param index: 过欠压板编号0-1
        :return:
        '''
        __data = self.dataBuffer.copy()
        __data.append(0x03 + index)  # 1-8个通道
        __data.append(0x00)  # 功能段
        __data.append(0x02)  # 数据长度
        __data.append(0xF0)  # 数据标识符
        __data.append(0x01)  # 数据标识符
        return self.addCrc(__data)
    def addPant(self,indexPass):
        '''
        通过索引增加第几块过欠压板的心跳，每调用一次+1
        :param indexPass: 通道编号0-1
        :return:
        '''
        with self.__lock:
            self.__pant[indexPass]+=1
    def getPant(self,indexPass):
        '''
        通过索引获取第几块过欠压板的心跳
        :param indexPass: 通道编号0-7
        :return: 心跳值
        '''
        return self.__pant[indexPass]
    def setPant(self,indexPass,value):
        '''
        通过索引设置第几块过欠压板的心跳
        :param indexPass: 通道编号0-1
        :param value: 心跳值
        :return:
        '''
        with self.__lock:
            self.__pant[indexPass] = value
    def checkPant(self,indexPass,maxPant=10):
        '''
        检查心跳值是否大于最大心跳值，大于返回true
        :return: true/false
        '''
        isTrue = False
        if self.getPant(indexPass)>maxPant:
            isTrue = True
        return isTrue