import os
from types import MethodDescriptorType
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import json
from PIL import Image
from static.steganography import *


app = Flask(__name__)

UPLOAD_FOLDER = './static/uploads/'
ENCODED_FOLDER = './static/encoded_files/'
TEMPLATES_FOLDER = './templates/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCODED_FOLDER'] = ENCODED_FOLDER

@app.route('/')
def index():
    return render_template('index.ejs')

@app.route('/encode')
def get_encode():
	return "This is get route of encode"

@app.route('/encode', methods=['POST'])
def encode_message():
	print(request.files)
	print("req form ",request.form)
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)

	file = request.files['file']
	if file.filename == '':
		flash('No selected file')
		return redirect(request.url)

	if file and file.filename.split('.')[-1]=='png':
		filename = secure_filename(file.filename)
		print("in here")
		encode(file, request.form['message'])
		print("done encoding")
		return redirect(url_for('download_file', name='encoded_'+filename))


@app.route('/decode')
def decode_get():
	return "this is the get route of decode"


@app.route('/decode', methods=['POST'])
def decode_message():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)

	file = request.files['file']
	if file.filename == '':
		flash('No selected file')
		return redirect(request.url)

	if file and file.filename.split('.')[-1]=='png':
		filename = secure_filename(file.filename)
		print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		decoded_message = decode(file)
		return decoded_message

@app.route('/encode/<name>')
def download_file(name):
    return send_from_directory(app.config["ENCODED_FOLDER"], name)

if __name__ == "__main__":
	app.run(port=5000)



