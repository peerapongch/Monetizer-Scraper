from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import pandas as pd
from pandas.util.testing import assert_frame_equal
import os
import time
import numpy as np
from functions_v1 import *

## config
url = "https://app.monetizer.com/"
username = "perry96121@gmail.com"
password = "Qg8RlLdnl7"
cycle = 5 # limit of number of cycles
N = 50 # maximum entries per cycle before conflict resolution
save_file = 'save.csv'
kim=100 # keeping this number of datapoints in memory for comparison of duplication

# start
driver = webdriver.Chrome()
# driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(60)

driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.implicitly_wait(30)

## need to handle delayed loading of submit button in the landing page
try:
    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
        "//input[@type='submit']"
        # "//div[@class='offerList']"
        )))
    print('landing page ready')
except TimeoutException:
    print('took too long')
driver.find_element_by_xpath("//input[@type='submit']").click()

driver.implicitly_wait(20)
## to the live leads
liveleads_button = driver.find_element_by_id("menu_liveleadsButton")
liveleads_button.click()


# fun begins here
begin_extract(driver, cycle, N, kim, save_file)
