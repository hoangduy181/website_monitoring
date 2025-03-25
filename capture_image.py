from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from PIL import Image
from io import BytesIO
import re
from utils import regex

def advanced_scroll_capture(driver, url, delay=2):
    driver.get(url)
    time.sleep(delay)  # Initial load delay
    
    # Get initial dimensions
    viewport_height = driver.execute_script("return window.innerHeight")
    total_height = driver.execute_script("return Math.max("
        "document.body.scrollHeight, "
        "document.documentElement.scrollHeight, "
        "document.body.offsetHeight, "
        "document.documentElement.offsetHeight, "
        "document.body.clientHeight, "
        "document.documentElement.clientHeight"
    ")")
    
    # Prepare page for scrolling
    driver.execute_script("""
        // Remove position:fixed and sticky elements
        document.querySelectorAll('*').forEach(function(el) {
            const style = window.getComputedStyle(el);
            if (style.position === 'fixed' || style.position === 'sticky') {
                el.style.position = 'static';
            }
        });
        
        // Ensure scrolling is possible
        document.body.style.overflow = 'visible';
        document.documentElement.style.overflow = 'visible';
        document.body.style.height = 'auto';
    """)
    
    screenshots = []
    current_position = 0
    overlap = 50  # pixels of overlap between screenshots
    
    while current_position < total_height:
        # Scroll using multiple methods for better compatibility
        driver.execute_script(f"""
            // Method 1: Standard scroll
            window.scrollTo(0, {current_position});
            
            // Method 2: Smooth scroll
            window.scrollTo({{
                top: {current_position},
                behavior: 'smooth'
            }});
            
            // Method 3: Element scroll
            document.documentElement.scrollTop = {current_position};
            document.body.scrollTop = {current_position};
        """)
        
        # Force layout recalculation and wait for content
        driver.execute_script("""
            // Trigger reflow
            void document.documentElement.offsetHeight;
            
            // Force any lazy-loaded images
            const images = document.getElementsByTagName('img');
            for(let img of images) {
                if(img.loading === 'lazy') {
                    img.loading = 'eager';
                }
            }
        """)
        
        # Wait for any dynamic content
        time.sleep(delay)
        
        # Take screenshot
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(Image.open(BytesIO(screenshot)))
        
        # Update scroll position
        current_position += (viewport_height - overlap)
        
        # Check if total height changed (dynamic content)
        new_height = driver.execute_script("return Math.max("
            "document.body.scrollHeight, "
            "document.documentElement.scrollHeight"
        ")")
        if new_height > total_height:
            total_height = new_height
    
    # Combine screenshots
    final_image = Image.new('RGB', (screenshots[0].width, total_height))
    y_offset = 0
    
    for i, screenshot in enumerate(screenshots):
        if i > 0:
            y_offset = (i * (viewport_height - overlap))
        final_image.paste(screenshot, (0, y_offset))
    
    return final_image

# Usage example:
def capture_page(url, folder_name, batch_name):
    domain_name = regex.sub('_', url.lower())
    domain_name = re.sub('_+', '_',
                        domain_name)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--headless')  # Optional: run in headless mode
    
    driver = webdriver.Chrome(options=options)
    try:
        # driver.set_window_size(1920, 1080)  # Set consistent window size
        try:
            # Wait up to 10 seconds for the popup button
            driver.get(url)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "close-dialog"))
            )
            button.click()
        except Exception as e:
            print(f"Could not click popup button: {e}")
        
        if os.path.exists(f'{folder_name}/{domain_name}'):
            print('Folder already exists')
        else:
            os.makedirs(f'{folder_name}/{domain_name}')
            print('Folder created')
            
        full_page = advanced_scroll_capture(driver, url)
        full_page.save(f'{folder_name}//{domain_name}//{batch_name}.png')
    finally:
        driver.quit()