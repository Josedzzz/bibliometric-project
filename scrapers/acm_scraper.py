import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Configure download directory
download_dir = os.path.join(os.getcwd(), "data", "raw")
os.makedirs(download_dir, exist_ok=True)

# Set Firefox download preferences
firefox_options = Options()
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.download.dir", download_dir)
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/x-bibtex")

driver = webdriver.Firefox(options=firefox_options)
driver.get("https://dl.acm.org/action/doSearch?AllField=computational+thinking&startPage=0&pageSize=50")

try:
    # Wait for page to load completely
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='markall']"))
    )

    # Select all papers (single click is enough)
    checkbox = driver.find_element(By.CSS_SELECTOR, "input[name='markall']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
    driver.execute_script("arguments[0].click();", checkbox)
    print("✓ Selected all papers")
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)
    driver.execute_script("arguments[0].click();", checkbox)

    # Click Export Citations button
    export_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.export-citation"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", export_button)
    driver.execute_script("arguments[0].click();", export_button)
    print("✓ Export modal opened")
    time.sleep(3)

    # Wait for modal and click "Download citation" button
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.export-options"))
    )
    
    # Find button by title attribute containing "Download citation"
    download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title*='Download citation'], [title*='Download citations']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
    driver.execute_script("arguments[0].click();", download_button)
    print(f"✓ Download started - saving to: {download_dir}")

    # Wait for download to complete
    print("Waiting for download to finish... (25 seconds)")
    time.sleep(25)
    print("✅ Download complete!")

except Exception as e:
    print(f"❌ Error occurred: {str(e)}")
finally:
    print("🏁 Script completed")
    input("Press Enter to close the browser...")
    driver.quit()
