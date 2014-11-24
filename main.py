import sys
import random
from PyQt4 import QtGui, QtCore
from RFID import *
from DrupalConnector import *

class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.initUI()
    self.checkCardReader()

  def initUI(self):
    cWidget = QtGui.QWidget(self)

    vBox = QtGui.QVBoxLayout()
    vBox.setSpacing(2)

    self.createBtn = QtGui.QPushButton('Create account', cWidget)
    self.connect(self.createBtn, QtCore.SIGNAL('clicked()'), self.createBtnPressed);

    self.activateBtn = QtGui.QPushButton('Activate account', cWidget)
    self.connect(self.activateBtn, QtCore.SIGNAL('clicked()'), self.activateBtnPressed);

    self.infoBtn = QtGui.QPushButton('Get information', cWidget)
    self.connect(self.infoBtn, QtCore.SIGNAL('clicked()'), self.infoBtnPressed);

    self.increaseBtn = QtGui.QPushButton('Increase dots', cWidget)
    self.connect(self.increaseBtn, QtCore.SIGNAL('clicked()'), self.increaseBtnPressed);

    self.decreaseBtn = QtGui.QPushButton('Decrease dots', cWidget)
    self.connect(self.decreaseBtn, QtCore.SIGNAL('clicked()'), self.decreaseBtnPressed);

    vBox.addWidget(self.createBtn)
    vBox.addWidget(self.activateBtn)
    vBox.addWidget(self.infoBtn)
    vBox.addWidget(self.increaseBtn)
    vBox.addWidget(self.decreaseBtn)
      
    cWidget.setLayout(vBox)
    self.setCentralWidget(cWidget)
    self.resize(200, 100)
    center(self)
    self.setWindowTitle('opendot manager')


  def checkCardReader(self):
    ports = list(rfid_reader.get_ports())
    text, ok = QtGui.QInputDialog.getItem(self, "Select port", "Please choose the port connected to the card reader:", ports, 0, False)

    if not ok or not text:
      QtGui.QMessageBox.critical(self, 'opendot manager', "Please connect the card reader")
      sys.exit()
    try:
      rfid_reader.connect(str(text))
    except serial.SerialException, e:
      QtGui.QMessageBox.critical(self, 'opendot manager', str(e))
      sys.exit()

  def infoBtnPressed(self):
    print ">>> Get user info"
    infoDialog = InfoDialog(self)
    infoDialog.deleteLater()

  def createBtnPressed(self):
    print ">>> Create user"
    createDiag = CreateDialog(self)
    createDiag.exec_()
    createDiag.deleteLater()

  def activateBtnPressed(self):
    print ">>> Activate user"
    activateDiag = ActivateDialog(self)
    activateDiag.exec_()
    activateDiag.deleteLater()

  def increaseBtnPressed(self):
    print ">>> Increase dots"
    increaseDiag = IncreaseDialog(self)
    increaseDiag.deleteLater()

  def decreaseBtnPressed(self): 
    print ">>> Decrease dots"
    decreaseDiag = DecreaseDialog(self)
    decreaseDiag.deleteLater()


#### 
##
## LOGIN WINDOW
##
####

