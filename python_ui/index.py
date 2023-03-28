"""
By Chenxu Wang

This program is used to design first window UI


"""


import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QLabel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.man_count = 0
        self.woman_count = 0
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 730)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #image Background button
        self.Man = QPushButton(self.centralwidget)
        self.Man.setGeometry(QtCore.QRect(40, 40, 200, 330))
        self.Man.setStyleSheet("background-color: transparent;  border: 0px solid ; border-radius: 50;")
        self.Man.setObjectName("")
        self.Man.clicked.connect(self.on_click_Man)
        self.Man.setCheckable(True)
        self.Woman = QPushButton(self.centralwidget)
        self.Woman.setGeometry(QtCore.QRect(560, 35, 200, 340))
        self.Woman.setStyleSheet("background-color: transparent;  border: 0px solid ; border-radius: 50;")
        self.Woman.setObjectName("")
        self.Woman.clicked.connect(self.on_click_Woman)
        self.Woman.setCheckable(True)
        #image
        self.ManImage = QPushButton(self.centralwidget)
        self.ManImage.setGeometry(QtCore.QRect(55, 30, 200, 330))
        self.ManImage.setStyleSheet(
            "background-image: url(./python_ui/man_posture.png);border: 0px solid;")
        self.ManImage.setText("")
        self.ManImage.setObjectName("label")
        self.ManImage.clicked.connect(self.on_click_Man)
        self.WomanImage = QPushButton(self.centralwidget)
        self.WomanImage.setGeometry(QtCore.QRect(575, 30, 200, 340))
        self.WomanImage.setStyleSheet("background-image: url(./python_ui/woman_posture.png); border: 0px solid;")
        self.WomanImage.setText("")
        self.WomanImage.setObjectName("WomanImage")
        self.WomanImage.clicked.connect(self.on_click_Woman)
        #age
        self.Age = QLineEdit(self.centralwidget)
        self.Age.setGeometry(QtCore.QRect(345, 240, 191, 31))
        self.Age.setObjectName("Age")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(245, 240, 61, 31))
        self.label_3.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        #weight
        self.Weight = QLineEdit(self.centralwidget)
        self.Weight.setGeometry(QtCore.QRect(345, 290, 191, 31))
        self.Weight.setObjectName("Weight")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(245, 290, 81, 31))
        self.label_4.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_4.setObjectName("label_4")
        #height
        self.Height = QLineEdit(self.centralwidget)
        self.Height.setGeometry(QtCore.QRect(345, 340, 191, 31))
        self.Height.setObjectName("Height")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(245, 340, 81, 31))
        self.label_2.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        #Target
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(120, 390, 150, 31))
        self.label_5.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        self.Target = QComboBox(self.centralwidget)
        self.Target.setGeometry(QtCore.QRect(280, 390, 360, 31))
        self.Target.setObjectName("Target")
        self.Target.addItems(["sedentary (little or no exercise)",
                              "lightly active (light exercise/sports 1-3 days/week)",
                              "moderately active (moderate exercise/sports 3-5 days/week)",
                              "very active (hard exercise/sports 6-7 days a week)",
                              "extra active (very hard exercise/sports & physical job)"])
        #Result
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(80, 500, 361, 41))
        self.label_6.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_6.setObjectName("label_6")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(80, 560, 180, 50))
        self.label_7.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_7.setObjectName("label_7")
        self.Result = QLabel(self.centralwidget)
        self.Result.setGeometry(QtCore.QRect(250, 560, 180, 50))
        self.Result.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.Result.setObjectName("Result")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(80, 530, 180, 50))
        self.label_8.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_8.setObjectName("label_8")
        self.LResult = QLabel(self.centralwidget)
        self.LResult.setGeometry(QtCore.QRect(250, 530, 180, 50))
        self.LResult.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.LResult.setObjectName("Result Loss")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(80, 590, 180, 50))
        self.label_9.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.label_9.setObjectName("label_9")
        self.GResult = QLabel(self.centralwidget)
        self.GResult.setGeometry(QtCore.QRect(250, 590, 180, 50))
        self.GResult.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.GResult.setObjectName("Result Gain")

        #submit button
        self.Submit = QPushButton(self.centralwidget)
        self.Submit.setGeometry(QtCore.QRect(360, 450, 120, 40))
        self.Submit.setStyleSheet(
            "background-color: rgb(170, 170, 255);  border: 0px solid ; border-radius: 10; font: bold 16px;")
        self.Submit.setObjectName("Submit")
        self.Submit.clicked.connect(self.calculate_Calorie)

        self.Man.raise_()
        self.Woman.raise_()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Input Body Data"))
        self.Submit.setText(_translate("MainWindow", "Submit"))
        self.label_2.setText(_translate("MainWindow", "Height:"))
        self.label_3.setText(_translate("MainWindow", "Age:"))
        self.label_4.setText(_translate("MainWindow", "Weight:"))
        self.label_5.setText(_translate("MainWindow", "Activity Level:"))
        self.label_6.setText(_translate("MainWindow", "Your suggested daily calorie injection:"))
        self.label_7.setText(_translate("MainWindow", "Maintain Weight:"))
        self.label_8.setText(_translate("MainWindow", "Weight Loss:"))
        self.label_9.setText(_translate("MainWindow", "Weight Gain:"))

    def on_click_Man(self, Man):
        self.man_count +=1
        if self.man_count % 2 == 0:
            self.Man.setStyleSheet("QPushButton"
                                   "{"
                                   "background-color: transparent;  border: 0px solid ; border-radius: 50;"
                                   "}")
            self.Man.setChecked(False)
            self.Man.raise_()
        else:
            self.Man.setStyleSheet("QPushButton"
                                "{"
                                "background-color: rgb(170, 170, 255);  border: 0px solid ; border-radius: 50;"
                                "}")
            self.Man.setChecked(True)
            self.ManImage.raise_()

    def on_click_Woman(self):
        self.woman_count += 1
        if self.woman_count % 2 == 0:
            self.Woman.setStyleSheet("QPushButton"
                                   "{"
                                   "background-color: transparent;  border: 0px solid ; border-radius: 50;"
                                   "}")
            self.Woman.setChecked(False)
            self.Woman.raise_()
        else:
            self.Woman.setStyleSheet("QPushButton"
                               "{"
                               "background-color: rgb(190, 255, 150);  border: 0px solid ; border-radius: 50;"
                               "}")
            self.Woman.setChecked(True)
            self.WomanImage.raise_()

    def calculate_Calorie(self):
        _translate = QtCore.QCoreApplication.translate
        age = self.Age.text()
        weight = self.Weight.text()
        height = self.Height.text()
        try:
            age = float(age)
            weight = float(weight)
            height = float(height)
            if self.Man.isChecked():
                LBMR = 9.99*(weight-5)+6.25*height-4.92*age+5
                BMR = 9.99*weight+6.25*height-4.92*age+5
                GBMR = 9.99*(weight+5)+6.25*height-4.92*age+5
                if self.Target.currentIndex() == 0:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.2, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.2, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(GBMR*1.2, 2))+"kcal"))
                elif self.Target.currentIndex() == 1:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.375, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.375, 2))+"kcal"))
                    self.GResult.setText(_translate(
                        "MainWindow", str(round(GBMR*1.375, 2))+"kcal"))
                elif self.Target.currentIndex() == 2:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.55, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.55, 2))+"kcal"))
                    self.GResult.setText(_translate(
                        "MainWindow", str(round(GBMR*1.55, 2))+"kcal"))
                elif self.Target.currentIndex() == 3:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.725, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.725, 2))+"kcal"))
                    self.GResult.setText(_translate(
                        "MainWindow", str(round(GBMR*1.725, 2))+"kcal"))
                else:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.9, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.9, 2))+"kcal"))
                    self.GResult.setText(_translate(
                        "MainWindow", str(round(GBMR*1.9, 2))+"kcal"))
            elif self.Woman.isChecked():
                LBMR = 9.99*(weight-5)+6.25*height-4.92*age-161
                BMR = 9.99*weight+6.25*height-4.92*age-161
                GBMR = 9.99*(weight+5)+6.25*height-4.92*age-161
                if self.Target.currentIndex() == 0:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.2, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.2, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(GBMR*1.2, 2))+"kcal"))
                elif self.Target.currentIndex() == 1:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.375, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.375, 2))+"kcal"))
                    self.GResult.setText(_translate(
                        "MainWindow", str(round(GBMR*1.375, 2))+"kcal"))
                elif self.Target.currentIndex() == 2:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.55, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.55, 2))+"kcal"))
                    self.GResult.setText(_translate(
                        "MainWindow", str(round(GBMR*1.55, 2))+"kcal"))
                elif self.Target.currentIndex() == 3:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.725, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.725, 2))+"kcal"))
                    self.GResult.setText(_translate(
                        "MainWindow", str(round(GBMR*1.725, 2))+"kcal"))
                else:
                    self.LResult.setText(_translate(
                        "MainWindow", str(round(LBMR*1.9, 2))+"kcal"))
                    self.Result.setText(_translate(
                        "MainWindow", str(round(BMR*1.9, 2))+"kcal"))
                    self.GResult.setText(_translate(
                        "MainWindow", str(round(GBMR*1.9, 2))+"kcal"))
            else:
                print("Please select gender")
        except ValueError:
            print("Please enter number")


        



