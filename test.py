# -*- coding:utf-8 -*-

import os
import os.path
import zipfile
from zipfile import *
import sys
from time import sleep

import _MT4ManagerAPI
import MT4ManagerAPI
import ctypes

from multiprocessing import Process

def f(name):
    while(1):
        sleep(1000)
        print ('hello', name)



#CALLBACK = ctypes.WINFUNCTYPE(None, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
#@CALLBACK
#def Notify_FuncEx( code, type, data, param):
def Notify_FuncEx( code, type ):
    if code == _MT4ManagerAPI.PUMP_START_PUMPING:
        print ("code = PUMP_START_PUMPING, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_STOP_PUMPING:
        print ("code = PUMP_STOP_PUMPING, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_SYMBOLS:
        print ("code = PUMP_UPDATE_SYMBOLS, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_GROUPS:
        print ("code = PUMP_UPDATE_GROUPS, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_USERS:
        print ("code = PUMP_UPDATE_USERS, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_ONLINE:
        print ("code = PUMP_UPDATE_ONLINE, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_BIDASK:
        print ("code = PUMP_UPDATE_BIDASK, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_NEWS:
        print ("code = PUMP_UPDATE_NEWS, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_NEWS_BODY:
        print ("code = PUMP_UPDATE_NEWS_BODY, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_MAIL:
        print ("code = PUMP_UPDATE_MAIL, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_TRADES:
        print ("code = PUMP_UPDATE_TRADES, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_REQUESTS:
        print ("code = PUMP_UPDATE_REQUESTS, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_PLUGINS:
        print ("code = PUMP_UPDATE_PLUGINS, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_ACTIVATION:
        print ("code = PUMP_UPDATE_ACTIVATION, type = %s"%type)
    elif code == _MT4ManagerAPI.PUMP_UPDATE_MARGINCALL:
        print ("code = PUMP_UPDATE_MARGINCALL, type = %s"%type)
    else:
        print ("code = PUMP_PING, type = %s"%type) 
 

def build_array(l):
	nitems = len(l)
	a = ptrcreate("double",0,nitems)
	i = 0
	for item in l:
		ptrset(a,item,i)
		i = i + 1
	return a

# Python function to turn an array into list
def build_list(a,nitems):
	l = []
	for i in range(0,nitems):
		l.append(ptrvalue(a,i))
	return l

if __name__ == '__main__':

    m_factory = MT4ManagerAPI.CManagerFactory("mtmanapi.dll")
    m_factory.WinsockStartup()
    #m_factory.Init("mtmanapi.dll");
    if m_factory.IsValid() == False:
        print ("Failed to create manager interface.")

    print (hex(m_factory.Version()))

    ExtManager = m_factory.Create(0x4000670)
    if ExtManager is None:
        print ("Failed to create manager interface.")
    print ("ExtManager = %s"%ExtManager)

    ExtDealer = m_factory.Create(0x4000670)
    if ExtDealer is None:
        print ("Failed to create manager interface.")
    print ("ExtDealer = %s"%ExtDealer)
        
    ExtManagerPump = m_factory.Create(0x19002e9)
    if ExtManagerPump is None:
        print ("Failed to create manager interface.")
    print ("ExtManagerPump = %s"%ExtManagerPump)
        
    res = ExtManager.Connect("127.0.0.1:443");
    print ("ExtManager.Connect: res = %s"%res)
    if res is not 0:
        print ("Connecting MT4 Server failed.")

    res = ExtManager.IsConnected()
    if res is 0:
        print ("MT4 Server is not connected.")
        
    res = ExtManager.Login(100,"12345678")
    print ("ExtManager.Login: res = %s"%res)
    if res is not 0:
        print ("Login to MT4 Server failed.")
        

    total = MT4ManagerAPI.intp()
    users = ExtManager.UsersRequest( total )
    print ("total = %s"%total.value())
    print ("users = %s"%users)
    userarr = MT4ManagerAPI.UserRecordArray_frompointer(users)

    """
    Very strange，the address of userarr[i] are same，
    but userarr[i].login are correct
    """

    print ("userarr = %s"%userarr)
    '''
    for i in range(total.value()):
        print (userarr[i].login)
        print (userarr[i].group)
        print (userarr[i].leverage)
    #print (userarr[1].login)
    '''
    ##############################################################
    trades = ExtManager.TradesRequest( total )
    print ("total = %s"%total.value())
    print ("trades = %s"%trades)
    tradearr = MT4ManagerAPI.TradeRecordArray_frompointer(trades)
    print ("tradearr = %s"%tradearr)
    '''
    for i in range(total.value()):
        print (tradearr[i].login)
        print (tradearr[i].order)
        print (tradearr[i].symbol)
        print (tradearr[i].cmd)
        print (tradearr[i].volume)
    '''
    ###############################################################

    res = ExtManagerPump.Connect("127.0.0.1:443");
    print ("ExtManagerPump.Connect: res = %s"%res)
    if res is not 0:
        print ("Connecting MT4 Server failed.")

    res = ExtManagerPump.IsConnected()
    if res is 0:
        print ("MT4 Server is not connected.")
        
    res = ExtManagerPump.Login(100,"12345678")
    print ("ExtManagerPump.Login: res = %s"%res)
    if res is not 0:
        print ("Login to MT4 Server failed.")


    res = ExtManagerPump.PumpingSwitchEx(Notify_FuncEx,MT4ManagerAPI.CLIENT_FLAGS_HIDETICKS|MT4ManagerAPI.CLIENT_FLAGS_HIDENEWS|MT4ManagerAPI.CLIENT_FLAGS_HIDEMAIL,None)
    print ("res = %s"%res)
    """
    total1 = MT4ManagerAPI.intp()
    users = ExtManagerPump.UsersGet( total1 )
    print ("total1 = %s"%total1.value())
    """
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
    ###############################################################
    m_factory.WinsockCleanup()

