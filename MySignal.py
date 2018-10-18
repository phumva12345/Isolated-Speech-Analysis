from PySide2.QtCore import *
from PyQt5.QtCore import *

class MySignal(QObject):
    sigStr = pyqtSignal(str)
