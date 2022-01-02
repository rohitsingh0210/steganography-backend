from PIL import Image
import cv2
import numpy as np
from numpy import random

def genData(data):
		newd = []
		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd
        
def modPix(pix, data):
	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1

		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

def encode(img, message):

	image = Image.open(img, 'r')

	if (len(message) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, message)
	newimg.save('./static/encoded_files/encoded_'+img.filename.split('/')[-1])

def encode_and_split(img, message):
	image = Image.open(img, 'r')
	if (len(message) == 0):
		raise ValueError('Data is empty')
	newimg = image.copy()
	encode_enc(newimg, message)
	c, r = newimg.size
	key = random.randint(256, size = (r, c, 4), dtype=np.uint8)
	enc = np.array(newimg) ^ key
	key = Image.fromarray(key)
	enc = Image.fromarray(enc)
	key.save('./static/encoded_files/encoded_key_'+img.filename.split('/')[-1])
	enc.save('./static/encoded_files/encoded_enc_'+img.filename.split('/')[-1])


def decode(img):
	print("TYPE IS ",type(img))
	if(type(img)==Image.Image):
		image = img
	else:
		image = Image.open(img, 'r')

	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data

def decodeSplit(img1, img2):
	key = Image.open(img1, 'r')
	enc = Image.open(img2, 'r')
	newkey = key.copy()
	newenc = enc.copy()
	dec = np.array(newenc) ^ np.array(newkey)
	decryptedImage = Image.fromarray(dec)
	decryptedMessage = decode(decryptedImage)
	return decryptedMessage