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


class Spectrogram(FigureCanvas):

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

    # def plot(self):
    #     sample_rate, samples = wavfile.read(self.file_name)
    #     frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    #     ax = self.figure.add_subplot(111)
    #     ax.pcolormesh(times, frequencies, spectrogram)
    #     ax.set_title('Spectrogram')
    #     ax.set_ylabel('Frequency [Hz]')
    #     ax.set_xlabel('Time [sec]')
    #     # props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    #     # ax.text(0.82, 0.9, "x = Frequency [Hz]\ny = Time [sec]", transform=ax.transAxes, fontsize=14,\
    #     #     verticalalignment='top', bbox=props)

    #     self.draw()

    def plot(self, sig, sample_rate):
        try:
            frequencies, times, spectrogram = signal.spectrogram(sig, sample_rate)
            fig, ax = plt.subplots()
            ax = self.figure.add_subplot(111)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
            im = ax.pcolormesh(times, frequencies, np.log(spectrogram))
            fig.colorbar(im, cax=cax)
            ax.set_title('Spectrogram')
            ax.set_ylabel('Frequency [Hz]')
            ax.set_xlabel('Time [sec]')
        except ValueError as err:
            print(err)


        self.draw()

    def close(self):
        self.axes.clear()
