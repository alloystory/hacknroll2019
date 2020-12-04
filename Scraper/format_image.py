from PIL import Image
import io

def format(image_data, file_type):
	width = 400
	height = int(width / 10 * 16)

	# Reading image data
	input_bytes = io.BytesIO(image_data)
	input_image = Image.open(input_bytes)
	input_width = input_image.width
	input_height = input_image.height

	# Obtaining most dominant color
	all_colors = input_image.getcolors(input_image.size[0] * input_image.size[1])
	most_dom_color = max(all_colors)

	# Resizing image to fit layer
	resized_width = int(width)
	resized_height = int(input_height / (input_width / width))
	resized_image = input_image.resize((resized_width, resized_height))

	# Flatten resized image and background layer
	offset = (int((width - resized_width) / 2), int((height - resized_height) / 2))
	output_layer = Image.new("RGB", (width, height), most_dom_color[1])
	output_layer.paste(resized_image, offset)

	# Output image
	output_arr = io.BytesIO()
	output_type = get_type(file_type)
	output_layer.save(output_arr, output_type)
	return output_arr.getvalue()

def get_type(file_type):
	if file_type in {".jpg", ".jpeg"}:
		return "jpeg"
	elif file_type in {".png"}:
		return "png"