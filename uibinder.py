from PyQt5.QtWidgets import QMessageBox
from ui import *
from uimain import MyWindow,MyDialog

from http.cookiejar import CookieJar,LWPCookieJar
from urllib import request
from urllib.request import Request,urlopen,HTTPCookieProcessor,build_opener
from urllib.parse import urlencode
import ssl

import json

import os.path

ssl._create_default_https_context = ssl._create_unverified_context

cookie_obj=CookieJar()
cookie_handle=HTTPCookieProcessor(cookie_obj)
opener = build_opener(cookie_handle)

name_button_dialog_menu = '菜单'
name_button_save_dialog_menu='保存菜单'
name_button_dialog_parameters = '接口参数'
name_button_save_dialog_parameters='保存参数'
name_button_dialog_comments = '接口备注'
name_button_save_dialog_comments='保存备注'
name_button_dialog_system = '添加环境'
name_button_save_dialog_system='保存环境'

name_file_sys='sys.json'
name_file_menu='menu.json'
name_file_parameters='parameters.json'
name_file_comments='comments.json'

def init(myWin:MyWindow,myDialog:MyDialog):
    # create new file
    datas = get_sys()
    
    firstKeys = datas.keys()
    myWin.comboBox_3.clear()
    myWin.comboBox.clear()
    if len(firstKeys) > 0:
        myWin.comboBox_3.addItems(firstKeys)

        for key in firstKeys:
            urls = datas[key]
            for urlTmp in urls:
                myWin.comboBox.addItem(urlTmp['sysUrl'])
                if urlTmp['isCurrent'] == '1':
                    myWin.comboBox_3.setCurrentText(key)
                    myWin.comboBox.setCurrentText(urlTmp['sysUrl'])
    cascadeUrl(myWin)

    

def get_sys():
    if not os.path.exists(name_file_sys):
        with open(name_file_sys,'w+') as f:
            pass

    datas = {}
    with open(name_file_sys, 'r') as f:
        str1 = f.read()
        if str1 is not None and str1 != '':
            datas:dict = json.loads(str1)
    return datas

def cascadeUrl(myWin:MyWindow):
    datas:dict = get_sys()
    firstKeys = datas.keys()
    if len(firstKeys) > 0:
        for key in firstKeys:
            syst = myWin.comboBox_3.currentText()
            if key == syst:
                print('key=', key)
                urls = datas[key]
                myWin.comboBox.clear()
                for urlTmp in urls:
                    myWin.comboBox.addItem(urlTmp['sysUrl'])
                    if urlTmp['isCurrent'] == '1':
                        myWin.comboBox.setCurrentText(urlTmp['sysUrl'])
                        

def setDomainUrl(myWin:MyWindow):
    datas = get_sys()
    firstKeys = datas.keys()
    if len(firstKeys) > 0:
        for key in firstKeys:
            syst = myWin.comboBox_3.currentText()
            domain_url = myWin.comboBox.currentText()
            urls = datas[key]
            for urlTmp in urls:
                sysUrl = urlTmp['sysUrl']
                if (key == syst and sysUrl == domain_url):
                    urlTmp['isCurrent']='1'
                else:
                    urlTmp['isCurrent']='0'
    #write
    with open(name_file_sys,'w+') as f:
        f.write(json.dumps(datas,indent=2,ensure_ascii=False))

def login(myWin):
    QMessageBox.information(myWin, "提示",  "用户自定义功能", QMessageBox.Yes)

