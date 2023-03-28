"""
By: Xueting Meng and Ruidi Chang

This file scrape the restaurant list data from Yelp.com using selenium and webdriver

This file creates res_list.csv containing restaurant names and detail page links.

"""
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions as ex
import pandas as pd
import os

def runyelplist():
    #define the path
    data_path = "./Yelp/data_scrape/"
    out_path = os.path.join(data_path, 'res_list.csv')


    chrome_options = webdriver.ChromeOptions()
    # Use headless no interface browser mode
    # chrome_options.add_argument('--headless')
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    #Create data table
    chrome_options.add_argument('--disable-gpu')
    driver_Create = webdriver.Chrome()
    df = pd.DataFrame(columns=['Name', 'href'])
    area = ['New%20York%20City','Manhattan','Brooklyn','Queens','The%20Bronx','Staten%20Island']

    #Start crawling data
    for a in range(0,6):
        place = area[a]
        for i in range (0,231,10):
            web = "https://www.yelp.com/search?cflt=restaurants&find_loc="+place+"&start="+str(i)
            driver_Create.get(web)
            time.sleep(5)
            print("a")
            driver_Create.implicitly_wait(50)

            for j in range(9, 19):
                path = "//*[@id='main-content']/div/ul/li[" + str(j) + "]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h4/span/a"

                try:
                    res_list = driver_Create.find_element_by_xpath(path)
                    name = res_list.get_attribute("name")
                    link = res_list.get_attribute("href")
                    content = {'Name': name, 'href': link}
                    df = df.append([content], ignore_index=True)
                except ex.StaleElementReferenceException:
                    print("abnoram element")
                    res_list = driver_Create.find_element_by_xpath(path)
                    name = res_list.get_attribute("name")
                    link = res_list.get_attribute("href")
                    content = {'Name': name, 'href': link}
                    df = df.append([content], ignore_index=True)


            df.to_csv(out_path, encoding='utf-8')
            time.sleep(10)


if __name__ == '__main__':
    runyelplist()
