from PyQt5 import QtCore, QtWidgets
from interface_ex1 import MainWindow as Ex1
from interface_ex2 import MainWindow as Ex2
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QMessageBox


app = QApplication([])
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.centralwidget.setStyleSheet("background-color: #DDDBDE;")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 430, 150, 50))
        self.pushButton.setStyleSheet("font-family: Arial; font-size: 15px; font-weight: bold;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 430, 150, 50))
        # self.pushButton_2.setStyleSheet("font-family: Arial; font-size: 15px; font-weight: bold;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(20, 390, 761, 2))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setStyleSheet("border: 1px solid black;")
        self.line_2.setObjectName("line_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 20, 600, 75))
        self.label.setStyleSheet("font-family: Arial; font-size: 40px; font-weight: bold; color: #0055AA;")
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(90, 90, 620, 2))
        self.line.setStyleSheet("border: 1px solid black;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setStyleSheet("border: 1px solid black;")
        self.line_2.setObjectName("line_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 110, 180, 40))
        self.label_2.setStyleSheet("font-family: Arial; font-size: 25px; color: #8AB6F9;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 150, 200, 50))
        self.label_3.setStyleSheet("font-family: Arial; font-size: 25px; font-weight: bold; color: #656E77;")
        self.label_3.setObjectName("label_3")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(520, 320, 200, 50))
        self.label_7.setStyleSheet("font-family: Arial; font-size: 25px; font-weight: bold; color: #656E77;")
        self.label_7.setObjectName("label_7")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setStyleSheet("font-family: Arial; font-size: 25px; font-weight: bold; color: #656E77;")        
        self.label_5.setGeometry(QtCore.QRect(310, 230, 200, 50))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(520, 150, 200, 50))
        self.label_4.setStyleSheet("font-family: Arial; font-size: 25px; font-weight: bold; color: #656E77;")
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setStyleSheet("font-family: Arial; font-size: 25px; font-weight: bold; color: #656E77;")
        self.label_6.setGeometry(QtCore.QRect(110, 320, 230, 50))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.open_exercice_1)
        self.pushButton_2.clicked.connect(self.open_exercice_2)

        #self.pushButton_6.clicked.connect(self.open_exercice_6)
    


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Exercice 1"))
        self.pushButton_2.setText(_translate("MainWindow", "Exercice 2"))

        self.label.setText(_translate("MainWindow", "Recherche Opérationnelle"))
        self.label_2.setText(_translate("MainWindow", "Made by:"))
        self.label_3.setText(_translate("MainWindow", "MEJDI Omar"))
        self.label_4.setText(_translate("MainWindow", "SILINI Ahmed"))
        
        self.label_6.setText(_translate("MainWindow", "CHERIF Ghassen"))
        self.label_7.setText(_translate("MainWindow", "BALTI Mohamed Aziz"))
    def open_exercice_1(self):
        
        self.exercice_1_window = Ex1()
        # self.exercice_1_window.setupUi(self.exercice_1_window)
        self.exercice_1_window.show()
        app.exec_()
    def open_exercice_2(self):


        self.exercice_2_window = Ex2()
        # self.exercice_2_window.setupUi(self.exercice_2_window)
        self.exercice_2_window.show()
        app.exec_()
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
