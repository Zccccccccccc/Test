# -*- coding: utf-8 -*-

#######################################################
# FileName: systemfunc.py
# Description: 反无人机雷达管理系统数据库相关操作的API函数

#反无人机雷达管理系统数据库结构如下：
#1、用户表（用户名，密码，角色）
# user (name, password, role)
#2、设备表（设备名，设备IP，服务器IP，设备状态，网络连接状态）
# device (deviceName, deviceIP, serverIP, deviceStatus, linkStatus)
#3、数据表（设备号，时间，距离，方位，高度，相位，速度，信噪比，信道，保留位）
# data (device, time, distance, azimuth, height, phase, speed, snr, channel, range)
#######################################################

import os

from WebAmplifier.conf import setting
from WebAmplifier.db import database
from WebAmplifier.syslog import systemlog

#初始化系统数据库
def initDB():
    if not os.path.isfile(setting.DATABASENAME) or not os.path.getsize(setting.DATABASENAME):
        conn = database.createDB(setting.DATABASENAME)
        if conn:
            createUserTable(conn)
            createDeviceTable(conn)
            createDataTable(conn)
            insertUserTableData(conn, "admin", "123123", "MANAGER")
        else:
            systemlog.log_error("初始化数据库失败！")
        disconnectDB(conn)

#连接数据库
def connectDB():
    return database.connectDB(setting.DATABASENAME)

#断开数据库
def disconnectDB(databaseHandler):
    return database.disconnectDB(databaseHandler)

#获取数据库信息
def DB_getInfo(databaseHandler):
    cmd = "SELECT name FROM sqlite_master WHERE type = 'table'"
    return database.selectDB_data(databaseHandler, cmd)

#获取数据库表格数据量
def DB_getTableSize(databaseHandler, tableName):
    for row in DB_getTableNameList(databaseHandler):
        cmd = "SELECT count(*) FROM " + str(tableName)
        (number_of_rows,) = database.selectDB_data(databaseHandler, cmd);
        return number_of_rows[0]

#获取数据库表格名
def DB_getTableNameList(databaseHandler):
    resList = []
    for row in DB_getInfo(databaseHandler):
        resList.append(','.join(row))
    return resList

#创建用户表
def createUserTable(databaseHandler):
    cmd = "CREATE TABLE user (name TEXT, password TEXT, role TEXT)"
    if not database.createDB_table(databaseHandler, cmd):
        systemlog.log_error("创建用户表失败！")

#清空用户表
def deleteUserTable(databaseHandler):
    cmd = "DELETE FROM user"
    if not database.deleteDB_table(databaseHandler, cmd):
        systemlog.log_error("清空用户表失败！")
        return False
    insertUserTableData(databaseHandler, "admin", "123123", "MANAGER")
    return True

#查询用户表数据
def selectUserTableData(databaseHandler, arguments = None):
    cmd = "SELECT * FROM user"
    if arguments != None:
        cmd += " " + str(arguments)
    return database.selectDB_data(databaseHandler, cmd)
        
#更新用户表数据
def updateUserTableData(databaseHandler, username, typeName = None, value = None):
    if typeName != None and value !=None :
        cmd = "UPDATE user SET " + str(typeName) + " = '" + str(value) + "' WHERE name = '" + str(username) + "'"
    else:
        cmd = ""
    if not database.updateDB_data(databaseHandler, cmd):
        systemlog.log_error("更新用户表失败")

#删除用户表数据
def deleteUserTableData(databaseHandler, typeName, value):
    if value == "admin":
        return False
    cmd = "DELETE FROM user WHERE " + str(typeName) + " = '" + str(value) + "'"
    if not database.deleteDB_data(databaseHandler, cmd):
        systemlog.log_error("删除用户失败")
        return False
    return True

#插入用户表数据
def insertUserTableData(databaseHandler, username, password, role):
    cmd = "INSERT INTO user (name, password, role) VALUES ('" + str(username) + "', '" + str(password) + "', '" + str(role) + "')"
    if not database.insertDB_data(databaseHandler, cmd):
        systemlog.log_error("插入用户数据失败")

#创建设备表
def createDeviceTable(databaseHandler):
    cmd = "CREATE TABLE device (deviceName TEXT, deviceIP TEXT, serverIP TEXT, deviceStatus TEXT, linkStatus TEXT)"
    if not database.createDB_table(databaseHandler, cmd):
        systemlog.log_error("创建设备表失败！")

