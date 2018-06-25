# this is the main script which executes the task
## roughly they are
## 1. initialise the spider
## 2. navigate to the live leads page
## 3. send requests and get response
## 4. repeat


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium import WebElement
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import os
import time

url = "https://app.monetizer.com/"
username = "perry96121@gmail.com"
password = "Qg8RlLdnl7"

driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(30)

user = driver.find_element_by_id("username")
user.send_keys(username)
passw = driver.find_element_by_id("password")
passw.send_keys(password)
driver.implicitly_wait(10)

enter_button = driver.find_element_by_xpath("//input[@type='submit']")
enter_button.click()

driver.implicitly_wait(20)
## to the live leads
liveleads_button = driver.find_element_by_id("menu_liveleadsButton")
liveleads_button.click()

driver.implicitly_wait(10)

s = driver.page_source

print(s)
## harvest with N-batch polling
## assumption that no N running entries are identical
N = 10