class LoginWindow(QtGui.QWidget):
  def __init__(self, main):
    super(LoginWindow, self).__init__()
    self.MainWindow = main
    self.initUI()
    self.checkServer()

  def initUI(self):
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    self.usernameLabel = QtGui.QLabel("Username")
    self.usernameLine = QtGui.QLineEdit()
    self.passwordLabel = QtGui.QLabel("Password")
    self.passwordLine = QtGui.QLineEdit()
    self.passwordLine.setEchoMode(QtGui.QLineEdit.Password)
    self.loginBtn = QtGui.QPushButton('Login')
    self.connect(self.loginBtn, QtCore.SIGNAL('clicked()'), self.doLogin);

    grid.addWidget(self.usernameLabel,0,0)
    grid.addWidget(self.usernameLine,0,1)
    grid.addWidget(self.passwordLabel,1,0)
    grid.addWidget(self.passwordLine,1,1)
    grid.addWidget(self.loginBtn,2,1)

    self.setLayout(grid)
    self.setGeometry(500, 300, 200, 100)
    center(self)
    self.setWindowTitle('opendot manager - login')

  def checkServer(self):
    try:
      result = connector.connect()
    except Exception, e:
      QtGui.QMessageBox.critical(self,  'Error', str(e))
      sys.exit()


  def doLogin(self):
    username = str(self.usernameLine.text())
    password = str(self.passwordLine.text())

    if (len(username) == 0 or len(password) == 0):
      QtGui.QMessageBox.critical(self,  'Error',  'Wrong credentials')
    else:
      self.loginBtn.setDisabled(True)
      waitingCursor(self)
      
      try:
        result = connector.login(username, password)
      except Exception, e:
        QtGui.QMessageBox.critical(self,  'Error',  str(e))
        return
      finally:
        self.loginBtn.setDisabled(False)
        normalCursor(self)

      self.MainWindow.show()
      self.close()


  def keyPressEvent(self, e):        
    if e.key() == QtCore.Qt.Key_Return:
      self.doLogin()


#### 
##
## CREATE DIALOG
##
####

class CreateDialog(QtGui.QDialog):
  def __init__(self, parent=None):
    super(CreateDialog, self).__init__()
    self.initUI()
    self.readCard()

  def initUI(self):
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    self.cardIdLabel = QtGui.QLabel('Card number:');
    self.cardId = QtGui.QLabel();
    self.usernameLabel = QtGui.QLabel('Username:');
    self.username = QtGui.QLineEdit();
    self.nameLabel = QtGui.QLabel('Name:');
    self.name = QtGui.QLineEdit();
    self.surnameLabel = QtGui.QLabel('Surname:');
    self.surname = QtGui.QLineEdit();
    self.emailLabel = QtGui.QLabel('Email:');
    self.email = QtGui.QLineEdit();
    self.confirmBtn = QtGui.QPushButton('Confirm')
    self.connect(self.confirmBtn, QtCore.SIGNAL('clicked()'), self.confirm)

    grid.addWidget(self.cardIdLabel,0,0)
    grid.addWidget(self.cardId,0,1)
    grid.addWidget(self.usernameLabel,1,0)
    grid.addWidget(self.username,1,1)
    grid.addWidget(self.nameLabel,2,0)
    grid.addWidget(self.name,2,1)
    grid.addWidget(self.surnameLabel,3,0)
    grid.addWidget(self.surname,3,1)
    grid.addWidget(self.emailLabel,4,0)
    grid.addWidget(self.email,4,1)
    grid.addWidget(self.confirmBtn,5,1)

    self.setLayout(grid)
    self.setGeometry(500, 300, 200, 100)
    center(self)
    self.setWindowTitle('opendot manager - activate user')

  def readCard(self):
    QtGui.QMessageBox.question(self, 'Reading', 'Pass the card over the card reader')

    cid = rfid_reader.read_from_serial()

    cb = QtGui.QApplication.clipboard()
    cb.clear(mode=cb.Clipboard)
    cb.setText(cid, mode=cb.Clipboard)

    self.cardId.setText(cid)

  def confirm(self):
    cid = str(self.cardId.text())
    user = str(self.username.text())
    name = str(self.name.text())
    surname = str(self.surname.text())
    email = str(self.email.text())

    if (len(user) > 0 and len(name) > 0 and len(surname) > 0 and len(email) > 0):
      u = {}
      u['name'] = user
      u['mail'] = email
      u['field_nome'] = {'und': [{'value': name}]}
      u['field_cognome'] = {'und': [{'value': surname}]}
      u['notify'] = '1'
      u['status'] = '1'
      u['pass'] = ''.join( [chr(random.randint(97,122)) for i in xrange(0,10)] )

      waitingCursor(self)
      try:
        connector.create(u)
        connector.activate(user, cid, False)
      except Exception, e:
        QtGui.QMessageBox.critical(self, 'Error', str(e))
        return
      finally:
        normalCursor(self)
      
      QtGui.QMessageBox.information(self, 'Success', 'New user \"{}\" created!'.format(user))
      self.close()
    else:
      QtGui.QMessageBox.critical(self, 'Error', 'Missing fields!')

