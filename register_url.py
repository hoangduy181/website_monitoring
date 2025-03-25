## todo:
# 1. download html from url to folder
# 2. get hash_value of all urls, then save to file
# 3. download image from url to folder

from utils import save_html_to_path, save_hash_value
from capture_image import capture_page
from constant import save_html_folder, hash_value_csv, save_image_folder, urls_to_care_about



def save_htmls():
    for url in urls_to_care_about:
        save_html_to_path(url, save_html_folder, 'original')

def get_hash_values():
    for url in urls_to_care_about:
        save_hash_value(url, save_html_folder, hash_value_csv, 'original')
    pass

def get_images():
    for url in urls_to_care_about:
        capture_page(url, save_image_folder, 'original')
    pass

def main():
    save_htmls()
    get_hash_values()
    get_images()

if __name__ == '__main__':
    main()
