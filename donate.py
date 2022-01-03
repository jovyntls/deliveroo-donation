import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


DELIVEROO_DONATION_URL = "https://deliveroo.com.sg/menu/singapore/chinatown/food-from-the-heart-x-deliveroo-new"
TIMEOUT = 10

load_dotenv()
EMAIL = os.getenv('DELIVEROO_EMAIL')
PASSWORD = os.getenv('DELIVEROO_PASSWORD')

chrome_options = Options() 
chrome_options.add_experimental_option("detach", True) # keeps browser open
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(DELIVEROO_DONATION_URL)

print('logging in...')
driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div[1]/div/div[2]/div/div[2]/p/span/a').click()
WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "continue-with-email"))).click()
WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located((By.ID, "email-address"))).send_keys(EMAIL + '\n')
WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located((By.ID, "login-password"))).send_keys(PASSWORD + '\n')
WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#find_food']"))).click()
# wait until dialog disappears
WebDriverWait(driver, TIMEOUT).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[aria-labelledby='modal-header-title']")))

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
WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Go to checkout')]"))).click()
WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='switch'][aria-checked='false'][type='button']"))).click()
driver.execute_script("window.scrollTo(0, 400);")

print('manually place delivery order :)')

