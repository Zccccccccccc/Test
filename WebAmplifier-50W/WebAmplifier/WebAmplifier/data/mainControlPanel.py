from WebAmplifier.data.panel import Panel
from WebAmplifier.conf import setting
class MainControlPanel(Panel):#主控板
    '''
    主控板
    '''

    def __init__(self):
        self.__data = self.dataBuffer.copy()
        self.__data.append(0x01)
        self.__data.append(0x00)  # 功能段
        super(MainControlPanel, self).__init__(self.__data,self.IP[0])

    def setWorkInf(self,value):
        '''
        配置工作状态信息
        :param value:配置二进制文本
        :return:
        '''

        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x01)  # 数据标识符（单次读）
        __data.append(value)  # 设置值
        return self.addCrc(__data)
    def getWorkInf(self):
        '''
        配置工作状态信息
        :param value:
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x02)  # 数据标识符（单次读）
        __data.append(0x01)  # 设置值
        return self.addCrc(__data)
    def getKeyInf(self):
        '''
        获取按键信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x03)  # 数据标识符
        __data.append(0x01)  # 数据任意值
        return self.addCrc(__data)
    def getPowerInf(self):
        '''
        获取功放信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x04)  # 数据标识符
        __data.append(0x01)  # 数据任意值
        return self.addCrc(__data)
    def setAlarmInf(self,value):
        '''
        配置告警信息
        :param value: 配置二进制文本
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x05)  # 数据标识符
        __data.append(value)  # 设置值
        return self.addCrc(__data)