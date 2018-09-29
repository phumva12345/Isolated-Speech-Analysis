from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

import numpy as np
import wave

class Graph(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=80, file_name=''):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.file_name = file_name

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        rate, signal = wavfile.read(self.file_name)
        ax = self.figure.add_subplot(111)
        ax.plot(signal)
        ax.set_title('Audio signal')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Amplitude')
        # props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        # ax.text(0.88, 0.9, "x = Sample\ny = Amplitude", transform=ax.transAxes, fontsize=14,\
        #     verticalalignment='top', bbox=props)

        self.draw()
