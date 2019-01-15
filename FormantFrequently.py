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
from FeatureExtraction import *
import matplotlib.patches as mpatches

import numpy as np
import wave

class FormantFrequently(FigureCanvas):

    def __init__(self, signal, sample_rate, formant_n=None, parent=None, width=5, height=4, dpi=80, file_name=''):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.file_name = file_name

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(signal, sample_rate, formant_n)

    def plot(self, sig, sample_rate, formant_n):
        try:
            frequencies, times, spectrogram = signal.spectrogram(sig, sample_rate)
            fig, ax = plt.subplots()
            ax = self.figure.add_subplot(111)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
            im = ax.pcolormesh(times, frequencies, np.log(spectrogram))
            if formant_n is None:
                ax.pcolormesh(times, frequencies, FeatureExtraction().formant_frequently(np.log(spectrogram), 0), cmap=plt.cm.Greys_r)
                ax.pcolormesh(times, frequencies, FeatureExtraction().formant_frequently(np.log(spectrogram), 1), cmap=plt.cm.winter)
                ax.pcolormesh(times, frequencies, FeatureExtraction().formant_frequently(np.log(spectrogram), 2), cmap=plt.cm.cool)
                ax.pcolormesh(times, frequencies, FeatureExtraction().formant_frequently(np.log(spectrogram), 3), cmap=plt.cm.Greens_r)
                ax.pcolormesh(times, frequencies, FeatureExtraction().formant_frequently(np.log(spectrogram), 4), cmap=plt.cm.summer)
                ax.pcolormesh(times, frequencies, FeatureExtraction().formant_frequently(np.log(spectrogram), 5), cmap=plt.cm.Reds_r)
            else:
                ax.pcolormesh(times, frequencies, FeatureExtraction().formant_frequently(np.log(spectrogram), formant_n), cmap=plt.cm.Reds_r)
            ax.set_title('Formant Frequently')
            ax.set_ylabel('Frequency [Hz]')
            ax.set_xlabel('Time [sec]')
            if formant_n is None:
                purple_patch = mpatches.Patch(color='black', label='F0')
                blue_patch = mpatches.Patch(color='blue', label='F1')
                aqua_patch = mpatches.Patch(color='aqua', label='F2')
                green_patch = mpatches.Patch(color='green', label='F3')
                lightseagreen_patch = mpatches.Patch(color='lightseagreen', label='F4')
                red_patch = mpatches.Patch(color='darkred', label='F5')
                ax.legend(handles=[purple_patch, blue_patch, aqua_patch, green_patch, lightseagreen_patch, red_patch])
            fig.colorbar(im, cax=cax)
        except ValueError as err:
            print(err)

        self.draw()

    def close(self):
        self.axes.clear()
