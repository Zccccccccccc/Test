from WebAmplifier.data.panel import Panel
import threading

class DrainPanel(Panel):#欠压检测板
    '''
    欠压检测版
    '''
    def __init__(self):
        self.__IP = self.IP[5:11]
        self.__pant=[0,0,0,0,0,0]
        self.__lock = threading.Lock()
    def getIP(self,index):
        '''
        获取过欠压版ip
        :param index:start 0 end 7
        :return:ip
        '''
        if index > 5:
            index = 5
        elif index <0:
            index = 0
        return self.__IP[index]
    def getNomalCurrentInf(self,index=1):
        '''
        获取普通电流信息
        :param index:过欠压板编号1-6
        :return:
        '''
        __data = self.dataBuffer.copy()
        __data.append(5+index)#1-6个通道
        __data.append(0x00)#功能段
        __data.append(0x02)#数据长度段
        __data.append(0x01)#数据标识符（获取普通电流信息）
        __data.append(0x02)#数据含义任意值
        return self.addCrc(__data)
    def getFirstDriverCurrentInf(self,index=1):
        '''
        获取一级驱动电流信息
        :param index: 过欠压板编号
        :return:
        '''
        __data = self.dataBuffer.copy()
        __data.append(5+index)#1-6个通道
        __data.append(0x00)#功能段
        __data.append(0x02)#数据长度段
        __data.append(0x02)#数据标识符（获取一级驱动电流信息）
        __data.append(0x02)#数据含义任意值
        return self.addCrc(__data)
    def getVersionInf(self,index=1):
        '''
        获取版本信息
        :param index: 过欠压板编号1-5
        :return:
        '''
        __data = self.dataBuffer.copy()
        __data.append(5 + index)  # 1-8个通道
        __data.append(0x00)  # 功能段
        __data.append(0x02)  # 数据长度
        __data.append(0xF0)  # 数据标识符
        __data.append(0x01)  # 数据标识符
        return self.addCrc(__data)
    def addPant(self,indexPass):
        '''
        通过索引增加第几块过欠压板的心跳，每调用一次+1
        :param indexPass: 通道编号0-5
        :return:
        '''
        with self.__lock:
            self.__pant[indexPass]+=1
    def getPant(self,indexPass):
        '''
        通过索引获取第几块过欠压板的心跳
        :param indexPass: 通道编号0-5
        :return: 心跳值
        '''
        return self.__pant[indexPass]
    def setPant(self,indexPass,value):
        '''
        通过索引设置第几块过欠压板的心跳
        :param indexPass: 通道编号0-5
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