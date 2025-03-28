import requests
import re
import hashlib
import pandas as pd
import os
from telegram import Bot
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

regex = re.compile('[^a-zA-Z10-9]')

TELEGRAM_BOT_TOKEN = '7465826162:AAEdOXm_w8w39610OJytH9bwg1b1Bk3aK4U'
TELEGRAM_CHAT_ID = ['942086993']  # Replace with the correct numeric chat ID

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        send_message_tasks = [bot.send_message(chat_id=chat_id, text=message) for chat_id in TELEGRAM_CHAT_ID]
        await asyncio.gather(*send_message_tasks)
    except Exception as e:
        print(f"Error sending message: {e}")

def send_message_sync(message):
    asyncio.run(send_telegram_message(message))

def get_page_content(url, timeout=30):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(timeout)
        
        # Navigate to URL
        driver.get(url)
        
        # Wait for body content to be present
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Execute JavaScript to get rendered page content
        page_content = driver.execute_script("""
            return {
                'html': document.documentElement.outerHTML,
                'text': document.body.innerText,
                'title': document.title
            }
        """)
        
        return page_content['html']
        
    except TimeoutException:
        print(f"Timeout while loading {url}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None
    finally:
        if 'driver' in locals():
            driver.quit()

def save_html_to_path(web_url, folder_path, batch_name):
    domain_name = web_url
    domain_name = regex.sub('_', domain_name.lower())
    # remove duplicate underscores
    domain_name = re.sub('_+', '_',
                        domain_name)
    print(domain_name)
    url = web_url.strip()
    try:
        # Get the webpage content
        response = get_page_content(url, timeout=30000)
        if os.path.exists(f'{folder_path}//{domain_name}'):
            print(f"Folder {domain_name} already exists")
        else:
            os.makedirs(f'{folder_path}//{domain_name}')
            print(f"Folder {domain_name} created")
        # Write the HTML content to a file
        with open(f'{folder_path}//{domain_name}//{batch_name}.txt', 'w', encoding='utf-8') as file:
            file.write(response)
        print("HTML content has been saved to {}//{}.txt".format(domain_name, batch_name))
        
    except requests.RequestException as e:
        print("{} Error downloading the webpage: {}".format(domain_name, e))
    return f'{folder_path}/{domain_name}.txt'

def get_html_hash(html_file_path):
    """
    Calculate the SHA-256 hash of an HTML file
    Args:
        html_path: Path to the HTML file
    Returns:
        Hash value as a hexadecimal string
    """

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Create SHA-256 hash object
            hash_object = hashlib.sha256(content.encode())
            # Get hexadecimal representation of hash
            return hash_object.hexdigest()
    except Exception as e:
        print(f"Error calculating hash: {e}")
        return None
    
def save_hash_value(url, folder_path, csv_file, batch_name):
    domain_name = regex.sub('_', url.lower())
    domain_name = re.sub('_+', '_',
                        domain_name)
    html_path = f'{folder_path}//{domain_name}//{batch_name}.txt'
    
    hash_value = get_html_hash(html_path)
    if batch_name == 'original':
        df = pd.DataFrame({
            'file_path': [domain_name],
            'hash_value': [hash_value]
        })
        df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
                
def compare_hash_value(url, folder_path, csv_file, test_batch_name):
    domain_name = regex.sub('_', url.lower())
    domain_name = re.sub('_+', '_',
                        domain_name)
    new_file_path = f'{folder_path}//{domain_name}//{test_batch_name}.txt'
    # old_file_path = f'{folder_path}//{domain_name}//original.txt'
    new_hash = get_html_hash(new_file_path)
    df = pd.read_csv(csv_file)
    old_hash = df.loc[df['file_path'] == domain_name, 'hash_value'].values[0]
    
    if new_hash == old_hash:
        print(f"Hash values match for {domain_name}")
    else:
        print(f"Hash values do not match for {domain_name}")
    
    return new_hash == old_hash
