from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile

import numpy as np
import wave
from python_speech_features import mfcc

class MFCCs(FigureCanvas):

    def __init__(self, signal, sample_rate, parent=None, width=5, height=4, dpi=80, file_name=''):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.file_name = file_name

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(signal, sample_rate)

    def plot(self, sig, sample_rate):
        try:
            mfcc_feat = mfcc(sig, sample_rate, nfft=2048)
            mfcc_data = np.swapaxes(mfcc_feat, 0 ,1)

            fig, ax = plt.subplots()
            ax = self.figure.add_subplot(111)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
            im = ax.imshow(mfcc_data, interpolation='nearest', origin='lower', aspect='auto')
            ax.set_title('MFCCs')
            ax.set_ylabel('MFCC Coefficients')
            ax.set_xlabel('Time [sec*10^-2]')
            fig.colorbar(im, cax=cax)
        except IndexError as err:
            print(err)

        self.draw()

    def close(self):
        self.axes.clear()
