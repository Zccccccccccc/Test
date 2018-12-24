from WebAmplifier.data.panel import Panel
class WarningPanel(Panel):#警告
    '''
    告警板
    '''
    def __init__(self):
        self.__data = self.dataBuffer.copy()
        self.__data.append(0x02)
        self.__data.append(0x00)  # 功能段
        super(WarningPanel, self).__init__(self.__data,self.IP[1])
    def getWorkInf(self):
        '''
        获取告警板工作信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x02)  # 数据标识符（单次读）
        __data.append(0x01)  # 数据任意值
        return self.addCrc(__data)
    def setWorkInf(self,value):#读取工作状态
        '''
        设置告警板信息
        :param value:
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x01)  # 数据标识符
        __data.append(value)  # 设置值
        return self.addCrc(__data)
    def getWarningInf(self):
        '''
        获取告警板警告信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x03)  # 数据标识符（单次读）
        __data.append(0x01)  # 数据任意值
        return self.addCrc(__data)