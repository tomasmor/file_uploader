import os
from flask import Flask, request, redirect, url_for, render_template, session, flash, abort, send_from_directory
from werkzeug.utils import secure_filename

from db import dummy_auth



def upload_folder():
    return os.path.dirname(os.path.realpath(__file__))

def download_folder():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "downloads")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder()
app.config['DOWNLOAD_FOLDER'] = download_folder()


@app.route('/file/upload', methods=['POST', 'PUT', 'GET'])
def upload_file(filename=None):
    if not session.get('logged_in'):
        return render_template('login.html')

    if request.method == 'POST' or request.method == 'PUT':
        file_handler = request.files['file']
        filename = secure_filename(file_handler.filename)
        file_handler.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('upload.html')

@app.route('/file/download', methods=['POST', 'PUT', 'GET'])
def file_download_list():
    if not session.get('logged_in'):
        return render_template('login.html')
    download_list = os.listdir(download_folder())
    download_source = ['/file/download/{}'.format(download) for download in download_list]
    return render_template('download.html', download_list=download_list, download_source=download_source)

@app.route('/file/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('menu.html')

@app.route('/login', methods=['POST'])
def do_login():
    if dummy_auth(request.form['username'], request.form['password']):
        session['logged_in'] = True
        return render_template('menu.html')
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()




if __name__ == "__main__":
    app.secret_key = os.urandom(12)

    app.run(host='0.0.0.0',debug=True)
