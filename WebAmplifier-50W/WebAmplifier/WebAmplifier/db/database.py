# -*- coding: utf-8 -*-

#######################################################
# FileName: database.py
# Description: sqllit数据库相关的API函数
#######################################################

import os
import sqlite3
from flask import g
from   WebAmplifier.syslog import systemlog

#创建数据库
def createDB(databaseName):
    return connectDB(databaseName)

#删除数据库
def deleteDB():
    pass

#连接数据库
def connectDB(databaseName):
    try:
        #conn = getattr(g, "_db", None)
        #if conn is None:
            #conn = g._db = sqlite3.connect(databaseName)
        conn = sqlite3.connect(databaseName)
    except Exception as e:
        systemlog.log_error(e)
        conn = None
    return conn

#断开数据库连接
def disconnectDB(databaseHandler):
    databaseHandler.close()

#创建数据库表格
def createDB_table(databaseHandler, cmd):
    status = False
    try:
        databaseHandler.execute(cmd)
        databaseHandler.commit()
        status = True
    except Exception as e:
        systemlog.log_error(e)
        databaseHandler.rollback()
    finally:
        return status

#删除数据库表格
def deleteDB_table(databaseHandler, cmd):
    status = False
    try:
        databaseHandler.execute(cmd)
        databaseHandler.commit()
        status = True
    except Exception as e:
        systemlog.log_error(e)
        databaseHandler.rollback()
    finally:
        return status

#数据库查询数据
def selectDB_data(databaseHandler, cmd):
    res_row = {}
    try:
        databaseHandler.row_factory = sqlite3.Row
        res = databaseHandler.cursor()
        res.execute(cmd)
        res_row = res.fetchall()
    except Exception as e:
        systemlog.log_error(e)
    finally:
        return res_row

#数据库插入数据
def insertDB_data(databaseHandler, cmd):
    status = False
    try:
        res = databaseHandler.cursor()
        res.execute(cmd)
        databaseHandler.commit()
        status = True
    except Exception as e:
        systemlog.log_error(e)
        databaseHandler.rollback()
    finally:
        return status

#数据库更新数据
def updateDB_data(databaseHandler, cmd):
    status = False
    try:
        databaseHandler.execute(cmd)
        databaseHandler.commit()
        status = True
    except Exception as e:
        systemlog.log_error(e)
        databaseHandler.rollback()
    finally:
        return status

#数据库删除数据
def deleteDB_data(databaseHandler, cmd):
    status = False
    try:
        res = databaseHandler.cursor()
        res.execute(cmd)
        databaseHandler.commit()
        status = True
    except Exception as e:
        systemlog.log_error(e)
        databaseHandler.rollback()
    finally:
        return status

