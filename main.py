from flask import Flask, render_template, send_file
from os import listdir
from os.path import isfile, join

import random
import os

MEDIA_PATH = './media'
app = Flask(__name__)
log = app.logger

media_file = None
media_file_type = None

@app.route('/')
def index():
	global media_file
	media_file = get_images_from_usb()

	if not media_file:
		log.warning("No image was found.")
		return render_template("notfound.html")

	return render_template("index.html", file_type=None)

@app.route('/media')
def media(id=None):

	# if '.gif' in media_file:
	# 	return send_file(media_file, mimetype="image/jpg")	

	log.debug(media_file)	

	return send_file(media_file)

def get_images_from_usb():
	if os.name == 'nt':
		return get_images_windows()

	return get_images_linux()

def get_images_windows():
	log.debug("Getting images from windows USB")

	windows_dir = "D:\\\\"

	return get_images(windows_dir)

def get_images(dir):
	try:
		files = [f for f in listdir(dir) if isfile(join(dir, f)) and f.endswith('jpg')]
	except:
		return None

	if not files:
		log.debug("No files were found on %s", dir)
		return None

	log.debug("Total files found were %d", len(files))

	files = list(map(lambda x : join(dir, x), files))

	random.shuffle(files)

	return files[0]

def get_images_linux():
	log.debug("Getting images from linux USB")

	linux_dir = "/media/pi/7A06-8800/"

	return get_images(linux_dir)

