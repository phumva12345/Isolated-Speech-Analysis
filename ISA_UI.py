import sys
import wave
import os

from Graph import *
from Spectrogram import *
from Request import *
from QCustomWidget import *
from scipy.io import wavfile as wav
from MySignal import *

class ISA_UI(QMainWindow):

    def __init__(self, parent = None):
        # Init attributes
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(1280, 720)

        # Init signal
        self.signal = MySignal()
        self.signal.sigStr.connect(self.update_request)

        # Set up main UI
        self.parent = parent
        self.setWindowTitle("ISA System")

        # Set up form
        loader = QUiLoader()
        form = loader.load("ISA_UI.ui")
        self.setCentralWidget(form)

        # Add icon
        # self.icon_label = form.findChild(QFrame, "icon_frame")
        # self.icon_label.setStyleSheet("QFrame{border-image:url("+"pics/icon.png"+")};")

        # Add title
        self.icon_label = form.findChild(QTextEdit, "textEdit_2")
        self.icon_label.setText("\tProcessed Requests")
        self.icon_label.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }")
        self.icon_label.setReadOnly(True)

        # Set up graph layouts
        self.layout_1 = form.findChild(QVBoxLayout,"layout_1")
        self.layout_2 = form.findChild(QVBoxLayout,"layout_2")

        # Set up list widget
        self.myQListWidget = form.findChild(QListWidget,"listWidget")
        self.myQListWidget.itemClicked.connect(self.clicked)

        # Set up text edit
        self.textEdit = form.findChild(QTextEdit,"textEdit")
        self.textEdit.setReadOnly(True)

        self.update_request('sample_16_8000.wav')
        self.update_request('sample_16_11025.wav')
        self.update_request('sample_16_22050.wav')
        self.update_request('sample_16_44100.wav')

    def clicked(self, item):
        row = item.listWidget().row(item)
        req = item.listWidget().itemWidget(item.listWidget().item(row)).req
        self.update_text_edit(req)
        self.update_graph_layout(req)

    def reset_layout(self):
        self.layout_1.takeAt(0)
        self.layout_2.takeAt(0)

    def generate_icon(self, req):
        rate, data = wav.read(req.getFileName())

        plt.plot(data)
        plt.axis('off')
        figure = plt.gcf()

        figure.set_size_inches(2, 0.48)
        plt.savefig(req.getFileName() + ".png", dpi = 100, transparent=True)
        plt.clf()

    def update_text_edit(self, req):
        text = ""
        spf = wave.open(req.getFileName(),'r')

        text += "<b>Channel:\t\t</b>"
        if spf.getnchannels() == 1:
            text += "Mono"
        else:
            text += "Stereo"
        text += "<br/><br/><b>Sampling rate:</b>  " + str(spf.getframerate()) + " Hz"
        text += "<br/><br/><b>Frame:</b>  " + str(spf.getnframes())
        text += "<br/><br/><b>Sample width:</b>  " + str(spf.getsampwidth()) + " bytes"
        text += "<br/><br/><b>Compression type:</b>  " + str(spf.getcomptype())

        self.textEdit.setText(text)

    def update_list_widget(self, req):
        myQCustomQWidget = QCustomWidget(req)

        # Set up an icon
        self.generate_icon(req)
        myQCustomQWidget.setIcon(req.getFileName() + ".png")

        myQListWidgetItem = QListWidgetItem(self.myQListWidget)
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

        # Add QListWidgetItem into QListWidget
        # self.myQListWidget.addItem(myQListWidgetItem)
        self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

        # Update to the newest row
        self.myQListWidget.setCurrentRow(int(req.id) - 1)

        os.remove(req.getFileName() + ".png")

    def update_graph_layout(self, req):
        self.reset_layout()

        original_graph = Graph(self, width=7, height=2, file_name = req.getFileName())
        spectrogram_graph = Spectrogram(self, width=7, height=2, file_name = req.getFileName())

        self.layout_1.addWidget(original_graph)
        self.layout_2.addWidget(spectrogram_graph)

    def update_request(self, file_name):
        req = Request(file_name)
        self.update_text_edit(req)
        self.update_list_widget(req)
        self.update_graph_layout(req)

def main():
    app = QApplication(sys.argv)
    w = ISA_UI()
    w.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
