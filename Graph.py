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


class Graph(FigureCanvas):

    def __init__(self, signal, type=1, header=False, parent=None, width=5, height=4, dpi=80):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.header = header

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.plot(signal, type)

    def plot(self, signal, typ):
        ax = self.figure.add_subplot(111)
        ax.plot(signal)
        if self.header:
            ax.set_title('Original Signal')
        if typ == 1:
            ax.set_xlabel('Sample')
            ax.set_ylabel('Amplitude')
        elif typ == 2:
            ax.set_xlabel('Window Indexes')
            ax.set_ylabel('SD')
        elif typ == 3:
            ax.set_xlabel('Window Indexes')
            ax.set_ylabel('Speech / Non-Speech')
        self.draw()

    def close(self):
        self.axes.clear()
