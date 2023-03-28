"""

This program is used to set up UI of the third window "recipes and restaurants recommendations"
Program reads generated file "restaurant_clean.csv" and "recipe_clean.csv"

"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
from PyQt5.QtWidgets import QLineEdit, QHeaderView, QAbstractScrollArea

import python_ui.UI_new as ui
import python_ui.recipe_match_instruction as rmi


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(60, 70, 1000, 1000))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 211, 232))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setLineWidth(1)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser_2.setEnabled(True)
        self.textBrowser_2.setMinimumSize(QtCore.QSize(0, 150))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout.addWidget(self.textBrowser_2)
        self.tableView = QtWidgets.QTableView(self.frame)
        self.tableView.setGeometry(QtCore.QRect(20, 280, 800, 192))
        self.tableView.setObjectName("tableView")
        self.tableView_2 = QtWidgets.QTableView(self.frame)
        self.tableView_2.setGeometry(QtCore.QRect(20, 500, 800, 200))
        self.tableView_2.setObjectName("tableView_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(320, 120, 81, 26))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(lambda: setResTable(self))
        self.pushButton.clicked.connect(lambda: setRecipeTable(self))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Recipes and Restaurants Recommendation"))
        self.label_2.setText(_translate("MainWindow", "Target Calorie"))
        self.label.setText(_translate("MainWindow", "Ingredients"))
        self.pushButton.setText(_translate("MainWindow", "Search"))

# restaurant table, uses function in UI_new through import UI_new as ui'
# restaurant data: 'clean_data.csv'
def setResTable(self):
    READ_PATH = "./python_ui/restaurant_clean.csv"
    data = pd.read_csv(READ_PATH, encoding='utf-8')
    data = ui.pre_process(data)
    test_input = str(self.textBrowser_2.toPlainText())
    result = ui.get_result(data, test_input)
    self.model = QStandardItemModel(10, 7)
    self.model.setHorizontalHeaderLabels(['Restaurant','Price','Star','Related Menu','Address','Open Time','Tag'])

    if len(result.index) > 0:
        for row in range(min(10, len(result.index))):
            item1 = QStandardItem(str(result['Restaurant'][row]))
            item2 = QStandardItem(str(result['Price'][row]))
            item3 = QStandardItem(str(result['Star'][row]))
            item4 = QStandardItem(str(result['Related Menu_x'][row]))
            item5 = QStandardItem(str(result['Address'][row]))
            item6 = QStandardItem(str(result['Open Time'][row]))
            item7 = QStandardItem(str(result['Tags'][row]))
            self.model.setItem(row, 0, item1)
            self.model.setItem(row, 1, item2)
            self.model.setItem(row, 2, item3)
            self.model.setItem(row, 3, item4)
            self.model.setItem(row, 4, item5)
            self.model.setItem(row, 5, item6)
            self.model.setItem(row, 6, item7)
            self.tableView_2.setModel(self.model)
            self.tableView_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    else:
        item = QStandardItem("no restaurant")
        self.model.setItem(0, 0, item)
        self.tableView_2.setModel(self.model)
        self.tableView_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


# recipe table, uses function in recipe_match_instruction.py through import recipe_match_instruction as rmi
def setRecipeTable(self):
    READ_PATH = "./python_ui/recipe_clean.csv"
    data = pd.read_csv(READ_PATH, encoding='utf-8')
    data = data.drop_duplicates()
    test_input = str(self.textBrowser_2.toPlainText())
    test_input = test_input.split(',')
    recipes = rmi.get_recipes(data, test_input)
    recipes = rmi.get_ingredients(data, recipes)

    self.model = QStandardItemModel(5, 4)
    self.model.setHorizontalHeaderLabels(['Recipe','Price','Ingredients','Instruction'])

    if len(recipes.index) > 0:
        recipe_list = list(set(recipes['recipe']))
        print(recipe_list)
        price_list = []
        ingredients_list = []
        instruction_list = []
        for recipe in recipe_list:
            temp_price = list(recipes.loc[recipes['recipe']==recipe,'price'])[0]
            temp_price = '{:8.2f}'.format(temp_price)
            print(temp_price)
            price_list.append(temp_price)
            temp_ingredient = list(recipes.loc[recipes['recipe']==recipe,'ingredient'])
            if len(temp_ingredient)>8:
                temp_ingredient = temp_ingredient[:9]
            string = ','
            temp_ingredient = string.join(temp_ingredient)
            ingredients_list.append(temp_ingredient)

            temp_instruction = list(recipes.loc[recipes['recipe'] == recipe, 'instruction'])[0]
            instruction_list.append(temp_instruction)

        for row in range(min(5, len(recipe_list))):
            item1 = QStandardItem(recipe_list[row])
            item2 = QStandardItem(price_list[row])
            item3 = QStandardItem(ingredients_list[row])
            item4 = QStandardItem(instruction_list[row])

            self.model.setItem(row, 0, item1)
            self.model.setItem(row, 1, item2)
            self.model.setItem(row, 2, item3)
            self.model.setItem(row, 3, item4)

            self.tableView.setModel(self.model)
            self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    else:
        item = QStandardItem("no recipe")
        self.model.setItem(0, 0, item)
        self.tableView.setModel(self.model)
        self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
