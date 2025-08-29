from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time

STREAMLIT_URL = "https://benson-mugure-portfolio.streamlit.app/"

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(STREAMLIT_URL)
        print(f"Opened {STREAMLIT_URL}")

        # Wait for and click the wake-up button
        wait = WebDriverWait(driver, 30) # 30-second initial wait
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
        )
        button.click()
        print("Button clicked successfully!")

        # Confirm the wake-up message appears
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'This will take just a sec! Your app is waking up!')]"))
        )
        print("Found wake-up message: app is starting ⏳")

        # --- NEW: WAIT FOR THE APP TO ACTUALLY LOAD ---
        # We increase the timeout here because app startup can be slow.
        print("Waiting for the main application to load...")
        app_wait = WebDriverWait(driver, 120) # Wait up to 2 minutes for app to load
        
        # Look for a unique element from your app, like the main header.
        app_header_xpath = "//*[contains(text(), 'Benson Mugure')]"
        app_wait.until(
            EC.presence_of_element_located((By.XPATH, app_header_xpath))
        )
        print("Application has fully loaded! ✅")

    except TimeoutException:
        print("No wake-up button found or app took too long to load. Maybe it was already awake?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Optional: take a screenshot to debug in GitHub Actions
        # driver.save_screenshot("final_state.png")
        driver.quit()
        print("Script finished.")


if __name__ == "__main__":
    main()