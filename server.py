import os
import random
from flask import Flask,request, url_for, render_template,jsonify 
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '../Desktop/kuay'
ALLOWED_EXTENSIONS = set(['wav','aac'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/test/post', methods=['POST'])
def get_tasks():
    if request.method == 'POST':
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return "No file"
            file = request.files['file']
            # submit a empty part without filename
            if file.filename == '':
                return "without filename"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return "success"
    


if __name__ == '__main__':
    app.run(debug=True)
