from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow
import sys

from ui import *
from uidialog import *
from uibinder import *

class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow,self).__init__(parent)
        self.setupUi(self)

class MyDialog(QDialog,Ui_Dialog):
    def __init__(self, parent=None):
        super(MyDialog,self).__init__(parent)
        self.setupUi(self)

def binder(myWin:MyWindow,myDialog:MyDialog):
    myWin.pushButton.clicked.connect(lambda:open_dialog(myWin,myDialog))
    myWin.pushButton_2.clicked.connect(lambda:open_dialog(myWin,myDialog))
    myWin.pushButton_4.clicked.connect(lambda:open_dialog(myWin,myDialog))
    myWin.pushButton_5.clicked.connect(lambda:open_dialog(myWin,myDialog))
    myWin.pushButton_3.clicked.connect(lambda:send_url(myWin))
    myWin.pushButton_6.clicked.connect(lambda:login(myWin))

    #set myDialog
    myDialog.setWindowModality(QtCore.Qt.ApplicationModal)
    myDialog.pushButton.clicked.connect(lambda:save_dialog(myWin,myDialog))

    #init
    init(myWin,myDialog)
    
    myWin.comboBox_3.currentIndexChanged.connect(lambda:cascadeUrl(myWin))
    myWin.comboBox.currentIndexChanged.connect(lambda:setDomainUrl(myWin))

def setDomainUrl(myWin):
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
                
    


if __name__=='__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myDialog = MyDialog()
    binder(myWin,myDialog)
    myWin.showMaximized()
    sys.exit(app.exec_())