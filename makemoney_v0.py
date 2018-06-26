# this is the main script which executes the task
## roughly they are
## 1. initialise the spider
## 2. navigate to the live leads page
## 3. send requests and get response
## 4. repeat


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time

url = "https://app.monetizer.com/"

driver = webdriver.Chrome()
# driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(60)

user = driver.find_element_by_id("username")
user.send_keys(username)
passw = driver.find_element_by_id("password")
passw.send_keys(password)
# driver.implicitly_wait(30)
try:
    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
        "//input[@type='submit']"
        # "//div[@class='offerList']"
        )))
    print('page ready')
except TimeoutException:
    print('took too long')

enter_button = driver.find_element_by_xpath("//input[@type='submit']")
enter_button.click()

driver.implicitly_wait(20)
## to the live leads
liveleads_button = driver.find_element_by_id("menu_liveleadsButton")
liveleads_button.click()

## from here refresh, wait, and repeat

try:
    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
        "//li[@class='offerRow list-group-item']"
        # "//div[@class='offerList']"
        )))
    print('page ready')
except TimeoutException:
    print('took too long')
# finally:
#     print('nope :(')
#     driver.quit()

# with open('ll_source.html','w') as file:
#     file.write(driver.page_source)
## harvest with N-batch polling
## assumption that no N running entries are identical
N=10

soup_level1=BeautifulSoup(driver.page_source,'lxml')
print(soup_level1)
