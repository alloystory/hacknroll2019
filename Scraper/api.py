import requests 
import amazon_scraper
import format_image
import global_func
import os, json
from io import BytesIO
from PIL import Image

def main():
	'''
	1. Pass entire library to amazon scraper
	2. Let amazon scraper get cateory names and category id 
	3. Once scraper is done, post requests
	'''

	categories_db = "http://178.128.110.173:9000/api/categories"
	image_db = "http://178.128.110.173:9000/api/items/images"
	items_db = "http://178.128.110.173:9000/api/items"

	# category_list = requests.get("http://178.128.110.173:9000/api/categories")
	# files_dir = amazon_scraper.main(category_list.json())


	files_dir = "C:/Users/Tan Ye Kai/Documents/Uni work/Y1S2/HackNroll/Scraper/output/files"
	resized_dir = "C:/Users/Tan Ye Kai/Documents/Uni work/Y1S2/HackNroll/Scraper/output/resized_images"
	# img_dir = amazon_scraper.return_img_dir()
	# resized_dir = global_func.resize_images(img_dir)
	# files_dir = global_func.return_files_dir()

	def recursive_post(img_dir, db):
		for path in os.listdir(img_dir):
			filepath = img_dir + "/" + path
			if (os.path.isfile(filepath)):
				if(db == items_db):
					post_json(filepath, db)
				else:
					post_image(filepath, path, db)
			else:
				recursive_post(filepath, db)

	# recursive_post (files_dir, items_db)
	recursive_post(resized_dir, image_db)
	
def post_json(filepath, db):

	with open(filepath, "r") as f:
		data = json.load(f)
		# print(data)
		# print(db)
		r = requests.post(db, json=data)
		print("Posting : " +filepath)
		print(r.content)

def post_image(filepath, path, db):

	# filepath = "C:/Users/Tan Ye Kai/Documents/Uni work/Y1S2/HackNroll/Scraper/output/resized_images/21KvoGdMCNL.jpg"
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print(filepath)
	with open(filepath, "rb") as f:
		# print(data)
		# header = "img"
		# data = {"img" : f}
		# r = requests.post(db +"/" + path, data=data)

		url = db + "/" + path
		img = format_image.format(f.read() ,".jpg")
		print(type(img))
		# img = BytesIO(f)
		payload = {"img" : img}

		# print(img)
		r = requests.request("POST", url, files=payload)

		# print(r.content)
		print("Posting : " +filepath)
		print(r.content)

if __name__ == "__main__":
    main()
