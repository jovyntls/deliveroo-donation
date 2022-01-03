import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


DELIVEROO_DONATION_URL="https://deliveroo.com.sg/menu/singapore/chinatown/food-from-the-heart-x-deliveroo-new"

load_dotenv()
EMAIL = os.getenv('DELIVEROO_EMAIL')
PASSWORD = os.getenv('DELIVEROO_PASSWORD')

chrome_options = Options() 
chrome_options.add_experimental_option("detach", True) # keeps browser open
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(DELIVEROO_DONATION_URL)
print('logging in...')
driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div[1]/div/div[2]/div/div[2]/p/span/a').click()
driver.find_element(By.ID, 'continue-with-email').click()
driver.find_element(By.ID, 'email-address').send_keys(EMAIL + '\n')
time.sleep(1.5)
driver.find_element(By.ID, 'login-password').send_keys(PASSWORD + '\n')
time.sleep(3)
driver.find_element(By.XPATH, '//a[@href="#find_food"]').click() # selects MOST RECENT address
time.sleep(3)
print('finding items...')
driver.find_element(By.XPATH, "//*[contains(text(), 'Donation Amounts')]").click()
# order $5 donation
driver.find_element(By.CSS_SELECTOR, '[aria-label="$5 Donation"]').click()
time.sleep(1)
driver.find_elements(By.XPATH, "//*[contains(text(), 'Agree')]")[-1].click()
ActionChains(driver).send_keys('\t\t').send_keys('\n').perform()
time.sleep(2)
# order $10 donation
driver.find_element(By.CSS_SELECTOR, '[aria-label="$10 Donation"]').click()
time.sleep(1)
driver.find_elements(By.XPATH, "//*[contains(text(), 'Agree')]")[-1].click()
ActionChains(driver).send_keys('\t\t').send_keys('\n').perform()
time.sleep(2)
print('checkout...')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
driver.find_element(By.XPATH, "//*[contains(text(), 'Go to checkout')]").click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button[aria-label='switch'][aria-checked='false'][type='button']").click()
time.sleep(2)
driver.execute_script("window.scrollTo(0, 400);")

print('manually place delivery order :)')