#### 
##
## INFORMATION DIALOG
##
####

class InfoDialog(QtGui.QDialog):
  def __init__(self, parent=None):
    super(InfoDialog, self).__init__()
    self.initUI()
    self.readCard()

  def initUI(self):
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    self.cardIdLabel = QtGui.QLabel('Card number:');
    self.cardId = QtGui.QLabel();
    self.usernameLabel = QtGui.QLabel('Username:');
    self.username = QtGui.QLabel();
    self.nameLabel = QtGui.QLabel('Name:');
    self.name = QtGui.QLabel();
    self.surnameLabel = QtGui.QLabel('Surname:');
    self.surname = QtGui.QLabel();
    self.dotsLabel = QtGui.QLabel('Dots:');
    self.dots = QtGui.QLabel();

    grid.addWidget(self.cardIdLabel,0,0)
    grid.addWidget(self.cardId,0,1)
    grid.addWidget(self.usernameLabel,1,0)
    grid.addWidget(self.username,1,1)
    grid.addWidget(self.nameLabel,2,0)
    grid.addWidget(self.name,2,1)
    grid.addWidget(self.surnameLabel,3,0)
    grid.addWidget(self.surname,3,1)
    grid.addWidget(self.dotsLabel,4,0)
    grid.addWidget(self.dots,4,1)

    self.setLayout(grid)
    self.setGeometry(500, 300, 200, 100)
    center(self)
    self.setWindowTitle('opendot manager - activate user')

  def readCard(self):
    QtGui.QMessageBox.question(self, 'Reading', 'Pass the card over the card reader')

    cid = rfid_reader.read_from_serial()

    cb = QtGui.QApplication.clipboard()
    cb.clear(mode=cb.Clipboard)
    cb.setText(cid, mode=cb.Clipboard)

    self.cardId.setText(cid)
    
    waitingCursor(main)
    try:
      user = connector.get_user(cid)
    except Exception, e:
      QtGui.QMessageBox.critical(self, 'Error', str(e))
      self.close()
      return
    finally:
      normalCursor(main)

    self.currUser = User(user)
    self.username.setText(self.currUser.getUsername())
    self.name.setText(self.currUser.getName())
    self.surname.setText(self.currUser.getSurname())
    self.dots.setText(str(self.currUser.getDots()))
    self.exec_()


#### 
##
## ACTIVATION DIALOG
##
####

class ActivateDialog(QtGui.QDialog):
  def __init__(self, parent=None):
    super(ActivateDialog, self).__init__()
    self.initUI()
    self.readCard()

  def initUI(self):
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    self.cardIdLabel = QtGui.QLabel('Card number:');
    self.cardId = QtGui.QLabel();
    self.usernameLabel = QtGui.QLabel('Username:');
    self.usernameLine = QtGui.QLineEdit();
    self.activateBtn = QtGui.QPushButton('Activate')
    self.connect(self.activateBtn, QtCore.SIGNAL('clicked()'), self.doActivation)

    grid.addWidget(self.cardIdLabel,0,0)
    grid.addWidget(self.cardId,0,1)
    grid.addWidget(self.usernameLabel,1,0)
    grid.addWidget(self.usernameLine,1,1)
    grid.addWidget(self.activateBtn,2,1)

    self.setLayout(grid)
    self.resize(200, 100)
    center(self)
    self.setWindowTitle('opendot manager - activate user')

  def readCard(self):
    QtGui.QMessageBox.question(self, 'Reading', 'Pass the card over the card reader')

    cId = rfid_reader.read_from_serial()

    self.cardId.setText(cId)

    cb = QtGui.QApplication.clipboard()
    cb.clear(mode=cb.Clipboard )
    cb.setText(cId, mode=cb.Clipboard)


  def doActivation(self):
    user = str(self.usernameLine.text())
    cid = str(self.cardId.text())

    if (len(user) > 0):
      waitingCursor(self)
      try:
        result = connector.activate(user, cid, True)
      except Exception, e:
        QtGui.QMessageBox.critical(self, 'Error', str(e))
        return
      finally:
        normalCursor(self)

      QtGui.QMessageBox.information(self, 'Success', 'User "{}" activated!'.format(user))
      self.close()

    else:
      QtGui.QMessageBox.critical(self, 'Error', 'Wrong username')




