from WebAmplifier.data.panel import Panel
class AmplifierPanel(Panel):

    def getVersionInf(self,address):
        '''
        获取软件版本
        :param address: 地址
        :return:
        '''
        data = []
        data.append(address)  # 地址段
        data.append(0x00)  # 功能段
        data.append(0x02)  # 数据长度
        data.append(0xF0)  # 数据标识符
        data.append(0x00)  # 数据
        return self.addCrc(data)
    def getWorkInf(self,address):
        '''
        获取工作状态
        :param address: 地址
        :return:
        '''
        data = []
        data.append(address)#地址段
        data.append(0x00)#功能段
        data.append(0x02)#数据长度
        data.append(0x02)#数据标识符
        data.append(0x00)#数据
        return self.addCrc(data)
    def getAlarmInf(self,address):
        '''
        获取告警信息
        :param address:地址
        :return:
        '''
        data = []
        data.append(address)  # 地址段
        data.append(0x00)  # 功能段
        data.append(0x02)  # 数据长度
        data.append(0x03)  # 数据标识符
        data.append(0x00)  # 数据
        return self.addCrc(data)
    def getCurrentInf(self,address):
        '''
        获取告警信息
        :param address:地址
        :return:
        '''
        data = []
        data.append(address)  # 地址段
        data.append(0x00)  # 功能段
        data.append(0x02)  # 数据长度
        data.append(0x10)  # 数据标识符
        data.append(0x00)  # 数据
        return self.addCrc(data)

    def GetTempInf(self,address):
        '''
        获取告警信息
        :param address:地址
        :return:
        '''
        data = []
        data.append(address)  # 地址段
        data.append(0x00)  # 功能段
        data.append(0x02)  # 数据长度
        data.append(0x11)  # 数据标识符
        data.append(0x00)  # 数据
        return self.addCrc(data)
    def singleReadGate(self,address,index):
        '''
        单次读珊压
        :param address:地址
        :param index:栅压通道编号(1~7)
        :return:
        '''
        data = []
        data.append(address)  # 地址段
        data.append(0x00)  # 功能段
        data.append(0x02)  # 数据长度
        data.append(0x20)  # 数据标识符
        data.append(index)  # 数据
        return self.addCrc(data)
    def continueReadGate(self,address,startIndex,num):
        '''
        连续读珊压
        :param address: 地址
        :param startIndex: 开始通道
        :param num: 数量
        :return:
        '''
        data = []
        data.append(address)  # 地址段
        data.append(0x00)  # 功能段
        data.append(0x03)  # 数据长度
        data.append(0x21)  # 数据标识符
        data.append(startIndex)  # 数据
        data.append(num)
        return self.addCrc(data)
