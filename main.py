from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

STREAMLIT_URL = "https://benson-mugure-portfolio.streamlit.app/"

def main():
    options = Options()
    options.add_argument('--headless=new')  # new headless mode for stability
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--window-size=1920,1080')

    # Use webdriver_manager to auto-install ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(STREAMLIT_URL)
        print(f"Opened {STREAMLIT_URL}")

        wait = WebDriverWait(driver, 30)
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
        )
        button.click()
        print("Button clicked successfully!")

        # Option 1: wait for button to disappear
        try:
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
            print("Wake-up button disappeared ✅")
        except TimeoutException:
            print("Button did not disappear in time ❌")

        # Option 2: wait for "waking up" text to appear
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'This will take just a sec! Your app is waking up!')]"))
            )
            print("Found wake-up message: app is starting ⏳")
        except TimeoutException:
            print("Did not see wake-up message — maybe app started instantly or text changed")

    except TimeoutException:
        print("No button found — maybe the app was already awake?")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
