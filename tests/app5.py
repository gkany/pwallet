#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,time
import wx,telnetlib
# import win32api,win32con
import re,os


#远程telnet进入OLT命令行
def TelnetOpen(event):
    print("")

def DrawPanel():
    #设置画布上面的控制信息
    app=wx.App()
    win= wx.Frame(None,title='OLT Auto Config ONU-Shelly',size=(850,700))
    #新增一张画布
    panel = wx.Panel(win)
   # panel.SetBackgroundColour('yellow')
    #选择中兴C300还是华为56XX OLT系列
    oltText = wx.StaticText(panel,label=u'OLT VendorID:')
    zte_checkBox = wx.CheckBox(panel,label=u"ZTE OLT")
    hw_checkBox = wx.CheckBox(panel,label=u"HUAWEI OLT")

    #设置IP地址进行telnet登录
    staticText = wx.StaticText(panel,label=u'IP_Address:')
    ip_textCtl = wx.TextCtrl(panel)
    #在Panel创建一些组件如按钮，文本框
    login_textCtl = wx.TextCtrl(panel)
    staticText10 = wx.StaticText(panel,label=u'Account:')
    pwd_textCtl = wx.TextCtrl(panel)
    staticText12 = wx.StaticText(panel,label=u'Password:')
    telnetBtn = wx.Button(panel,label=u'Telnet_OLT')
    #打开按纽绑定事件函数，处理操作
    telnetBtn.Bind(wx.EVT_BUTTON,TelnetOpen)
    #给控件设置背景颜色：如telnetBtn设置绿色背景，如图
    telnetBtn.SetBackgroundColour("Green")

    shelf_textCtl = wx.TextCtrl(panel)
    staticText1 = wx.StaticText(panel,label=u'Shelf_No:')
    slot_textCtl = wx.TextCtrl(panel)
    staticText2 = wx.StaticText(panel,label=u'Slot_No:')
    pon_textCtl = wx.TextCtrl(panel)
    staticText3 = wx.StaticText(panel,label=u'Port_No:')
    onu_textCtl = wx.TextCtrl(panel)
    staticText4 = wx.StaticText(panel,label=u'ONU_ID:')
    vlan_textCtl = wx.TextCtrl(panel)
    staticText11 = wx.StaticText(panel,label=u'VlanID:') 

    onutypeText = wx.StaticText(panel,label=u'PON Type:') 
    gpon_checkBox = wx.CheckBox(panel,label=u"GPON")
    epon_checkBox = wx.CheckBox(panel,label=u"EPON")
    showButton = wx.Button(panel,label=u'ShowOLTCfg')
    vlanButton = wx.Button(panel,label=u'VlanCreate')
    showvidButton = wx.Button(panel,label=u'ShowVidCfg')
    untagButton = wx.Button(panel,label=u'UplinkUntagCfg')
    tagButton = wx.Button(panel,label=u'UplinkTagCfg')

    #添加一个标签
    staticText5 = wx.StaticText(panel,label=u'Note:Click the ShowOLTCfg button to view the configuration in each case based on the configured shelf, slot, pon port, ONUID, including the configuration of the uplink interface.\nlike:show run interface gpon_olt_1/15/1 and show run interface gpon_olt_1/15/1:1 and show run inter gei_1/19/1 ',pos=(1,107),size=(650,50))
    onuregisterText = wx.StaticText(panel,label=u'Note:The ONU registration process is as follows:')

    #SN 复制
    copySnText = wx.StaticText(panel,label=u'2.Copy the already found SN(MAC) to the textBox:')
    sn_textCtl = wx.TextCtrl(panel)
    changeOnuText = wx.StaticText(panel,label=u'Exec Replace_ONU:')
    changeButton = wx.Button(panel,label=u'Replace ONU')

    #添加两个按钮，一个用于显示配置，一个用于一键自动化配置ONU信息
    findButton = wx.Button(panel,label=u'1.Find unauth ONU')
    registerButton = wx.Button(panel,label=u'3.Register ONU')
    cfgButton = wx.Button(panel,label=u'4.Config ONU')
    viewButton = wx.Button(panel,label=u'Find all_Online_ONU')
    deleteButton = wx.Button(panel,label=u'Delete_ONU')

    #修改控件的父对象改成panel 而不是Frame，Panel的父对象是Frame
    dbaTest1 = wx.StaticText(panel,label='ZTE Config Parameter:')
    dbaTest = wx.StaticText(panel,label='1.DBA:')
    dba100M_checkBox = wx.CheckBox(panel,label=u"100M")
    dba1000M_checkBox = wx.CheckBox(panel,label=u"1G")
    onutypeTest = wx.StaticText(panel,label='2.ONU_Type:')
    onutype_textCtl = wx.TextCtrl(panel)
    onutypeButton = wx.Button(panel,label=u'Create ONU_TYPE')

    #HUAWEI 配置参数
    dbaTest2 = wx.StaticText(panel,label='HUAWEI Config Parameter:')
    dbaTest3 = wx.StaticText(panel,label='1.DBA:')
    dba100M_checkBox1 = wx.CheckBox(panel,label=u"100M")
    dba1000M_checkBox1 = wx.CheckBox(panel,label=u"1G")

    #HUAWEI模版
    Test2 = wx.StaticText(panel,label='2.ont-lineprofile-id:')
    onuline_textCtl = wx.TextCtrl(panel)
    onulineButton = wx.Button(panel,label=u'Create linePro')
    Test3 = wx.StaticText(panel,label='3.ont-srvprofile-id:')
    onusrv_textCtl = wx.TextCtrl(panel)
    onusrvButton = wx.Button(panel,label=u'Create SrvPro')
    #一个大的显示文本框
    showContent = wx.TextCtrl(panel,style=wx.TE_MULTILINE | wx.HSCROLL,size=(850,300)) #增加可移动下拉

    #开始面板上布局
    #实例化一个尺寸器，默认水平
    #proportion：相对比例：只能设置 0,1,2,3等，0是保持本身大小，按比例显示大小，1比0的宽一倍，以此类推
    #flag：填充的样式和方向,wx.EXPAND为完整填充，wx.ALL为填充的方向
    #border：边框
    box = wx.BoxSizer() #默认是创建横向BoxSizer
    box.Add(oltText,proportion = 1,flag = wx.EXPAND|wx.ALIGN_RIGHT,border = 3)
    #box.AddStretchSpacer(1) #将第一个控件加如伸缩控件
    box.Add(zte_checkBox,proportion = 1,flag = wx.EXPAND|wx.ALIGN_LEFT,border = 3)
    box.Add(hw_checkBox,proportion = 1,flag = wx.EXPAND|wx.ALIGN_LEFT,border = 3)

    box1 = wx.BoxSizer()
    box1.Add(staticText,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box1.Add(ip_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box1.Add(staticText10,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box1.Add(login_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box1.Add(staticText12,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box1.Add(pwd_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box1.Add(telnetBtn,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 0)

    box2 = wx.BoxSizer()
    box2.Add(staticText1,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(shelf_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(staticText2,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(slot_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(staticText3,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(pon_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(staticText4,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(onu_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(staticText11,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box2.Add(vlan_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)

    box3 = wx.BoxSizer()
    box3.Add(onutypeText,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box3.Add(gpon_checkBox,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box3.Add(epon_checkBox,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box3.Add(showButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box3.Add(vlanButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box3.Add(showvidButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box3.Add(untagButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box3.Add(tagButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)

    box4 = wx.BoxSizer()
    box4.Add(copySnText,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box4.Add(sn_textCtl,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box4.Add(changeOnuText,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box4.Add(changeButton,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)

    box5 = wx.BoxSizer()
    box5.Add(findButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box5.Add(registerButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box5.Add(cfgButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box5.Add(viewButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box5.Add(deleteButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)

    box6 = wx.BoxSizer()
    box6.Add(dbaTest1,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box6.Add(dbaTest,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box6.Add(dba100M_checkBox,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box6.Add(dba1000M_checkBox,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box6.Add(onutypeTest,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box6.Add(onutype_textCtl,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box6.Add(onutypeButton,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)

    box7 = wx.BoxSizer()
    box7.Add(dbaTest2,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box7.Add(dbaTest3,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box7.Add(dba100M_checkBox1,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)
    box7.Add(dba1000M_checkBox1,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 3)

    box8 = wx.BoxSizer()
    box8.Add(Test2,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box8.Add(onuline_textCtl,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box8.Add(onulineButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box8.Add(Test3,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box8.Add(onusrv_textCtl,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)
    box8.Add(onusrvButton,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3)

    # box9 = wx.BoxSizer()
    # box9.Add(showContent,proportion = 3,flag = wx.EXPAND|wx.ALL,border = 3)
    #创建一个垂直尺寸器，把一些横向Box或控件都装载其中
    v_box = wx.BoxSizer(wx.VERTICAL)
    v_box.Add(box,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)# 随着窗口托大控件一直保持居中或居左 
    v_box.Add(box1,proportion = 0,flag = wx.ALIGN_LEFT ,border = 3)
    v_box.Add(box2,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(box3,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(staticText5,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(onuregisterText,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(box4,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(box5,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(box6,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(box7,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(box8,proportion = 0,flag = wx.ALIGN_LEFT,border = 3)
    v_box.Add(showContent,proportion = 5,flag = wx.ALIGN_LEFT,border = 3)

    '''
    flag 参数详解：
    wx.EXPAND|wx.ALL 会随着窗口变大而变化
    wx.ALIGN_CENTER  保持居中
    wx.ALIGN_LEFT  居左
    wx.ALIGN_RIGHT 居右
    wx.ALIGN_TOP  置顶
    wx.ALIGN_BOTTOM  置底部
    wx.ALIGN_CENTER_VERTICAL  垂直居中
    wx.ALIGN_CENTER_HORIZONTAL   水平居中
    wx.ALIGN_CENTER  居中
    '''
    #设置画布的主尺寸器（一层包一层）

    panel.SetSizer(v_box) 
    win.Show()
    app.MainLoop()

DrawPanel()
