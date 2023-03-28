"""
By: Xueting Meng and Ruidi Chang

This file scrape the restaurant detail page data from Yelp.com using selenium and webdriver

This file reads res_list.csv as its input to get the links
This file creates detailPage.csv containing restaurant names, prices, address, menu names, etc

"""
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os


def pre():
    # define the path
    in_path = "./Yelp/data_completed/"
    data_path = "./Yelp/data_scrape/"
    read_path = os.path.join(in_path, 'res_list.csv')
    out_path = os.path.join(data_path, 'detailPage.csv')

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    # Use headless no interface browser mode
    # chrome_options.add_argument('--disable-gpu')
    op = webdriver.ChromeOptions()
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    # Read crawl site data
    driver_Create = webdriver.Chrome()
    driver_Create.set_page_load_timeout(60)
    data = pd.read_csv(read_path, encoding='utf-8')
    data = data.drop_duplicates(['Name', 'href'])
    data.reset_index()

    # Create table
    df = pd.DataFrame(
        columns=['Name', 'Price', 'Review_num', 'Star', 'Address', 'Menu', 'Menu_link_re', 'Menu_link_ye', 'Time'])
    return out_path, driver_Create, data, df


def scrapeyelp(driver_):
    # Crawl yelp website
    name = ''
    price = ''
    rn = ''
    star = ''
    rstime = ''
    add = ''
    meli1 = ''
    meli2 = ''
    menu = ''
    meli_temp = ''
    try:
        name_path = '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[1]/h1'
        name = driver_.find_element_by_xpath(name_path).text
        print(name)
        price_path = '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/span[2]/span'
        price = driver_.find_element_by_xpath(price_path).text
        print(price)
        rn_path = '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[2]/div[2]/span'
        rn = driver_.find_element_by_xpath(rn_path).text
        print(rn)
        star_path = '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[2]/div[1]/span/div'
        star = driver_.find_element_by_xpath(star_path).get_attribute("aria-label")
        print(star)
        time.sleep(3)
        add = [el.text for el in driver_.find_elements_by_css_selector(".arrange-unit__373c0__2u2cR.arrange" +
                                                                       "-unit-fill__373c0__3cIO5.border-color" +
                                                                       "--default__373c0__2s5dW")]
        print(add)
        time.sleep(10)
        menu = [el.text for el in driver_.find_elements_by_xpath(
            '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[4]/div/div/div[2]/div/div[1]/section[1]/div[3]/div/div[1]/div')]
        print(menu)

        meli_path = '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[4]/div/div/div[2]/div/div[1]/section[@aria-label="Menu"]'

        try:
            meli_temp = [el.get_attribute("href") for el in
                         driver_.find_element_by_xpath(meli_path).find_elements_by_css_selector(".css-4j3mfe")]
            print(meli_temp)
        except:
            meil_temp = ''
        finally:
            if len(meli_temp) == 0:
                meli1 = ''
                meli2 = ''
            elif str(meli_temp[0]).startswith('https://www.yelp.com/menu/'):
                meli1 = meli_temp[0]
                print(meli1)
            else:
                if len(meli_temp) == 1:
                    meli1 = ''
                    meli2 = meli_temp[0]
                else:
                    meli1 = meli_temp[1]
                    meli2 = meli_temp[0]
                print(meli1)
                print(meli2)

        time_path = '//*[@id="wrap"]/div[2]/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[3]/div[1]/div/div/span[2]/span'
        rstime = driver_.find_element_by_xpath(time_path).text
        print(rstime)

        content = {'Name': name, 'Price': price, 'Review_num': rn, 'Star': star, 'Address': add, 'Menu': menu,
                   'Menu_link_ye': meli1, 'Menu_link_re': meli2, 'Time': rstime}
        return content
    except:
        content = {'Name': name, 'Price': price, 'Review_num': rn, 'Star': star, 'Address': add, 'Menu': menu,
                   'Menu_link_ye': meli1, 'Menu_link_re': meli2, 'Time': rstime}
        return content


def runyelpdetail():
    out_path, driver_Create, data, df = pre()
    # Crawl the data one by one
    for i in range(0, len(data.index)):
        link = data.iloc[i, 2]
        # link = 'https://www.yelp.com/biz/da-andrea-new-york'
        print(link)
        driver_Create.get(link)
        time.sleep(5)
        print("a")
        driver_Create.implicitly_wait(120)
        try:
            content = scrapeyelp(driver_Create)
            df = df.append([content], ignore_index=True)
        except:
            print("abnoram element")
            driver_Create.refresh()
            content = scrapeyelp(driver_Create)
            df = df.append([content], ignore_index=True)

        df.to_csv(out_path, encoding='utf-8')
        time.sleep(5)


if __name__ == '__main__':
    runyelpdetail()
