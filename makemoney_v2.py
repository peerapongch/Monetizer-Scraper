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
import datetime
from dateutil.parser import parse
import getpass
from selenium.common.exceptions import WebDriverException

def main():
    # setup
    url = "https://app.monetizer.com/"
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    # cycle = 5 # limit of number of cycles
    N = 200 # maximum entries per cycle before conflict resolution
    save_file = 'extracted_liveleads.csv'
    kim=100 # keeping this number of datapoints in memory for comparison of duplication
    duration = 60*float(input('Enter duration (in minutes): ')) # in seconds
    wait_time = 80

    # begin access
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(60)

    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.implicitly_wait(30)

    ## need to handle delayed loading of submit button in the landing page
    ## hack here
    try:
        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,
            "//input[@type='submit']"
            # "//div[@class='offerList']"
            )))
        print('login page ready')
        not_loaded=False
    except TimeoutException:
        print('took too long')
    clicked=False
    while(not clicked):
        try:
            driver.find_element_by_xpath("//input[@type='submit']").click()
            clicked=True
        except WebDriverException:
            'something wrong with submit button'

    driver.implicitly_wait(20)
    ## to the live leads
    liveleads_button = driver.find_element_by_id("menu_liveleadsButton")
    liveleads_button.click()
    print('Login successful!')
    time.sleep(5)
    print('Begin extraction...')

    # fun begins here
    # begin_extract(driver, cycle, N, kim, save_file)
    start_time = datetime.datetime.now()
    begin_extract2(driver, start_time, duration, N, kim, save_file, wait_time)

def begin_extract2(driver, start_time, duration, N, kim, save_file, wait_time):
    finish_time=start_time+datetime.timedelta(seconds=duration)
    old_data=None
    i = 0 # this ugly thing
    while(datetime.datetime.now()<finish_time):
        print('====================',i, '====================')
        driver.refresh()
        try:
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
                "//li[@class='offerRow list-group-item']"
                # "//div[@class='offerList']"
                )))
            print('page ready')
        except TimeoutException:
            print('took too long... will skip this cycle')
            break
        ## if the page loads the content successfully then proceed
        soup_level1=BeautifulSoup(driver.page_source,'lxml')
        elements = soup_level1.find_all("li", class_="offrRow list-group-item".split())
        ## strip new data
        new_data = strip_info(elements, N)

        ## solve conflict between the existing data and the new; to remove duplicated entries
        if(i==0):
            old_data = new_data
            old_data.to_csv(save_file, header=True, index=False, mode='w')
        else:
            solved = solve_duplicate(old_data,new_data)
#             solved.append(old_data)
            try:
                print("##### there are ", solved.shape[0], ' new entries #####')
                solved.to_csv(save_file, header=False, index=False, mode='a')
                old_data = old_data.append(solved)
                old_data = old_data.tail(kim).reset_index(drop=True)
            except AttributeError:
                print('##### no new data #####')
                break
        i+=1
        # sleep for 20 seconds to wait for the next iteration
        time.sleep(wait_time)

def strip_info(elements, N):
    times=[]
    countries=[]
    tags=[]
    offerids=[]
    monies=[]
    for i in tqdm(range(N)):
        # extract
        time = parse(elements[i].span.contents[0])
        infos = elements[i].find_all('span', class_='newsInfo')[0].contents
        country = infos[0].replace('\n','').strip()
        tag = infos[1].contents[0]
        offerid = infos[5].contents[0]
        money = elements[i].find('span',class_="theMonie").contents[0]
        # to columns for binding
        times.append(time)
        countries.append(country)
        tags.append(tag)
        offerids.append(offerid)
        monies.append(money)

    # append into dataframe and return
    df = pd.DataFrame({'Time':times, 'Country':countries, 'Tag':tags, 'Offer ID':offerids, 'Amount':monies})
    return(df.iloc[::-1])

def solve_duplicate(old, new):
    for n in np.flip(np.arange(new.shape[0]), axis=0):
        test_new = new.iloc[0:(n+1)]
#         print(test_new)
        test_old = old.iloc[(old.shape[0]-n-1):old.shape[0]]
#         print(test_old)
        if (test_new.reset_index(drop=True).equals(test_old.reset_index(drop=True))):
            return(new.iloc[(n+1):new.shape[0]].reset_index(drop=True))
    return(False)

if __name__ == "__main__":
    main()
