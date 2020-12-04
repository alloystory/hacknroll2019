from pathlib import Path
import os, ntpath
from difflib import SequenceMatcher
import json, csv
from time import localtime, strftime
import urllib.request 
import format_image
from PIL import Image

time = str(strftime("%Y-%m-%d %H:%M:%S", localtime())) 
def make_directory(directory, extn):
	# path = os.path.join(directory, extn)
	path = directory + "/" + extn
	if(not os.path.isdir(path)):
		os.mkdir(path)
	return path

def make_filepath(directory, file_name, ext):
	# filepath = os.path.join(directory, file_name) 
	filepath = directory + "/" + file_name
	filepath = filepath + ext
	return filepath

def make_json(output_filepath, input_data):
	with open(output_filepath, "w+", encoding = "utf-8") as output_file:
		json.dump(input_data, output_file)
	print(time + " File output to: "+output_filepath)

def read_csv(filepath):
	output = []
	with open(filepath, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			for cat in row:
				output.append(cat)
	return output

def download_img(image_url, image_name):
	try:
		urllib.request.urlretrieve(image_url, image_name)
		return True
	except Exception as e:
		print(e)
		return False

def resize_images(img_dir):
	# filepath, filename = ntpath.split(img_dir)
	# filename, file_extension = os.path.splitext(filename)

	p = Path(img_dir).parents[0]
	resized_dir = os.path.join(p, "resized_images")
	make_directory(str(p), "resized_images")


	for path in os.listdir(img_dir):
		filename, file_extension = os.path.splitext(path)
		with open(os.path.join(img_dir, path), 'rb+') as f:
			img = format_image.format(f.read() ,file_extension)
			# print(img)
			with open(resized_dir + "/" + path, "wb+") as g:
				g.write(img)
			# img.save(resized_dir + "/" + path)
			print(time + " File output to: "+ resized_dir + "/" + path)

	return resized_dir








