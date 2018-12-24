# -*- coding: utf-8 -*-

#######################################################
# FileName: toolsfunc.py
# Description: 工具型独立功能函数
#######################################################

import platform
import copy
import wmi
import pythoncom

from RadarFlaskWebProject.db import systemfunc
from RadarFlaskWebProject.admin import userfunc
from RadarFlaskWebProject.radar import device

#获取服务器系统信息
def getServerInfo():
    return platform.uname()

#获取服务器操作系统版本
def getServerOS():
    res = getServerInfo()
    return str(res[0]) + str(res[2]) + " - " + str(res[3])

#获取服务器节点名
def getServerName():
    return getServerInfo()[1]

#获取服务器体系结构
def getServerArchitecture():
    return getServerInfo()[4]

#获取服务器处理器型号
def getServerProcessors():
    return getServerInfo()[5]

#获取数据库信息
def getServerDB():
    db_info = {}
    db_infoList = []
    conn = systemfunc.connectDB()
    for tableName in systemfunc.DB_getTableNameList(conn):
        db_info['name'] = tableName
        db_info['size'] = systemfunc.DB_getTableSize(conn, tableName)
        temp = copy.deepcopy(db_info)
        db_infoList.append(temp)
    return db_infoList

#获取系统用户数据量
def getUserAmount():
    return userfunc.userAmount()

#获取系统设备数据量
def getDeviceAmount():
    return len(device.get_DeviceListName())

#获取系统数据数据量
def getDataAmount():
    conn = systemfunc.connectDB()
    res = systemfunc.DB_getTableSize(conn, "data")
    systemfunc.disconnectDB(conn)
    return res

#获取系统服务器处理器型号
def getServerProcessorType():
    processors = wmi.WMI()
    for core in processors.Win32_Processor():
        res = core.Name
    return res

#获取系统服务器处理器数windows
def getServerProcessorNum():
    processors = wmi.WMI()
    for core in processors.Win32_Processor():
        res = core.NumberOfCores
    return res

#获取系统服务器处理器当前使用率windows
def getServerProcessorUsage():
    processors = wmi.WMI()
    for core in processors.Win32_Processor():
        res = core.LoadPercentage
    return res

#获取系统服务器内存空间windows
def getServerRamSize():
    ramSize = 0
    system = wmi.WMI()
    for ram in system.Win32_ComputerSystem():
        try:
            ramSize = ramSize + int(ram.TotalPhysicalMemory)
        except Exception as e:
            continue
    return ramSize // 1024 // 1024

#获取系统服务器内存当前空闲量
def getServerRamFree():
    ramFree = 0
    system = wmi.WMI()
    for ram in system.Win32_OperatingSystem():
        try:
            ramFree = ramFree + int(ram.FreePhysicalMemory)
        except Exception as e:
            continue
    return ramFree // 1024

def getServerRamUsage():
    return int((getServerRamSize() - getServerRamFree()) / getServerRamSize() * 100)

#获取系统服务器硬盘空间windows
def getServerDiskSize():
    diskSize = 0
    disk = wmi.WMI()
    for disk in disk.Win32_LogicalDisk():
        try:
            diskSize = diskSize + int(disk.Size)
        except Exception as e:
            continue
    return diskSize // 1024 // 1024 // 1000
