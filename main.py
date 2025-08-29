from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
import os

# You can now pass the URL as an environment variable in your GitHub Action
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://benson-mugure-portfolio.streamlit.app/")

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    app_loaded = False

    try:
        driver.get(STREAMLIT_URL)
        print(f"Opened {STREAMLIT_URL}")

        # Try to click the wake-up button if it exists
        try:
            initial_wait = WebDriverWait(driver, 20)
            button = initial_wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            button.click()
            print("Button clicked successfully!")
            print("Found wake-up message: app is starting ⏳")
        except TimeoutException:
            print("No wake-up button found. Assuming app is already running or loading.")

        # Polling loop to check for app load status
        print("Starting polling loop to check for app load status...")
        for i in range(1, 7):
            print(f"--- Attempt {i}/6 ---")
            try:
                poll_wait = WebDriverWait(driver, 25)
                
                # --- UNIVERSAL SELECTOR: Checks for the main app container ---
                app_container_xpath = "//div[@class='appview-container']"
                poll_wait.until(EC.presence_of_element_located((By.XPATH, app_container_xpath)))
                
                print("Application has fully loaded! ✅")
                app_loaded = True
                break 
            except TimeoutException:
                print("App not loaded yet. Refreshing page and trying again...")
                driver.refresh()
                time.sleep(5)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if not app_loaded:
            print("App did not load within the expected time. ❌")
        driver.quit()
        print("Script finished.")
    
    if not app_loaded:
        exit(1)


if __name__ == "__main__":
    main()
