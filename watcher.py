import cv2
import time
from skimage.metrics import structural_similarity as ssim
from constant import urls_to_care_about, save_image_folder, save_html_folder, hash_value_csv
from capture_image import capture_page
import os
import re
from utils import regex, save_html_to_path, compare_hash_value
from ngram_model import predict

def check_with_n_gram(test_batch_name):
    result = []
    for index, url in enumerate(urls_to_care_about):
        domain_name = regex.sub('_', url.lower())
        domain_name = re.sub('_+', '_',
                            domain_name)
        file_path = f'{save_html_folder}//{domain_name}//{test_batch_name}.txt'
        res = predict(file_path)
        result.append(res)
    
    if all(result):
        print("All pages are not defaced")
        
    else:
        print("Some pages are defaced!")
        url_to_check = [urls_to_care_about[index] for index, res in enumerate(result) if not res]
        print("url_to_check:", url_to_check)
        return False
        
    return True

def get_images(test_batch_name):
    for index, url in enumerate(urls_to_care_about):
        domain_name = regex.sub('_', url.lower())
        domain_name = re.sub('_+', '_',
                            domain_name)
        
        sub_folder = f'{save_image_folder}'
        capture_page(url, sub_folder, test_batch_name)

def get_htmls(test_batch_name):
    for url in urls_to_care_about:
        save_html_to_path(url, save_html_folder, test_batch_name)

def check_diff_htmls(test_batch_name):
    results = []
    for index, url in enumerate(urls_to_care_about):
        domain_name = regex.sub('_', url.lower())
        domain_name = re.sub('_+', '_',
                            domain_name)
        single_res = compare_hash_value(url, save_html_folder, hash_value_csv, test_batch_name)
        results.append(single_res)
    if all(results):
        print("All pages are similar")
        return True
    else:
        print("Some pages are different!")
        url_to_check = [urls_to_care_about[index] for index, res in enumerate(results) if not res]
        print("url_to_check:", url_to_check)
        return False
        # print(f"Hash value comparison result: {res}")
    pass

def check_diff_images(test_batch_name, delete_images=False):
    ssim_scores = []
    for index, url in enumerate(urls_to_care_about):
        domain_name = regex.sub('_', url.lower())
        domain_name = re.sub('_+', '_',
                            domain_name)
        
        original_image = f'{save_image_folder}//{domain_name}//original.png'
        test_image = f'{save_image_folder}//{domain_name}//{test_batch_name}.png'
        img1 = cv2.imread(original_image, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(test_image, cv2.IMREAD_GRAYSCALE)

        # Compute SSIM
        score, diff = ssim(img1, img2, full=True)
        print(f"SSIM {index} Score: {score}")
        ssim_scores.append(score)

    if all(score > 0.9 for score in ssim_scores):
        print("All pages are similar")
        # delete all test images
        if (delete_images):
            sub_folder = f'{save_image_folder}//{domain_name}'
            for index, url in enumerate(urls_to_care_about):
                try:
                    test_image = f'{sub_folder}//{test_batch_name}.png'
                    os.remove(test_image)
                except Exception as e:
                    print(f"Error deleting {test_image}: {e}")
    else:
        print("Some pages are different!")
        low_scores = [index for index, score in enumerate(ssim_scores) if score < 0.9]
        print("Low scores:", low_scores)
        url_to_check = [urls_to_care_about[index] for index in low_scores]
        print("url_to_check:", url_to_check)

# if __name__ == '__main__':
    
def watch_one_time():
    print('capturing website'.center(20, '_'))
    current_time = time.strftime("%Y%m%d-%H%M%S")
    print("🐧 ~ current_time:", current_time)
    test_batch_name = f'test_batch_{current_time}'
    print("🐧 ~ test_batch_name:", test_batch_name)
    
    get_htmls(test_batch_name)
    ngram_check =check_with_n_gram(test_batch_name)
    if not ngram_check:
        print('*'*20)
        print('NGRAM')
        print('Please check!!!!')
        print('*'*20)
    res = check_diff_htmls(test_batch_name)
    if not res:
        print('*'*20)
        print('HASH VALUE')
        print('Please check!!!!')
        print('*'*20)
    
    get_images(test_batch_name)
    check_diff_images(test_batch_name, delete_images=True)
    
if __name__ == '__main__':
    watch_one_time()