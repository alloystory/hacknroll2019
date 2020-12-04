# -*- coding: utf-8 -*-
import sys, logging, re, os
sys.path.insert(0, 'C:/Users/Tan Ye Kai/Documents/Uni work/Y1S2/HackNroll/amazon_scraper_full')
import amazonscraper
import global_func, json_format
from time import localtime, strftime
import ntpath

'''
1. Script to call http://178.128.110.173:9000/api/categories
2. Take in list of categories 
3. Pass it to amazon_scraper 
4. 

1. Take in a list of categories to search for, limit each category to 100 products
2. Use assert to check whether empty 
3. If not empty, write to a json format

'''

def main(category_list):

    logger = logging.getLogger(__name__)  
    time = str(strftime("%Y-%m-%d %H:%M:%S", localtime()))  
    output_dir = "C:/Users/Tan Ye Kai/Documents/Uni work/Y1S2/HackNroll/Scraper/output"


    # category_list_path = "C:/Users/Tan Ye Kai/Documents/Uni work/Y1S2/HackNroll/Scraper/data/categories.csv"
    # category_list = global_func.read_csv(category_list_path)

    # category_list = ['Sweatpants']

    for dic in category_list:

        new_output_dir = global_func.make_directory(output_dir, "files")
        image_dir = global_func.make_directory(output_dir, "images")

        category = dic["category_name"]
        category_id = dic["id"]
        new_output_dir = global_func.make_directory(new_output_dir, category)

        if(len(category_list)> 0):
            print(time + ": Number of categories in list: {}".format(len(category_list)))
        else:
            logger.error("Category list not extracted")
        
        print(time + ": Scraping.....")
        results = amazonscraper.search(category, max_product_nb=50)


        lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

        for result in results:
            # print(result)
            json_object = json_format.initialise_job_roles()
            json_object["name"] = result.title
            json_object["description"] = lorem
            json_object["category_id"] = category_id
            json_object["provider"] = "Amazon"

            price = cleanup_price(result.price)
            json_object["price"] = price

            image = cleanup_img(result.img)
            json_object["image"] = image
            

            # print(result.url)
            json_object["url"] = result.url

            if(result.rating):
                rating = convert_to_percentage(float(result.rating))
                json_object["rating"] = rating

            # print("{}".format(result.title))
            # print("  - ASIN : {}".format(result.asin))
            # print("  - {} out of 5 stars, {} customer reviews".format(result.rating, result.review_nb))
            # print("  - {}".format(result.url))
            # print("  - Image : {}".format(result.img))
            # print("  - Price : {}".format(result.price))
            # print()


            title = (result.title[:40] + '') if len(result.title) > 50 else result.title
            title = title.replace(" ", "_")
            title = re.match("^[a-zA-Z0-9_]*$", title)

            if(title):
                filename, file_extension = os.path.splitext(image)
                img_path = global_func.make_filepath(image_dir, filename,file_extension)
                if(global_func.download_img(result.img, img_path)):
                    title = title.group(0)
                    file_path = global_func.make_filepath(new_output_dir,title,".json")
                    global_func.make_json(file_path, json_object)

            else:
                pass

    return new_output_dir

# -----------------------------------------------------------------------------------------------------------------
# Local cleanup functions 

def return_img_dir():
    output_dir = "C:/Users/Tan Ye Kai/Documents/Uni work/Y1S2/HackNroll/Scraper/output"
    image_dir = global_func.make_directory(output_dir, "images")

    return image_dir

def return_files_dir():
    output_dir = "C:/Users/Tan Ye Kai/Documents/Uni work/Y1S2/HackNroll/Scraper/output"
    new_output_dir = global_func.make_directory(output_dir, "files")

    return new_output_dir

def cleanup_price(string):

    '''
    1. regex? to find the first instance of a numbernumber.numbernumber 
    or number.numbernumber
    '''
    # print(string)
    pattern1 = "\d?\d\.\d\d"

    '''
    search matches ANYWHERE in string where match only starts at the front
    '''
    matched = re.search(pattern1, string)

    if(matched):
        string = float(matched.group(0))
    else:
        string = None
    # print(string)
    return string

def cleanup_img(string):
    img_name = ntpath.basename(string)
    return img_name

def convert_to_percentage(string):
    percentage = 100* (string/5)
    return int(percentage)



if __name__ == "__main__":
    main()