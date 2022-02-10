import sys
from configparser import ConfigParser
import database
import main

from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QLabel, QFormLayout, QComboBox, QPushButton
from PyQt5 import QtGui, QtCore, QtSvg


class App(QWidget):
    def __init__(self):
        super().__init__()
        file = 'config.ini'
        config = ConfigParser()
        config.read(file)

        self.setWindowTitle('Game Menu')
        self.setGeometry(450, 150, 300, 250)
        self.layout = QFormLayout(self)

        self.combousername = QComboBox()
        self.combousername.addItems([name[0] for name in database.get_usernames()])
        self.combodifficulty = QComboBox()
        self.combodifficulty.addItems(["Easy", "Medium", "Hard"])

        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        self.save_button = QPushButton("Save Config")
        self.save_button.clicked.connect(self.save_config)
        self.score_button = QPushButton("Show Highscore")
        self.score_button.clicked.connect(self.show_score)
        self.editcomport = QLineEdit()
        self.editcomport.setText(config["comport"]["port"])
        self.labeldifficulty = QLabel("Difficulty")
        self.labelusername = QLabel("Username")
        self.labelcomport = QLabel("Comport")
        self.labelhighscore = QLabel("Show Highscore")

        self.layout.addRow(self.labelusername, self.combousername)
        self.layout.addRow(self.labelcomport, self.editcomport)
        self.layout.addRow(self.labeldifficulty, self.combodifficulty)
        self.layout.addRow(self.labelhighscore, self.score_button)
        self.layout.addRow(self.save_button, self.start_button)

        self.option_button = QPushButton("Options")
        self.option_button.pressed.connect(self.show_options)

        self.layout.addWidget(self.option_button)


        self.show()

    def show_score(self):
        self.score_button.setText(str(database.get_highscore(self.combousername.currentText())))

    def start_game(self):
        main.run_game()

    def save_config(self):
        file = 'config.ini'
        config = ConfigParser()
        config.read(file)
        config.set("comport", "port", f"{self.editcomport.text()}")
        config.set("user", "name", f"{self.combousername.currentText()}")
        config.set("user", "highscore", f"{database.get_highscore(self.combousername.currentText())}")
        config.set("user", "difficulty", f"{self.combodifficulty.currentText()}")
        with open(file, "w") as configfile:
            config.write(configfile)

    def show_options(self):
        self.window = Options()
        #self.window.set_layout(self.label_name.text(), self.config)
        self.window.submitted.connect(self.transmit)
        self.window.show()

    def transmit(self, dict_string):
        self.alarm_dict.update(json.loads(dict_string))


class Options(QWidget):
    """
    AlarmOptions provides the additional window which gets
    opened, when the user wants to configure an alarm.
    When the Window opens, the User can pass in the
    parameters, which will be sent to the Main class
    with a pyqtSignal.
    """
    submitted = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        self.setGeometry(500, 400, 450, 150)
        self.setLayout(self.layout)
        self.alarm = None
        self.save_button = QPushButton("Save")
        self.cema_button = QPushButton("CEMA")
        self.layout_alarm = QFormLayout()
        self.image = QtSvg.QSvgWidget(self)


if __name__ == '__main__':
    # file = 'config.ini'
    # config = ConfigParser()
    # config.read(file)
    # print(config["comport"])
    # print(config.sections())
    # print(config["comport"]["port"])
    # config.set("comport", "port", "fffff")
    # print(config["comport"]["port"])
    #
    # with open (file, "w") as configfile:
    #    config.write(configfile)

    # editable.setCurrentIndex(val - 1)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
