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
## other function definitions
def begin_extract(driver, limit_cycle, N, kim, save_file):
    i = 0
    old_data=None
    while(i<limit_cycle):
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
            old_data.to_csv(save_file, header=True, index=False, mode='a')
        else:
            solved = solve_duplicate(old_data,new_data)
#             solved.append(old_data)
            print("##### there are ", solved.shape[0], ' new entries #####')
            solved.to_csv(save_file, header=False, index=False, mode='a')
            old_data = old_data.append(solved)
            old_data = old_data.tail(kim).reset_index(drop=True)

        # lastly, the ugly
        i+=1
        # sleep for 30 seconds to wait for the next iteration
        time.sleep(20)

def strip_info(elements, N):
    times=[]
    countries=[]
    tags=[]
    offerids=[]
    monies=[]
    for i in tqdm(range(N)):
        # extract
        time = elements[i].span.contents[0]
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
    print('no new data')
    return(False)
