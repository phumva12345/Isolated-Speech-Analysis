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

from PreProcessing import *


class ComparisonGraph(FigureCanvas):

    def __init__(self, signal_1, signal_2, type=1, parent=None, width=5, height=4, dpi=80):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.plot(signal_1, signal_2)

    def plot(self, signal_1, signal_2):
        ax = self.figure.add_subplot(111)
        ax.plot(signal_1, label="Original")
        ax.plot(signal_2, label="Segmented")
        ax.set_title('Original / Segmented Signals')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Amplitude')
        ax.legend()
        self.draw()

    def close(self):
        self.axes.clear()
