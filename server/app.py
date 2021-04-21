import os
import sys
from flask import Flask, render_template, request, redirect
from asciiTrans import asciiTran
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'uploads')
RESULT_FOLDER = os.path.join('static', 'results')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('index.html', msg='No file selected')


@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('index.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('index.html', msg='No file selected')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            asciiTran(filename)
            # call the ascii function on it
            full_filename = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)

            full_filename = os.path.join(
                app.config['RESULT_FOLDER'], "result.png")
            # extract the text and display it
            return render_template('index.html',
                                   msg='Successfully processed',
                                   img_src=full_filename)
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
