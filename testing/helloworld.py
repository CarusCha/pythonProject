# import sys
# from PyQt5.QtWidgets import QApplication, QPushButton, QToolTip, QMainWindow, QAction, qApp, QDesktopWidget, QLabel, QVBoxLayout, QWidget
# from PyQt5.QtCore import QCoreApplication, QDate, Qt
# from PyQt5.QtGui import *
#
# class HelloWorld(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.date = QDate.currentDate()
#         self.initUI()
#
#
#     def initUI(self):
#
#
#         # Title
#         self.setWindowTitle('Hello World')
#
#         # Status bar
#         self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))
#
#         # Exit action
#         exitAction = QAction(QIcon(), 'Exit', self)
#         exitAction.setShortcut('Ctrl+W')
#         exitAction.setStatusTip('Exit application')
#         exitAction.triggered.connect(qApp.quit)
#
#         # Tool bar
#         # self.toolbar = self.addToolBar('Exit')
#         # self.toolbar.addAction(exitAction)
#
#         # Menu bar
#         menubar = self.menuBar()
#         menubar.setNativeMenuBar(False)
#         filemenu = menubar.addMenu('&File')
#         filemenu.addAction(exitAction)
#
#         # Tool tip
#         QToolTip.setFont(QFont('', 10))
#         self.setToolTip('This is a <b>QWidget</b> widget')
#
#         # Button
#         btn = QPushButton('Quit', self)
#         btn.move(200, 50)
#         btn.setToolTip('This is a <b>QPushButton</b> widget')
#         btn.resize(btn.sizeHint())
#         btn.clicked.connect(QCoreApplication.instance().quit)
#
#         # Icon
#         # self.setWindowIcon(QIcon('tuck.png'))
#
#
#
#
#
#         # Show window
#         self.setGeometry(300, 300, 300, 200)
#         self.center()
#         self.show()
#
#         # Style
#         lbl_red = QLabel('Red')
#         lbl_green = QLabel('Green')
#         lbl_blue = QLabel('Blue')
#
#         lbl_red.setStyleSheet("color: red;"
#                               "border-style: solid;"
#                               "border-width: 2px;"
#                               "border-color: #FA8072;"
#                               "border-radius: 3px")
#         lbl_green.setStyleSheet("color: green;"
#                                 "background-color: #7FFFD4")
#         lbl_blue.setStyleSheet("color: blue;"
#                                "background-color: #87CEFA;"
#                                "border-style: dashed;"
#                                "border-width: 3px;"
#                                "border-color: #1E90FF")
#
#         vbox = QVBoxLayout()
#         vbox.addWidget(lbl_red)
#         vbox.addWidget(lbl_green)
#         vbox.addWidget(lbl_blue)
#
#
#
#         testWidget = QWidget()
#         testWidget.setGeometry(100, 100, 100, 100)
#         testWidget.show()
#
#         testWidget.setLayout(vbox)
#
#
#
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = HelloWorld()
#     sys.exit(app.exec_())


import datetime

today = datetime.datetime.today() + datetime.timedelta(days=8)
print(today)
dayOfWeek = today.weekday()
if dayOfWeek > 4:
    tt = dayOfWeek - 4
    today += datetime.timedelta(days=-tt)

print(today)


today = datetime.datetime.today()
dayOfWeek = today.weekday()
if dayOfWeek > 4:
    overDay = dayOfWeek - 4
    today += datetime.timedelta(days=-overDay)

