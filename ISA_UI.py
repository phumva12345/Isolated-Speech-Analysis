import sys
import wave
import os

from PySide2 import QtWidgets, QtMultimedia
from Graph import *
from Spectrogram import *
from Request import *
from QCustomWidget import *
from server import *
from scipy.io import wavfile as wav
from MySignal import *
from PreProcessing import *
from MFCCs import *
from FormantFrequently import *
from ComparisonGraph import *
from ProcessedSignal import *

class ISA_UI(QMainWindow):
    
    def __init__(self, parent = None):
        # Init attributes
        QMainWindow.__init__(self, None)
        self.setMinimumSize(1600, 900)
        self.setMaximumSize(1600, 900)

        self.current_req = 0
        self.signals = {}
        self.current_opening_graphs = None

        # Init signal
        self.signal = MySignal()
        self.signal.sigStr.connect(self.update_request)

        # Set up main UI
        self.parent = parent
        self.setWindowTitle("ISA System")

        # Set up form
        loader = QUiLoader()
        form = loader.load("newISA_UI.ui")
        self.setCentralWidget(form)

        # Add icon
        # self.icon_label = form.findChild(QFrame, "icon_frame")
        # self.icon_label.setStyleSheet("QFrame{border-image:url("+"pics/icon.png"+")};")

        # Add title
        self.icon_label = form.findChild(QTextEdit, "textEdit_2")
        self.icon_label.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }")
        self.icon_label.setReadOnly(True)

        # Pre-Processing title
        self.icon_label = form.findChild(QTextEdit, "textEdit_3")
        self.icon_label.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }")
        self.icon_label.setReadOnly(True)

         # Feature Extraction title
        self.icon_label = form.findChild(QTextEdit, "textEdit_4")
        self.icon_label.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }")
        self.icon_label.setReadOnly(True)

        # Connect buttons
        self.play_button = form.findChild(QPushButton,"play_button")
        self.process_button = form.findChild(QPushButton,"process_button")
        self.play_button.clicked.connect(self.play)
        self.process_button.clicked.connect(self.process)

        # Connect spin box
        self.spin_box = form.findChild(QDoubleSpinBox,"spin_box")

        # Set up graph layouts
        self.original_layout = form.findChild(QVBoxLayout,"original")
        self.compare_layout = form.findChild(QVBoxLayout,"compare")

        self.zero_layout = form.findChild(QVBoxLayout,"zero")
        self.normal_layout = form.findChild(QVBoxLayout,"normal")
        self.fixed_layout = form.findChild(QVBoxLayout,"fixed")
        self.power_layout = form.findChild(QVBoxLayout,"power")
        self.window_layout = form.findChild(QVBoxLayout,"window")
        self.segmented_layout = form.findChild(QVBoxLayout,"segmented")
        self.remove_layout = form.findChild(QVBoxLayout,"remove")
        self.recon_layout = form.findChild(QVBoxLayout,"recon")

        self.spec_layout = form.findChild(QVBoxLayout,"spec")
        self.mfcc_layout = form.findChild(QVBoxLayout,"mfcc")
        self.formant_layout = form.findChild(QVBoxLayout,"formant")
        self.f0_layout = form.findChild(QVBoxLayout,"f0")
        self.f1_layout = form.findChild(QVBoxLayout,"f1")
        self.f2_layout = form.findChild(QVBoxLayout,"f2")
        self.f3_layout = form.findChild(QVBoxLayout,"f3")
        self.f4_layout = form.findChild(QVBoxLayout,"f4")
        self.f5_layout = form.findChild(QVBoxLayout,"f5")

        # Set up list widget
        self.myQListWidget = form.findChild(QListWidget,"listWidget")
        self.myQListWidget.itemClicked.connect(self.clicked)

        # Set up text edit
        self.textEdit = form.findChild(QTextEdit,"textEdit")
        self.textEdit.setReadOnly(True)

        self.update_request('robot-1.wav, robot')
        self.update_request('robot-2.wav, robot')
        self.update_request('robot-3.wav, robot')
        self.update_request('robot-4.wav, robot')
        # self.update_request('isw_2M_jealous.wav, jealous')
        # self.update_request('isw_2M_mushroom.wav, mushroom')
        # self.update_request('isw_2M_palace.wav, palace')
        # self.update_request('isw_2M_spider.wav, spider')
        # self.update_request('isw_2M_zipper.wav, zipper')

    def play(self):
        QtMultimedia.QSound.play(self.current_req.getFileName())

    def process(self):
        self.process_request(self.current_req, threshold=self.spin_box.value())
        self.update_graph_layout(self.current_req)

    def clicked(self, item):
        row = item.listWidget().row(item)
        req = item.listWidget().itemWidget(item.listWidget().item(row)).req
        self.current_req = req
        self.update_text_edit(req)
        self.update_graph_layout(req)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def close_graphs(self):
        plt.close('all')

    def reset_layout(self):
        self.clear_layout(self.original_layout)
        self.clear_layout(self.compare_layout)
        self.clear_layout(self.zero_layout)
        self.clear_layout(self.normal_layout)
        self.clear_layout(self.fixed_layout)
        self.clear_layout(self.power_layout)
        self.clear_layout(self.window_layout)
        self.clear_layout(self.segmented_layout)
        self.clear_layout(self.remove_layout)
        self.clear_layout(self.recon_layout)
        self.clear_layout(self.spec_layout)
        self.clear_layout(self.mfcc_layout)
        self.clear_layout(self.formant_layout)
        self.clear_layout(self.f0_layout)
        self.clear_layout(self.f1_layout)
        self.clear_layout(self.f2_layout)
        self.clear_layout(self.f3_layout)
        self.clear_layout(self.f4_layout)
        self.clear_layout(self.f5_layout)

    def generate_icon(self, req):
        rate, data = wav.read(req.getFileName())

        plt.plot(data)
        plt.axis('off')
        figure = plt.gcf()

        figure.set_size_inches(1.5, 0.48)
        plt.savefig(req.getFileName() + ".png", dpi = 100, transparent=True)
        plt.clf()

    def update_text_edit(self, req):
        text = ""
        spf = wave.open(req.getFileName(),'r')

        text += "<b>Word:</b>  " + req.getWord()
        text += "<br/><br/><b>Channel:\t\t</b>"
        if spf.getnchannels() == 1:
            text += "Mono"
        else:
            text += "Stereo"

        text += "<br/><br/><b>Sampling rate:</b>  " + str(spf.getframerate()) + " Hz"
        text += "<br/><br/><b>Sample:</b>  " + str(spf.getnframes()) + " sample(s)"
        text += "<br/><br/><b>Time Duration:</b>  " + str("{0:.2f} second(s)".format(spf.getnframes() / spf.getframerate()))
        text += "<br/><br/><b>Sample width:</b>  " + str(spf.getsampwidth()) + " byte(s)"
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
        self.close_graphs()
        signals = self.request_to_graph(self.signals[req.getID()])

        original_graph = signals[0]
        zero_graph = signals[1]
        normal_graph = signals[2]
        fixed_graph = signals[3]
        power_graph = signals[4]
        window_graph = signals[5]
        segmented_graph = signals[6]
        remove_graph = signals[7]
        recon_graph = signals[8]
        spec_graph = signals[9]
        mfcc_graph = signals[10]
        formant_graph = signals[11]
        f0_graph = signals[12]
        f1_graph = signals[13]
        f2_graph = signals[14]
        f3_graph = signals[15]
        f4_graph = signals[16]
        f5_graph = signals[17]
        compare_graph = signals[18]

        self.zero_layout.addWidget(zero_graph)
        self.normal_layout.addWidget(normal_graph)
        self.fixed_layout.addWidget(fixed_graph)
        self.power_layout.addWidget(power_graph)
        self.window_layout.addWidget(window_graph)
        self.segmented_layout.addWidget(segmented_graph)
        self.remove_layout.addWidget(remove_graph)
        self.recon_layout.addWidget(recon_graph)
        self.spec_layout.addWidget(spec_graph)
        self.mfcc_layout.addWidget(mfcc_graph)
        self.formant_layout.addWidget(formant_graph)
        self.f0_layout.addWidget(f0_graph)
        self.f1_layout.addWidget(f1_graph)
        self.f2_layout.addWidget(f2_graph)
        self.f3_layout.addWidget(f3_graph)
        self.f4_layout.addWidget(f4_graph)
        self.f5_layout.addWidget(f5_graph)
        self.original_layout.addWidget(original_graph)
        self.compare_layout.addWidget(compare_graph)

    def request_to_graph(self, sig):
        types = [1, 1, 1, 1, 1, 2, 3, 3, 1, 1]
        signals = []
        signal = sig.getSignals()
        sample_rate = sig.getSampleRate()

        signals.append(Graph(signal[0], header=True, type=types[0], width=7, height=7))
        for i in range(1, 9):
            signals.append(Graph(signal[i], type=types[i], width=7, height=7))
        signals.append(Spectrogram(signal[9], sample_rate, width=7, height=7))
        signals.append(MFCCs(signal[9], sample_rate, width=7, height=7))
        signals.append(FormantFrequently(signal[9], sample_rate, width=7, height=7))
        for i in range(6):
            signals.append(FormantFrequently(signal[9], sample_rate, i, width=7, height=7))
        signals.append(ComparisonGraph(signal[2], signal[8], i, width=7, height=7))
        self.current_opening_graphs = signals
        return signals

    def process_request(self, req, threshold=0.04):
        sample_rate, signal = PreProcessing().getAllProcess(req.getFileName(), threshold)
        self.signals[req.getID()] = ProcessedSignal(signal, sample_rate)

    def update_request(self, request):
        filename, word = request.split(',')
        req = Request(filename, word)
        self.current_req = req
        self.update_text_edit(req)
        self.update_list_widget(req)
        self.process_request(req, threshold=self.spin_box.value())
        self.update_graph_layout(req)
    def test_request(self,file_name):
        print(file_name)
    def test(self, file_name):
        self.textEdit.setText(file_name)

def main():
    app = QApplication(sys.argv)
    w = ISA_UI()
    fla = FlaskThread(w)
    
    w.show()
    fla.start()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
