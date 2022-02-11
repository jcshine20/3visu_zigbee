import sys
from configparser import ConfigParser
import database
# import main
import subprocess
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QLabel, QFormLayout, QComboBox, QPushButton, \
    QGridLayout
from PyQt5 import QtGui, QtCore, QtSvg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from visualization import main


class App(QWidget):
    def __init__(self):
        super().__init__()

        myFont = QtGui.QFont()
        myFont.setBold(True)
        #self.label.setFont(myFont)

        self.file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.file)

        self.setWindowTitle('Game Menu')
        self.setGeometry(450, 150, 300, 250)
        self.layout = QFormLayout(self)

        self.combousername = QComboBox()
        self.combousername.addItems([name[0] for name in database.get_usernames()])
        self.combodifficulty = QComboBox()
        self.combodifficulty.addItems(["easy", "medium", "hard", "very_hard"])
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        #self.start_button.setStyleSheet("border: 1px solid; border-color:red; background-color:white")

        self.save_button = QPushButton("Save Config")
        self.save_button.clicked.connect(self.save_config)
        self.score_button = QPushButton("Show Highscore")
        self.score_button.clicked.connect(self.show_score)
        self.visu_button = QPushButton("Show visu")
        self.visu_button.pressed.connect(self.show_visu)
        self.option_button = QPushButton()
        self.option_button.pressed.connect(self.show_options)
        self.option_button.setIcon(QIcon("icons\\options.png"))
        self.option_button.setGeometry(200, 150, 100, 30)

        self.label_options = QLabel("Options")
        self.label_options.setStyleSheet("background-color: red")
        self.label_options.setFont(myFont)
        self.label_difficulty = QLabel("Difficulty")
        self.label_difficulty.setStyleSheet("background-color: red")
        self.label_difficulty.setFont(myFont)
        self.label_options.setFont(myFont)
        self.label_username = QLabel("Username")
        self.label_username.setStyleSheet("background-color: red")
        self.label_username.setFont(myFont)
        self.label_highscore = QLabel("Show Highscore")
        self.label_highscore.setStyleSheet("background-color: red")
        self.label_highscore.setFont(myFont)
        self.label_visu = QLabel("Visu anzeigen")
        self.label_visu.setStyleSheet("background-color: red")
        self.label_visu.setFont(myFont)

        self.layout.addRow(self.label_options, self.option_button)
        self.layout.addRow(self.label_username, self.combousername)
        self.layout.addRow(self.label_difficulty, self.combodifficulty)
        self.layout.addRow(self.label_highscore, self.score_button)
        self.layout.addRow(self.label_visu, self.visu_button)
        self.layout.addRow(self.save_button, self.start_button)

        self.show()

    def show_score(self):
        self.score_button.setText(str(database.get_highscore(self.combousername.currentText())))

    def start_game(self):
        self.close()
        subprocess.call("python main.py", shell=True)

    def save_config(self):
        self.config.set("user", "name", f"{self.combousername.currentText()}")
        self.config.set("user", "highscore", f"{database.get_highscore(self.combousername.currentText())}")
        self.config.set("user", "difficulty", f"{self.combodifficulty.currentText()}")
        with open(self.file, "w") as configfile:
            self.config.write(configfile)

    def show_options(self):
        self.window = Options()
        self.window.submitted.connect(self.transmit)
        self.window.show()

    def show_visu(self):
        main()

    def transmit(self, names):
        if names != "":
            self.combousername.addItems(name for name in names.split(","))


class Options(QWidget):
    """
    Options provides the additional window which gets
    opened, when the user wants to configure the game.
    When the Window opens, the User can pass in the
    parameters, which will be sent to the Main window
    with a pyqtSignal.
    """
    submitted = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.new_names = []
        self.file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.file)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.button_name = QPushButton("Save name")
        self.button_save = QPushButton("Save Comport and close")
        self.edit_comport = QLineEdit()
        self.edit_comport.setText(self.config["comport"]["port"])
        self.edit_username = QLineEdit()
        self.label_comport = QLabel("Comport")
        self.label_username = QLabel("Enter new name")

        self.layout.addWidget(self.label_comport, self.layout.rowCount() - 1, self.layout.columnCount())
        self.layout.addWidget(self.edit_comport, self.layout.rowCount() - 1, self.layout.columnCount())
        self.layout.addWidget(self.label_username, self.layout.rowCount(), self.layout.columnCount() - 2)
        self.layout.addWidget(self.edit_username, self.layout.rowCount() - 1, self.layout.columnCount() - 1)

        self.layout.addWidget(self.button_save, self.layout.rowCount(), self.layout.columnCount() - 1)
        self.layout.addWidget(self.button_name, self.layout.rowCount() - 1, self.layout.columnCount() - 2)

        self.button_name.pressed.connect(self.save_name)
        self.button_save.pressed.connect(self.save_comport)

    def save_name(self):
        database.insert_user(str(self.edit_username.text()))
        self.new_names.append(str(self.edit_username.text()))

    def save_comport(self):
        self.config.set("comport", "port", f"{self.edit_comport.text()}")
        with open(self.file, "w") as configfile:
            self.config.write(configfile)
        self.submitted.emit(",".join(self.new_names))
        self.close()

    def closeEvent(self, event):
        # In case the user doesn't use the designated button to close the form
        self.submitted.emit(",".join(self.new_names))
        self.close()


if __name__ == '__main__':
    qp = QPalette()
    qp.setColor(QPalette.Window, Qt.black)
    app = QApplication(sys.argv)
    app.setStyleSheet("QLineEdit { background-color: yellow }")
    app.setStyleSheet("QLabel{font-size: 14pt;}")
    app.setStyleSheet("QLabel{background-color: red;}")
    myFont = QtGui.QFont()
    myFont.setBold(True)
    app.setFont(myFont)

    app.setPalette(qp)
    ex = App()
    sys.exit(app.exec_())

