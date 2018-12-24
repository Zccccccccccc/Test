from WebAmplifier.data.panel import Panel
import threading

class FanPanel(Panel):#风扇
    '''
    风扇板
    '''
    def __init__(self):
        self.__data = self.dataBuffer.copy()
        self.__IP = self.IP[11:14]
        self.__pant = [0,0,0]
        self.__lock = threading.Lock()
    def getIP(self,index):
        '''
        风扇板ip
        :param index:start 13 end 15
        :return:ip
        '''
        if index > 2:
            index = 2
        elif index <0:
            index = 0
        return self.__IP[index]
    def getFanInf(self, index):
        '''
        获取风扇信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x0C + index)
        __data.append(0x00)  # 功能段
        __data.append(0x02)  # 数据长度
        __data.append(0x01)  # 数据标识符（单次读）
        __data.append(0x01)  # 数据任意值
        return self.addCrc(__data)
    def getFanSpeedInf(self, index):
        '''
        获取风扇转速信息
        :param index: 0-2
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x0C + index)
        __data.append(0x00)  # 功能段
        __data.append(0x02)  # 数据长度
        __data.append(0x02)  # 数据标识符（单次读）
        __data.append(0x01)  # 数据任意值
        return self.addCrc(__data)
    def getVersionInf(self,index=1):
        '''
        获取版本信息
        :param index: 过欠压板编号0-2
        :return:
        '''
        __data = self.dataBuffer.copy()
        __data.append(0x0C + index)  # 1-3个通道
        __data.append(0x00)  # 功能段
        __data.append(0x02)  # 数据长度
        __data.append(0xF0)  # 数据标识符
        __data.append(0x01)  # 数据标识符
        return self.addCrc(__data)
    def addPant(self,indexPass):
        '''
        通过索引增加第几块过欠压板的心跳，每调用一次+1
        :param indexPass: 通道编号0-2
        :return:
        '''
        with self.__lock:
            self.__pant[indexPass]+=1
    def getPant(self,indexPass):
        '''
        通过索引获取第几块过欠压板的心跳
        :param indexPass: 通道编号0-2
        :return: 心跳值
        '''
        return self.__pant[indexPass]
    def setPant(self,indexPass,value):
        '''
        通过索引设置第几块过欠压板的心跳
        :param indexPass: 通道编号0-2
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