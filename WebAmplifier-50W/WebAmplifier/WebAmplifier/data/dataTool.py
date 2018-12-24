'''

@author: wyndem
@Emil:   wyndem.wen@timevary.com
@FileName: dataTool.py
@Time: 2018/8/20 15:27
@Software: PyCharm
@Description: 

'''
from WebAmplifier.api.crc import getCRC


def addCrc(func):
    """
        给数据包装CRC
    """
    def wrapper(*args, **kw):
        data=func(*args, **kw)
        print(data)
        checRes = getCRC(data, len(data))
        data.append(checRes % 256)
        data.append(checRes // 256)
        return data
    return wrapper