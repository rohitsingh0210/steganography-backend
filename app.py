import os
import re
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
    return render_template('index.html')

@app.route('/encode')
def get_encode():
	return render_template("encode.html")

@app.route('/encode', methods=['POST'])
def encode_message():
	print("FILES ARE ",request.files)
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
		url = url_for('download_file', name='encoded_'+filename)
		return "<a href="+url+" download><img src="+url+" alt='img'><button>Download encrypted image</button></a>"
		return redirect(url_for('download_file', name='encoded_'+filename))

@app.route('/encodeWithSplit', methods=['POST'])
def encodeWithSplit():
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
		encode_and_split(file, request.form['message'])
		print("done encoding and split")
		keyurl = url_for('download_file', name='encoded_key_'+filename)
		encurl = url_for('download_file', name='encoded_enc_'+filename)
		return "<a href="+keyurl+" download><img src="+keyurl+" alt='img'><button>Download key img</button></a><a href="+encurl+" download><img src="+encurl+" alt='img'><button>Download encoded img</button></a>"
		return redirect(url_for('download_file', name='encoded_key_'+filename))

@app.route('/decode')
def decode_get():
		return render_template("decode.html")


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
		return '<h1>'+decoded_message+'</h1>'
		# return render_template("decode.html", {"msg":decode_message})

@app.route('/decodeWithSplit', methods=['POST'])
def decode_message_with_split():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	file2 = request.files['file2']
	if file.filename == '' or file2.filename == '':
		flash('No selected file')
		return redirect(request.url)

	if file and file2 and file.filename.split('.')[-1]=='png':
		filename = secure_filename(file.filename)
		filename2 = secure_filename(file2.filename)
		print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		decoded_message = decodeSplit(file, file2)

		return decoded_message

@app.route('/encode/<name>')
def download_file(name):
    return send_from_directory(app.config["ENCODED_FOLDER"], name)


@app.route('/decodeWithSplit')
def get_decodeWithSplit():
	return render_template("decodeWithSplit.html")


if __name__ == "__main__":
	app.run(port=5000)



