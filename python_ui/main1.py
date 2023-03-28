"""
By Ruidi Chang and Simon

This program is used to design the first window's UI furthermore
and pass input text to later windows

Also the program designed to check if the input ingredients could
cause possible illness or allergy

"""

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
import PyQt5.QtWidgets as QtWidgets
import python_ui.index as index


class AppWindow(QMainWindow, index.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow,self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.firstwindow = MyWindow()
        #self.firstwindow.dispayInfo()
        # click Loss, Maintain and Gain buttons to pass data
        self.btn1.clicked.connect(lambda: self.passData1())
        self.btn2.clicked.connect(lambda: self.passData2())
        self.btn3.clicked.connect(lambda: self.passData3())

    # add three button
    def initUI(self):
        self.btn1 = QPushButton("Loss", self)
        self.btn1.move(500, 537)
        self.btn2 = QPushButton("Maintain", self)
        self.btn2.move(500, 567)
        self.btn3 = QPushButton("Gain", self)
        self.btn3.move(500, 597)
    
    # pass calories data to the next page
    def passData1(self):
        self.firstwindow.textBrowser_a.setText(self.LResult.text())
        print(self.LResult.text())
        self.firstwindow.dispayInfo()
        
    def passData2(self):
        self.firstwindow.textBrowser_a.setText(self.Result.text())
        print(self.Result.text())
        self.firstwindow.dispayInfo()
        
    def passData3(self):
        self.firstwindow.textBrowser_a.setText(self.GResult.text())
        print(self.GResult.text())
        self.firstwindow.dispayInfo()
    
import python_ui.nutrition_api as nutrition_api
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
import requests
import pandas as pd

header = {'x-app-id': '564584ad', 'x-app-key': '596ecbf4294f77e67bc3fff38c4b4465', 'x-remote-user-id': '0'}
url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'


class MyWindow(QMainWindow, nutrition_api.Ui_MainWindow):
    food_list = []
    conflict_list = []

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        df = pd.read_csv('./python_ui/FoodDataFinalClean.csv')
        self.conflict_list = df['food_conflicts'].str.lower().str.split(", ")
        # print(self.conflict_list)
        self.searchButton.clicked.connect(lambda: self.search_api())
        self.initUI()
        self.secondwindow = MyWindow2()
        self.btn.clicked.connect(lambda: self.passData())

  
    def initUI(self):
        self.btn = QPushButton("Continue", self)
        self.btn.move(700, 500)
        self.textBrowser_a = QtWidgets.QTextEdit(self.layoutWidget)
        self.textBrowser_a.setObjectName("textBrower_a")
        self.horizontalLayout_2.addWidget(self.textBrowser_a)

    # Send post request to the Nutrition API with user inputted food list
    # as well as required header in order to retrieve total calories
    def search_api(self):
        self.food_list = []
        query = {'query': self.searchBox.toPlainText()}
        result = requests.post(url=url, headers=header, data=query)
        if 'couldn\'t match any' not in result.text:
            result = result.json()['foods']
            total_calories = 0
            for food in result:
                self.food_list.append(food['food_name'].lower())
                total_calories += food['nf_calories']
            self.resultBox.setText(str(total_calories))
            print(self.food_list)
            self.load_food_conflict()
    
    # Compare the food conflict data with the user inputted food list
    # to see if there is any combination of foods that can cause
    # illness
    def load_food_conflict(self):

        # print(conflict_list)
        conflict_result = set()
        for l in self.conflict_list:

            if len(l) == 1:
                continue
            # print(l)
            count = 0
            temp_result = set()
            for food in self.food_list:
                if food in l:
                    count += 1
                    temp_result.add(food)
            # print(count)
            if float(count) / len(l) > 0.7:
                # print(l)
                conflict_result = conflict_result.union(temp_result)
        # print(conflict_result)
        message = ''
        if len(conflict_result) != 0:
            message = ', '.join(conflict_result)
            message = 'Warning: ' + str(message) + ' together could cause serious illness!!!!'

        allergy_list = self.find_allergy_sources()
        if len(allergy_list) != 0:
            message += '\nAllergy warning: ' + str(', '.join(allergy_list)) + ' might cause allergy!'
        self.warningMsg.setText(message)

    # Compare possible allergy sources with the user inputtd food list to see
    # if there is any food that can cause allergy
    def find_allergy_sources(self):
        allergy_list = []
        for l in self.conflict_list:
            if len(l) == 1:
                if l[0] in self.food_list:
                    allergy_list.append(l[0])
        return allergy_list

    # pass calories and ingredient data to the next page
    def passData(self):
        tftb = ",".join(self.food_list)
        self.secondwindow.textBrowser_2.setText(tftb)
        rci=str(self.textBrowser_a.toPlainText()).replace('\n', ',')
        self.secondwindow.textBrowser.setText(rci)
        self.secondwindow.dispayInfo()
    
    def dispayInfo(self):
        self.show()


from python_ui.python_ui import *
#from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
#import python_ui


class MyWindow2(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWindow2, self).__init__(parent)
        self.setupUi(self)

    def dispayInfo(self):
        self.show()
        

def runUI():
    app = QApplication(sys.argv)
    a = AppWindow()
    b = MyWindow()
    c = MyWindow2()
    a.show()
    # a.btn1.clicked.connect(b.show)
    sys.exit(app.exec_())

if __name__ == '__main__':
    runUI()