####
##
## INCREASE DOTS DIALOG
##
####

class IncreaseDialog(QtGui.QDialog):
  def __init__(self, parent=None):
    super(IncreaseDialog, self).__init__()

    self.initUI()
    self.readCard()

  def loadButtons(self):
    self.font = QtGui.QFont()
    self.font.setFamily("Open Sans")
    self.font.setBold(True)

    self.smallBtn = QtGui.QPushButton()
    self.font.setPointSize(11)
    self.smallBtn.setFont(self.font)
    self.smallBtn.setText("SMALL")
    self.smallBtn.resize(100, 50)
    self.connect(self.smallBtn, QtCore.SIGNAL('clicked()'), lambda plan="small": self.doIncrease(plan))

    self.mediumBtn = QtGui.QPushButton()
    self.font.setPointSize(13)
    self.mediumBtn.setFont(self.font)
    self.mediumBtn.setText("MEDIUM")
    self.mediumBtn.resize(100, 50)
    self.connect(self.mediumBtn, QtCore.SIGNAL('clicked()'), lambda plan="medium": self.doIncrease(plan))

    self.largeBtn = QtGui.QPushButton()
    self.font.setPointSize(15)
    self.largeBtn.setFont(self.font)
    self.largeBtn.setText("LARGE")
    self.largeBtn.resize(100, 50)
    self.connect(self.largeBtn, QtCore.SIGNAL('clicked()'), lambda plan="large": self.doIncrease(plan))

    self.manualBtn = QtGui.QPushButton()
    self.manualBtn.setText("Pay Per Use")
    self.manualBtn.resize(100, 50)
    self.connect(self.manualBtn, QtCore.SIGNAL('clicked()'), lambda plan="ppu": self.doIncrease(plan))

    self.confirmBtn = QtGui.QPushButton('Confirm')
    self.connect(self.confirmBtn, QtCore.SIGNAL('clicked()'), self.confirm)

  def initUI(self):
    self.loadButtons()

    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    self.userLabel = QtGui.QLabel("Username")
    self.username = QtGui.QLabel()
    self.currBalanceLabel = QtGui.QLabel("Current Balance")
    self.currBalance = QtGui.QLabel()
    self.newBalanceLabel = QtGui.QLabel("New Balance")
    self.newBalance = QtGui.QLabel()

    # labels
    grid.addWidget(self.userLabel,0,0)
    grid.addWidget(self.username,0,1)
    grid.addWidget(self.currBalanceLabel,1,0)
    grid.addWidget(self.currBalance,1,1)
    grid.addWidget(self.newBalanceLabel,2,0)
    grid.addWidget(self.newBalance,2,1)

    # buttons
    grid.addWidget(self.smallBtn,3,0)
    grid.addWidget(self.mediumBtn,3,1)
    grid.addWidget(self.largeBtn,3,2)
    grid.addWidget(self.manualBtn,3,3)
    grid.addWidget(self.confirmBtn,4,3)

    self.setLayout(grid)
    #self.resize(500, 460)
    center(self)
    self.setWindowTitle('opendot manager - increase dots')


  def readCard(self):
    QtGui.QMessageBox.question(self, 'Reading', 'Pass the card over the card reader')

    cId = rfid_reader.read_from_serial()

    cb = QtGui.QApplication.clipboard()
    cb.clear(mode=cb.Clipboard )
    cb.setText(cId, mode=cb.Clipboard)

    waitingCursor(main)
    try:
      user = connector.get_user(cId)
    except Exception, e:
      QtGui.QMessageBox.critical(self, 'Error', str(e))
      self.close()
      return
    finally:
      normalCursor(main)

    self.currUser = User(user)
    self.balance = self.currUser.getDots()
    self.username.setText(self.currUser.getUsername())
    self.currBalance.setText(str(self.currUser.getDots()))
    self.newBalance.setText(str(self.balance))
    self.exec_()

  def doIncrease(self, plan):

    if (plan == "small"):
      self.balance += 50
    elif (plan == "medium"):
      self.balance += 100
    elif (plan == "large"):
      self.balance += 250
    elif (plan == "ppu"):
      dots, ok = QtGui.QInputDialog.getText(self, 'Purchased dots', 'Number of dots purchased:')

      if (ok and len(dots) > 0):
        self.balance += float(dots)

    self.newBalance.setText(str(self.balance))

  def confirm(self):
    if (self.balance == float(self.currBalance.text())):
      self.close()
    else:
      reply = QtGui.QMessageBox.question(self, 'Confirmation', "New balance will be {} dots, confirm?".format(self.balance), QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
      if (reply == QtGui.QMessageBox.Yes):
        self.currUser.setDots(self.balance)
        waitingCursor(self)
        print self.currUser.getDots()
        try:
          connector.update(self.currUser)
        except Exception, e:
          QtGui.QMessageBox.critical(self, 'Error', str(e))
          return
        finally:
          normalCursor(self)
      
        QtGui.QMessageBox.information(self, 'Success', 'New balance confirmed!')
        self.close()
      


#### 
##
## DECREASE DOTS DIALOG
##
####

class DecreaseDialog(QtGui.QDialog):
  def __init__(self, parent=None):
    super(DecreaseDialog, self).__init__()

    if sys.platform.startswith('win'):
      self.icons_dir = os.path.dirname(os.path.abspath(sys.argv[0])) + "\icons"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
      self.icons_dir = "icons"
	  
    self.initUI()
    self.readCard()

  def loadIcons(self):
    self.icon = QtGui.QIcon()
    self.icon1 = QtGui.QIcon()
    self.icon2 = QtGui.QIcon()
    self.icon3 = QtGui.QIcon()
    self.icon4 = QtGui.QIcon()
    self.icon5 = QtGui.QIcon()
    self.icon6 = QtGui.QIcon()
    self.icon7 = QtGui.QIcon()

    self.icon.addFile(os.path.join(self.icons_dir, "01.png"))
    self.icon1.addFile(os.path.join(self.icons_dir, "02.png"))
    self.icon2.addFile(os.path.join(self.icons_dir, "03.png"))
    self.icon3.addFile(os.path.join(self.icons_dir, "04.png"))
    self.icon4.addFile(os.path.join(self.icons_dir, "05.png"))
    self.icon5.addFile(os.path.join(self.icons_dir, "06.png"))
    self.icon6.addFile(os.path.join(self.icons_dir, "07.png"))
    self.icon7.addFile(os.path.join(self.icons_dir, "08.png"))

  def loadButtons(self):
    self.printer1Btn = QtGui.QPushButton()
    self.printer1Btn.setIcon(self.icon)
    self.printer1Btn.setIconSize(QtCore.QSize(100, 100))
    self.printer1Btn.setText("3D Printer\nFDM")
    self.connect(self.printer1Btn, QtCore.SIGNAL('clicked()'), lambda machine="printer1": self.doDecrease(machine))

    self.printer2Btn = QtGui.QPushButton()
    self.printer2Btn.setIcon(self.icon1)
    self.printer2Btn.setIconSize(QtCore.QSize(100, 100))
    self.printer2Btn.setText("3D Printer\nSTL")
    self.connect(self.printer2Btn, QtCore.SIGNAL('clicked()'), lambda machine="printer2": self.doDecrease(machine))

    self.printer3Btn = QtGui.QPushButton()
    self.printer3Btn.setIcon(self.icon2)
    self.printer3Btn.setIconSize(QtCore.QSize(100, 100))
    self.printer3Btn.setText("3D Printer Hi-Res\nSTL")
    self.connect(self.printer3Btn, QtCore.SIGNAL('clicked()'), lambda machine="printer3": self.doDecrease(machine))

    self.cncBtn = QtGui.QPushButton()
    self.cncBtn.setIcon(self.icon3)
    self.cncBtn.setIconSize(QtCore.QSize(100, 100))
    self.cncBtn.setText("Fresatrice CNC")
    self.connect(self.cncBtn, QtCore.SIGNAL('clicked()'), lambda machine="cnc": self.doDecrease(machine))

    self.festBtn = QtGui.QPushButton()
    self.festBtn.setIcon(self.icon4)
    self.festBtn.setIconSize(QtCore.QSize(100, 100))
    self.festBtn.setText("Sega ad\naffondamento")
    self.connect(self.festBtn, QtCore.SIGNAL('clicked()'), lambda machine="festool": self.doDecrease(machine))

    self.cutterBtn = QtGui.QPushButton()
    self.cutterBtn.setIcon(self.icon5)
    self.cutterBtn.setIconSize(QtCore.QSize(100, 100))
    self.cutterBtn.setText("Vinyl Cutter")
    self.connect(self.cutterBtn, QtCore.SIGNAL('clicked()'), lambda machine="cutter": self.doDecrease(machine))

    self.laserBtn = QtGui.QPushButton()
    self.laserBtn.setIcon(self.icon6)
    self.laserBtn.setIconSize(QtCore.QSize(100, 100))
    self.laserBtn.setText("Laser Cutter Pro")
    self.connect(self.laserBtn, QtCore.SIGNAL('clicked()'), lambda machine="laser": self.doDecrease(machine))

    self.materialsBtn = QtGui.QPushButton()
    self.materialsBtn.setIcon(self.icon7)
    self.materialsBtn.setIconSize(QtCore.QSize(100, 100))
    self.materialsBtn.setText("Materials")
    self.connect(self.materialsBtn, QtCore.SIGNAL('clicked()'), lambda machine="materials": self.doDecrease(machine))

    self.confirmBtn = QtGui.QPushButton('Confirm')
    self.connect(self.confirmBtn, QtCore.SIGNAL('clicked()'), self.confirm)

  def initUI(self):
    self.loadIcons()
    self.loadButtons()

    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    self.userLabel = QtGui.QLabel("Username")
    self.username = QtGui.QLabel()
    self.currBalanceLabel = QtGui.QLabel("Current Balance")
    self.currBalance = QtGui.QLabel()
    self.newBalanceLabel = QtGui.QLabel("New Balance")
    self.newBalance = QtGui.QLabel()

    # labels
    grid.addWidget(self.userLabel,0,0)
    grid.addWidget(self.username,0,1)
    grid.addWidget(self.currBalanceLabel,1,0)
    grid.addWidget(self.currBalance,1,1)
    grid.addWidget(self.newBalanceLabel,2,0)
    grid.addWidget(self.newBalance,2,1)

    # buttons
    grid.addWidget(self.printer1Btn,3,0)
    grid.addWidget(self.laserBtn,3,1)
    grid.addWidget(self.cutterBtn,4,0)
    grid.addWidget(self.cncBtn,4,1)
    grid.addWidget(self.printer2Btn,5,0)
    grid.addWidget(self.printer3Btn,5,1)
    grid.addWidget(self.festBtn,6,0)
    grid.addWidget(self.materialsBtn,6,1)
    grid.addWidget(self.confirmBtn,7,1)

    self.setLayout(grid)
    #self.resize(500, 460)
    center(self)
    self.setWindowTitle('opendot manager - Decrease dots')

  def readCard(self):
    QtGui.QMessageBox.question(self, 'Reading', 'Pass the card over the card reader')

    cId = rfid_reader.read_from_serial()

    cb = QtGui.QApplication.clipboard()
    cb.clear(mode=cb.Clipboard )
    cb.setText(cId, mode=cb.Clipboard)

    waitingCursor(main)
    try:
      user = connector.get_user(cId)
    except Exception, e:
      QtGui.QMessageBox.critical(self, 'Error', str(e))
      self.close()
      return
    finally:
      normalCursor(main)

    self.currUser = User(user)
    self.balance = self.currUser.getDots()
    self.username.setText(self.currUser.getUsername())
    self.currBalance.setText(str(self.currUser.getDots()))
    self.newBalance.setText(str(self.balance))
    self.exec_()


  def confirm(self):
    if (self.balance == float(self.currBalance.text())):
      self.close()
    elif (self.balance < 0):
      QtGui.QMessageBox.critical(self,  'opendot manager', "Insufficient dots, recharge needed!")
      self.close()
    else:
      reply = QtGui.QMessageBox.question(self, 'Confirmation', "New balance will be {} dots, confirm?".format(self.balance), QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
      if (reply == QtGui.QMessageBox.Yes):
        self.currUser.setDots(self.balance)
        waitingCursor(self)
        try:
          connector.update(self.currUser)
        except Exception, e:
          QtGui.QMessageBox.critical(self, 'Error', str(e))
          return
        finally:
          normalCursor(self)
      
        QtGui.QMessageBox.information(self, 'Success', 'New balance confirmed!')
        self.close()

  def doDecrease(self, machine):
    if (machine == "materials"):
      eur, ok = QtGui.QInputDialog.getText(self, 'Used material', 'Value of used materials (in euro):')

      if (ok and len(eur) > 0):
        try:
          dots = float(eur) * 1.25
        except Exception, e:
          QtGui.QMessageBox.critical(self, 'Error', "Valore non corretto")
          return
        self.balance -= dots
        self.newBalance.setText(str(self.balance))

    else:
      minutes, ok = QtGui.QInputDialog.getText(self, 'Usage time', 'Usage time (in minutes):')

      if ok:
        minutes = float(minutes)

        if (machine == "printer1"):
          if (minutes <= 60):
            self.balance -= minutes*0.25
          else:
            self.balance -= (15 + ((minutes-60) * 0.1))
        elif (machine == "printer2" or machine == "printer3"):
          self.balance -= (15 + minutes*0.25)
        elif (machine == "cnc" or machine == "laser" or machine == "festool" or machine == "cutter"):
          self.balance -= minutes # 1 dot/min

        self.newBalance.setText(str(self.balance))


def waitingCursor(window):
  window.setCursor(QtCore.Qt.WaitCursor)

def normalCursor(window):
  window.unsetCursor()

def center(window):
  qr = window.frameGeometry()
  cp = QtGui.QDesktopWidget().availableGeometry().center()
  qr.moveCenter(cp)
  window.move(qr.topLeft())
	
if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  app.setStyle("plastique")

  if sys.platform.startswith('win'):
    icon = QtGui.QIcon(os.path.dirname(os.path.abspath(sys.argv[0])) + "\icon.ico")
    sshFile = os.path.dirname(os.path.abspath(sys.argv[0])) + "\darkorange.stylesheet"
  elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    icon = QtGui.QIcon("icon.ico")
    sshFile = "darkorange.stylesheet"

  app.setWindowIcon(icon)

  with open(sshFile,"r") as fh:
    app.setStyleSheet(fh.read())
 
  rfid_reader = RFID()
  connector = DrupalConnector()
  main = MainWindow()
  login = LoginWindow(main)
  login.show()

  sys.exit(app.exec_())

