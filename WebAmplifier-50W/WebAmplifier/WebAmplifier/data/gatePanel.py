from WebAmplifier.data.panel import Panel
from WebAmplifier.api.knob import *


class GatePanel(Panel):#栅压

    '''
    栅压板
    '''
    def __init__(self):
        self.__data = self.dataBuffer.copy()
        self.__data.append(0x05)
        self.__data.append(0x00)  # 功能段
        super(GatePanel, self).__init__(self.__data,self.IP[4])
    def SingleReadGate(self,number):
        '''
        单次读取栅压
        :param number:
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)# 数据长度
        __data.append(0x01)# 数据标识符（单次读）
        __data.append(number)#通道编号
        return self.addCrc(__data)
    def ContinueReadGate(self,startNum,lenNum):
        '''
        连续读栅压
        :param startNum:
        :param lenNum:
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x03)  # 数据长度
        __data.append(0x02)  # 数据标识符（连续读）
        __data.append(startNum)  # 起始通道编号
        __data.append(lenNum)  # 通道数量
        return self.addCrc(__data)
    def SingleWriteGate(self,num,value):
        ''''
        单次写栅压
        '''
        __data = self.__data.copy()
        __data.append(0x04)  # 数据长度
        __data.append(0x03)  # 数据标识符（单次写栅压）
        __data.append(num)  # 通道编号
        __data += self.to2byte(value)  # 设置值
        return self.addCrc(__data)
    def ContinueWriteGate(self,startNum,values):
        '''
        连续写栅压
        :param startNum:
        :param values:
        :return:
        '''
        __data = self.__data.copy()
        __data.append(3+len(values)*2)  # 数据长度
        __data.append(0x04)  # 数据标识符（单次写栅压）
        __data.append(int(startNum))  # 通道编号
        __data.append(len(values))  # 通道数量
        for v in values:# 设置值
            __data += self.to2byte(int(v))
        return self.addCrc(__data)
    def ConfigAchKnobInf(self,zy,pl,gl):
        '''
        配置a通道旋钮信息
        :param zy:增益int
        :param pl:频率float
        :param gl:功率int
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x07)  # 数据长度
        __data.append(0x05)  # 数据标识符
        __data += self.to2byte(gain_to_v(zy))  # 先查表然后转换成2个字节
        print(gain_to_v(zy))
        __data += self.to2byte(freq_to_v(pl))  # 频率
        print(freq_to_v(pl))
        __data += self.to2byte(power_to_v(gl,pl))  # 功率
        print(power_to_v(gl,pl))
        print(__data)
        return self.addCrc(__data)
    def ConfigBchKnobInf(self,zy,pl,gl):
        '''
        配置b通道旋钮信息
        :param zy:增益int
        :param pl:频率float
        :param gl:功率int
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x07)  # 数据长度
        __data.append(0x06)  # 数据标识符
        __data += self.to2byte(gain_to_v(zy))  # 先查表然后转换成2个字节
        __data += self.to2byte(freq_to_v(pl))  # 频率
        __data += self.to2byte(power_to_v(gl, pl))  # 功率
        return self.addCrc(__data)
    def getAchKnobInf(self):
        '''
        获取a弦钮信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x07)  # 数据标识符
        __data.append(0x01)  # 任意数据
        return self.addCrc(__data)
    def getBchKnobInf(self):
        '''
        获取a弦钮信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x08)  # 数据标识符
        __data.append(0x01)  # 任意数据
        return self.addCrc(__data)
    def getDacOnlineInf(self):
        '''
        获取DAC在位信息
        :return:
        '''
        __data = self.__data.copy()
        __data.append(0x02)  # 数据长度
        __data.append(0x09)  # 数据标识符
        __data.append(0x01)  # 任意数据
        return self.addCrc(__data)
if __name__ == '__main__':
    g = GatePanel()
    print(g.to2byte(2567))
    #print(g.ConfigAchKnobInf(1,10.6,49))