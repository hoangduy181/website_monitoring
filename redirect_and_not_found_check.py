from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from constant import urls_to_care_about
import time
from utils import send_message_sync

def check_not_found_or_redirect():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    check_results_redirect = []
    check_results_not_found = []
    for url in urls_to_care_about:
        try:    
            driver.set_page_load_timeout(10)  # Đặt timeout là 30 giây
            driver.get(url)
            current_url = driver.current_url
            
            if "404" in driver.title or "not found" in driver.page_source.lower():
                print(f"[{url}] Trang web có thể đã bị sập hoặc không tồn tại.")
                check_results_not_found.append(False)
                msg = f"[{time.strftime("%Y-%m-%d %H:%M:%S")}][{url}] Trang web có thể đã bị sập hoặc không tồn tại.\n"
                send_message_sync(msg)
            else:
                print(f"[{url}] Trang hoạt động bình thường.")
                check_results_not_found.append(True)
                msg = f"[{time.strftime("%Y-%m-%d %H:%M:%S")}][{url}] Trang hoạt động bình thường.\n"
                send_message_sync(msg)
            if current_url != url:
                print(f"[{url}] Trang đã bị redirect đến: {current_url}")
                check_results_redirect.append(True)
                msg = f"[{time.strftime("%Y-%m-%d %H:%M:%S")}][{url}] Trang đã bị redirect đến: {current_url}\n"
                send_message_sync(msg)
            else:
                print(f"[{url}] Trang không bị redirect.")
                check_results_redirect.append(False)
                msg = f"[{time.strftime("%Y-%m-%d %H:%M:%S")}][{url}] Trang không bị redirect.\n"
        except TimeoutException:
            print(f"[{url}] Trang web không phản hồi, có thể đã bị sập.")
            check_results_not_found.append(False)
            check_results_redirect.append(False)
            msg = f"[{time.strftime("%Y-%m-%d %H:%M:%S")}][{url}] Trang web không phản hồi, có thể đã bị sập.\n"
        except WebDriverException as e:
            print(f"Lỗi trình duyệt: {e.msg}")
            check_results_not_found.append(False)
            check_results_redirect.append(False)
            msg = f"[{time.strftime("%Y-%m-%d %H:%M:%S")}][{url}] Lỗi trình duyệt: {e.msg}\n"
            send_message_sync(msg)
        except Exception as e:
            print(f"Lỗi không xác định: {e.msg}")
            check_results_not_found.append(False)
            check_results_redirect.append(False)
            msg = f"[{time.strftime("%Y-%m-%d %H:%M:%S")}][{url}] Lỗi không xác định: {e.msg}\n"
            send_message_sync(msg)
    driver.quit()
    return check_results_not_found, check_results_redirect


if __name__ == "__main__":
    check_not_found_or_redirect()