def open_dialog(myWin:MyWindow,myDialog:MyDialog):
    sender = myWin.sender()
    event = sender.text()
    myDialog.textEdit.setPlainText('')
    if event == name_button_dialog_menu:
        myDialog.pushButton.setText(name_button_save_dialog_menu)
        datas:dict = get_file_content(name_file_menu)
        syst = myWin.comboBox_3.currentText()
        myDialog.textEdit.setPlainText(datas.get(syst))
            
    elif event == name_button_dialog_parameters or event == name_button_dialog_comments:
        name_button = name_button_save_dialog_parameters
        name_file = name_file_parameters
        if event == name_button_dialog_comments:
            name_button = name_button_save_dialog_comments
            name_file = name_file_comments
        myDialog.pushButton.setText(name_button)
        datas = get_file_content(name_file)
        syst = myWin.comboBox_3.currentText()
        sys_domain = myWin.comboBox.currentText()
        url = myWin.plainTextEdit.toPlainText()
        myDialog.textEdit.setPlainText(datas.get(syst+sys_domain+url))
    elif event == name_button_dialog_system:
        myDialog.pushButton.setText(name_button_save_dialog_system)

        # create new file
        if not os.path.exists(name_file_sys):
            with open(name_file_sys,'w+') as f:
                pass

        datas = {
                    'sysName':[
                        {'sysUrl':'',
                        'loginUrl':'',
                        'isCurrent':''}
                    ]
                }
        with open(name_file_sys, 'r') as f:
            str1 = f.read()
            if str1 is not None and str1 != '':
                datas = json.loads(str1)
        
        
        #syst = myWin.comboBox_3.currentText()
        #myDialog.textEdit.setPlainText(datas)
        myDialog.textEdit.setPlainText(json.dumps(datas,indent=2,ensure_ascii=False))
        
    myDialog.show()

def get_file_content(file_name):
    # create new file
    if not os.path.exists(file_name):
        with open(file_name,'w+') as f:
            pass

    datas = {}
    with open(file_name, 'r') as f:
        str = f.read()
        if str is not None and str != '':
            datas = json.loads(str)
    return datas

def save_dialog(myWin:MyWindow,myDialog:MyDialog):
    sender = myDialog.sender()
    event = sender.text()
    print('event=',event)
    if event == name_button_save_dialog_menu:
        save_dialog_menu(myWin,myDialog)
        QMessageBox.information(myDialog, "提示",  "保存菜单成功", QMessageBox.Yes)
    elif event == name_button_save_dialog_parameters:
        save_dialog_parameters(myWin,myDialog,name_file_parameters)
        QMessageBox.information(myDialog, "提示",  "保存参数成功", QMessageBox.Yes)
    elif event == name_button_save_dialog_comments:
        save_dialog_parameters(myWin,myDialog,name_file_comments)
        QMessageBox.information(myDialog, "提示",  "保存备注成功", QMessageBox.Yes)
    elif event == name_button_save_dialog_system:
        save_dialog_system(myWin,myDialog,name_file_sys)
        QMessageBox.information(myDialog, "提示",  "保存环境成功", QMessageBox.Yes)
    


def save_dialog_menu(myWin:MyWindow,myDialog:MyDialog):
    syst = myWin.comboBox_3.currentText()
    val = myDialog.textEdit.toPlainText()
    
    #read
    menus = {}
    with open(name_file_menu, 'r') as f:
        str = f.read()
        if str is not None and str != '':
            menus = json.loads(str)
    #write
    with open(name_file_menu,'w+') as f:
        menus[syst] = val
        f.write(json.dumps(menus,indent=2,ensure_ascii=False))

def save_dialog_parameters(myWin:MyWindow,myDialog:MyDialog,name_file):
    syst = myWin.comboBox_3.currentText()
    sys_domain = myWin.comboBox.currentText()
    url = myWin.plainTextEdit.toPlainText()
    val = myDialog.textEdit.toPlainText()
    
    #read file 
    parameters = {}
    with open(name_file, 'r') as f:
        str = f.read()
        if str is not None and str != '':
            parameters = json.loads(str)
    #write
    with open(name_file,'w+') as f:
        parameters[syst+sys_domain+url] = val
        f.write(json.dumps(parameters,indent=2,ensure_ascii=False))

def save_dialog_system(myWin:MyWindow,myDialog:MyDialog,name_file):
    syst = myWin.comboBox_3.currentText()
    val = myDialog.textEdit.toPlainText()
    
    #read
    #write
    with open(name_file,'w+') as f:
        f.write(val)
    
    #init 
    init(myWin,myDialog)


def send_url(myWin:MyWindow):
    domain_url = myWin.comboBox.currentText()
    print('domain_url=',domain_url)
    url = myWin.plainTextEdit.toPlainText()
    full_url = domain_url + url
    parameters = myWin.textEdit.toPlainText()
    method = myWin.comboBox_2.currentText()
    request = Request(url=full_url,data=bytes(parameters,encoding='utf-8'),headers={})
    response = opener.open(request)
    result = response.read().decode()
    myWin.textBrowser.setText(json.dumps(json.loads(result),indent=2,ensure_ascii=False))

