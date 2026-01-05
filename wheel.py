import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
from dotenv import load_dotenv
from logger import write_log, DISPLAY

load_dotenv("credentials.env")
USERNAME = os.getenv("MINESTRATOR_USERNAME")
PASSWORD = os.getenv("MINESTRATOR_PASSWORD")

options = uc.ChromeOptions()
# options.add_argument("--headless=new")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")
driver = uc.Chrome(options=options)

def random_delay(min_seconds=1, max_seconds=3):
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Delaying for {delay:.2f} seconds...") if DISPLAY else None
    return delay


try:
    url = "https://minestrator.com/roue/de/la/fortune"
    print(f"{url=}") if DISPLAY else None
    driver.get(url)
        
    WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "pseudo"))
        )
        
    username_field = driver.find_element(By.NAME, "pseudo")
    password_field = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "#form-login .btn-submit")

    time.sleep(random_delay(2, 4))
    print(f"Filling username : {USERNAME[0:3]}...@{USERNAME.partition('@')[2]}") if DISPLAY else None
    username_field.send_keys(USERNAME)
    time.sleep(random_delay(2, 4))
    print(f"Filling password : {'*' * len(PASSWORD)}...") if DISPLAY else None
    password_field.send_keys(PASSWORD)
    write_log("\tCredentials filled.", "info")
    time.sleep(random_delay(2, 4))
    print("Clicking login button...") if DISPLAY else None
    login_button.click()
    write_log("\tLogin button clicked.", "info")

    print("Waiting for login to complete...") if DISPLAY else None
    time.sleep(random_delay(10, 60))

    wait = WebDriverWait(driver, 100)
    wheel_button = wait.until(EC.element_to_be_clickable((By.ID, "btn-roue")))

    print("Clicking wheel button...") if DISPLAY else None
    wheel_button.click()
    write_log("\tWheel button clicked.", "info")

    # <div class="toastify on  toastify-right toastify-bottom" style="background: rgb(220, 53, 69); bottom: 15px;"><img alt="Icone représentant une alerte" class="icon icon-xs" src="/assets/img/icons/theme/minesr/warning-white.svg"> Encore un peu de patience... C'est bientôt l'heure.</div>
    try: 
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toastify")))
        message_element = driver.find_element(By.CLASS_NAME, "toastify")
        message_text = message_element.text
        print(f"Message: {message_text}") if DISPLAY else None
        write_log(f"\tWheel message: {message_text}", "info")
    except Exception as e:
        print("No toast message found or error occurred:", e.partition(';')[0])
        write_log(f"\tNo toast message found or error occurred: {e.partition(';')[0]}", "error")

    try:
        result_element = driver.find_element(By.ID, "nbCredits")
        result_text = result_element.text
        if not result_text:
            result_text = "No result text found."
        print(f"Result: {result_text}")
        write_log(f"\tWheel result: {result_text}", "info")
    except Exception as e:
        print("Could not find result element:", e)
        write_log(f"\tCould not find result element: {e}", "error")




    time.sleep(random_delay(60, 120))
    print("Finished.") if DISPLAY else None

except Exception as e:
    print("An error occurred:", e)
    write_log(f"\tAn error occurred: {e}", "error")

finally:
    driver.quit()