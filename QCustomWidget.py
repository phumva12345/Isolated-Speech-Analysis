from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

from Request import *

class QCustomWidget(QWidget):
    def __init__ (self, req, parent = None):
        super(QCustomWidget, self).__init__(parent)

        # Init attributes
        self.req = req
        self.textQVBoxLayout = QVBoxLayout()
        self.idLabel = QLabel()
        self.dateTimeLabel = QLabel()
        self.fileNameLabel = QLabel()
        self.allQHBoxLayout = QHBoxLayout()
        self.iconLabel = QLabel()

        # Set up
        self.textQVBoxLayout.addWidget(self.idLabel)
        self.textQVBoxLayout.addWidget(self.dateTimeLabel)
        # self.textQVBoxLayout.addWidget(self.fileNameLabel)
        self.allQHBoxLayout.addWidget(self.iconLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

        # Set default text
        self.setID("ID: " + self.req.getID())
        self.setDateTime(self.req.getDate() + " " +self.req.getTime())
        self.setFileName(self.req.getFileName())

        # setStyleSheet
        self.idLabel.setStyleSheet('''
            color: rgb(51, 102, 153);
        ''')
        self.dateTimeLabel.setStyleSheet('''
            color: rgb(153, 51, 255);
        ''')

    def setID(self, text):
        self.idLabel.setText(text)

    def setDateTime(self, text):
        self.dateTimeLabel.setText(text)

    def setFileName(self, text):
        self.fileNameLabel.setText(text)

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))
