# -*- coding: utf-8 -*-

#######################################################
# FileName: threadfunc.py
# Description: 线程处理函数
#######################################################

from WebAmplifier.conf import setting
from WebAmplifier.syslog import systemlog

# 获取有效通信套接字
def get_ActiveSocket(IP):
    '''
    通过ip返回具体套接字链接
    :param IP:
    :return:
    '''
    try:
        sockRequest = setting.clientSocketList[str(IP)]
        return sockRequest
    except Exception:
        #systemlog.log_error(e)
        return None