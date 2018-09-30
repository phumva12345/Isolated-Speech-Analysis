import os
import random

from flask import Flask,request, url_for, render_template,jsonify
from werkzeug.utils import secure_filename
from PySide2 import QtCore
from ISA_UI import *

# Init URL and port
PORT = 5000
ROOT_URL = 'http://localhost:{}'.format(PORT)

app = Flask(__name__)

# Set recievable file
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['wav'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/test/post', methods=['POST'])
def update_request():
    # Call the UI application in Flask
    w = FlaskThread._single.application

    # check if the post request has the file part
    if 'file' not in request.files:
        return "No file"
    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return "without filename"

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        w.update_request(file_name)
        return "success"


class FlaskThread(QtCore.QThread):
    # Singleton Flask
    _single = None

    def __init__(self, application):
        QtCore.QThread.__init__(self)
        if FlaskThread._single:
            raise FlaskThread._single
        FlaskThread._single = self
        self.application = application

    def __del__(self):
        self.wait()

    def run(self):
        self.application.run(port=PORT, debug=True, use_reloader=False)

def start_GUI(application):
    qtApp = QApplication(sys.argv)

    webapp = FlaskThread(application)
    w = ISA_UI()

    webapp.start()
    w.show()

    qtApp.aboutToQuit.connect(webapp.terminate)
    QApplication.setQuitOnLastWindowClosed(False)

    return qtApp.exec_()

if __name__ == '__main__':
    sys.exit(start_GUI(app))
