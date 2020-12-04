from collections import OrderedDict

def initialise_job_roles():
	output_data = OrderedDict()
	output_data["name"] = ""
	output_data["description"] = ""
	output_data["category_id"] = ""
	output_data["provider"] = ""
	output_data["price"] = ""
	output_data["image"] = ""
	output_data["url"] = ""
	output_data["rating"] = ""

	return output_data