import logging
import socket
import struct

from WebAmplifier.api import crc
from WebAmplifier.conf.setting import TARGETPOINT_PORT
from WebAmplifier.data import receiveData

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


#ip_port = ('10.8.0.113', TARGETPOINT_PORT)
ip_port = ('127.0.0.1', TARGETPOINT_PORT)

def getClinect():

    # 生成一个socket对象
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 开启心跳维护
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    # 请求连接服务端
    client.connect(ip_port)
    return client


def start(func,client):
    while True:
        # 接收数据
        server_reply = client.recv(1024 * 1024 * 2)
        # 获取到客户端的数据
        clinect_data = struct.unpack("%dB" % len(server_reply), server_reply)
        # logging.warning('接收到数据:%s' % server_reply)
        resList = receiveData.sliceData(clinect_data)
        for res in resList:
            logging.warning('接收到数据:%s' % res)
            resData = receiveData.parseData(res)
            if resData['head'] != 0xA6:
                logging.error("head error")
                break
            if crc.checkData(res[:-2], resData['crc']):
                # 处理后的数据
                buf = func(res)
                logging.warning('发送数据:%s' % buf)
                res = struct.pack("%dB" % (len(buf)), *buf)
                client.send(res)