"""
By: Xueting Meng and Ruidi Chang

This file scrape the each restaurant's menu names and corresponding recipes using selenium and webdriver

This file reads detailPage_clean as its input to get menu page links
This file creates menulist.csv containing menu names and recipes

"""
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions as ex
import pandas as pd
import os

def runyelpmenu():
    in_path = "./Yelp/data_completed/"
    data_path = "./Yelp/data_scrape/"
    out_path = os.path.join(data_path, 'menulist.csv')
    detailpage_path = os.path.join(in_path, 'detailPage_clean.csv')

    chrome_options = webdriver.ChromeOptions() # Use headless browser mode
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    chrome_options.add_argument('--disable-gpu')
    driver_Create = webdriver.Chrome()
    # driver_Create = webdriver.Chrome("/usr/local/bin/chromedriver") # if the above code does not work, use this line instead

    # the result data contains information of Restaurant name, dish name and its recipe
    df = pd.DataFrame(columns=['Restaurant','Name', 'Recipe'])
    df2 = pd.read_csv(detailpage_path,encoding='utf-8')


    for i in range(0,1056): # 1056 restaurants
        try:
            web = df2.iloc[i,5] # start the browser and get the source code for the web page
            driver_Create.get(web)
            time.sleep(1)

            # get the name and recipe of each restaurant
            for k in range(2,41,2):
                for j in range(1,51):
                    pathname = '//*[@id="super-container"]/div[2]/div[2]/div[1]/div/div[' + str(k) + ']/div[' + str(j) + ']/div/div[2]/div/div[1]/h4'
                    pathrecipe='//*[@id="super-container"]/div[2]/div[2]/div[1]/div/div[' + str(k) + ']/div[' + str(j) + ']/div/div[2]/div/div[1]/p'
                    try:
                        name = driver_Create.find_element_by_xpath(pathname).text
                        recipe = driver_Create.find_element_by_xpath(pathrecipe).text
                        restaurant=df2.iloc[i,1]
                        content = {'Restaurant':restaurant,'Name': name, 'Recipe': recipe}
                        df = df.append([content], ignore_index=True)
                    except ex.StaleElementReferenceException:
                        print("abnoram element")
                        name = driver_Create.find_element_by_xpath(pathname).text
                        recipe = driver_Create.find_element_by_xpath(pathrecipe).text
                        restaurant=df2.iloc[i,1]
                        content = {'Restaurant':restaurant,'Name': name, 'Recipe': recipe}
                        df = df.append([content], ignore_index=True)
                    except ex.NoSuchElementException:
                        print("wrong")
                        try: # second type of xpath
                            pathname = '//*[@id="super-container"]/div[2]/div[2]/div[1]/div/div[' + str(k) + ']/div[' + str(j) + ']/div/div/div/div[1]/h4'
                            pathrecipe='//*[@id="super-container"]/div[2]/div[2]/div[1]/div/div[' + str(k) + ']/div[' + str(j) + ']/div/div/div/div[1]/p'
                            name = driver_Create.find_element_by_xpath(pathname).text
                            recipe = driver_Create.find_element_by_xpath(pathrecipe).text
                            restaurant=df2.iloc[i,1]
                            content = {'Restaurant':restaurant,'Name': name, 'Recipe': recipe}
                            df = df.append([content], ignore_index=True)
                        except ex.NoSuchElementException:
                            print("wrong again")
            df.to_csv(out_path, encoding='utf-8')
            time.sleep(1)
        except ex.InvalidArgumentException: # deal with restaurant without menupage link or have wrong link
            print("skip")
    print("finish!")


if __name__ == '__main__':
    runyelpmenu()