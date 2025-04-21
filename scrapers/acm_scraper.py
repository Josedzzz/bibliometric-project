from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def start_browser():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_example():
    driver = start_browser()
    try:
        driver.get("https://scholar.google.com/")
        time.sleep(2)  # Espera que cargue

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("computational thinking")
        search_box.submit()

        time.sleep(3)

        results = driver.find_elements(By.CLASS_NAME, "gs_ri")
        for idx, result in enumerate(results):
            title = result.find_element(By.TAG_NAME, "h3").text
            print(f"{idx+1}. {title}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_example()

