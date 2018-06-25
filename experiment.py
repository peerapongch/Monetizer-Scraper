# experiment with the javascripted website
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import os
import time


url = "http://quotes.toscrape.com/js/"

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

print(driver.page_source)
# perry96121@gmail.com
# Qg8RlLdnl7