#清空设备表
def deleteDeviceTable(databaseHandler):
    cmd = "DELETE FROM device"
    if not database.deleteDB_table(databaseHandler, cmd):
        systemlog.log_error("清空设备表失败！")
        return False
    return True

#查询设备表数据
def selectDeviceTableData(databaseHandler, arguments = None):
    cmd = "SELECT * FROM device"
    if arguments != None:
        cmd += " " + str(arguments)
    return database.selectDB_data(databaseHandler, cmd)

#更新设备表数据
def updateDeviceTableData(databaseHandler, deviceName, typeName = None, value = None):
    if typeName != None and value != None:
        cmd = "UPDATE device SET " + str(typeName) + " = '" + str(value) + "' WHERE deviceName = '" + str(deviceName) + "'"
    else:
        cmd = ""
    if not database.updateDB_data(databaseHandler, cmd):
        systemlog.log_error("更新设备表失败！")

#插入设备表数据
def insertDeviceTableData(databaseHandler, deviceName, deviceIP, serverIP, deviceStatus = 0, linkStatus = 0):
    cmd = "INSERT INTO device (deviceName, deviceIP, serverIP, deviceStatus, linkStatus) VALUES ('" + str(deviceName) + "', '" + str(deviceIP) + "', '" + str(serverIP) + "', '" + str(deviceStatus) + "', '" + str(linkStatus) + "')"
    if not database.insertDB_data(databaseHandler, cmd):
        systemlog.log_error("插入设备表数据失败！")

#删除设备表数据
def deleteDeviceTableData(databaseHandler, typeName, value):
    cmd = "DELETE FROM device WHERE " + str(typeName) + " = '" + str(value) + "'"
    if not database.deleteDB_data(databaseHandler, cmd):
        systemlog.log_error("删除设备表数据失败！")
        return False
    return True

#创建数据表
def createDataTable(databaseHandler):
    cmd = "CREATE TABLE data (device TEXT, time TEXT, distance TEXT, azimuth TEXT, height TEXT, phase TEXT, speed TEXT, snr TEXT, channel TEXT, range TEXT)"
    if not database.createDB_table(databaseHandler, cmd):
        systemlog.log_error("创建数据表失败！")

#清空数据表
def deleteDataTable(databaseHandler):
    cmd = "DELETE FROM data"
    if not database.deleteDB_table(databaseHandler, cmd):
        systemlog.log_error("清空数据表失败！")
        return False
    return True

#查询数据表数据
def selectDataTableData(databaseHandler, arguments = None):
    cmd = "SELECT * FROM data"
    if arguments != None:
        cmd += " " + str(arguments)
    return database.selectDB_data(databaseHandler, cmd)

#更新数据表数据
def updateDataTableData(databaseHandler, deviceName, typeName = None, value = None):
    if typeName != None and value != None:
        cmd = "UPDATE data SET " + str(typeName) + " = '" + str(value) + "' WHERE device = '" + str(deviceName) + "'"
    else:
        cmd = ""
    if not database.updateDB_data(databaseHandler, cmd):
        systemlog.log_error("更新数据表数据失败！")

#插入数据表数据
def insertDataTableData(databaseHandler, deviceName, saveTime, distance, azimuth, height, phase, speed, snr, channel, default):
    cmd = "INSERT INTO data (device, time, distance, azimuth, height, phase, speed, snr, channel, range) VALUES ('" + str(deviceName) + "', '" + str(saveTime) + "', '" + str(distance) + "', '" + str(azimuth) + "', '" + str(height) + "', '" + str(phase) + "', '" + str(speed) + "', '" + str(snr) + "', '" + str(channel) + "', '" + str(default) + "')"
    if not database.insertDB_data(databaseHandler, cmd):
        systemlog.log_error("插入数据表数据失败！")

#删除数据表数据
def deleteDataTableData(databaseHandler, typeName, value):
    cmd = "DELETE FROM data WHERE " + str(typeName) + " = '" + str(value) + "'"
    if not database.deleteDB_data(databaseHandler, cmd):
        systemlog.log_error("删除数据表数据失败！")
        return False
    return True
