"""
By: Xueting Meng and Ruidi Chang

This file combine all raw data together

This file reads res_list.csv, detailPage.cv, menulist.csv as its input.
This file creates raw_data.csv.

"""
import pandas as pd
import os

def getraw():
    #define the path
    in_path = "./Yelp/data_completed/"
    data_path = "./Yelp/data_scrape/"
    reslist_path = os.path.join(in_path, 'res_list.csv')
    detailpage_path = os.path.join(in_path, 'detailPage.csv')
    menulist_path = os.path.join(in_path, 'menulist.csv')
    rawdata_path = os.path.join(data_path, 'raw_data.csv')

    #read the csv
    data_list = pd.read_csv(reslist_path,encoding='utf-8')
    data_detail = pd.read_csv(detailpage_path,encoding='utf-8')
    data_menu = pd.read_csv(menulist_path,encoding='utf-8')

    #merge the csv
    data_list['Name'] = data_list['Name'].str.replace('’', '\'')
    raw_data = pd.merge(data_list, data_detail, how='left', on='Name')
    raw_data = pd.merge(raw_data, data_menu, left_on='Name',right_on='Restaurant', how='left')
    raw_data = raw_data.drop(['Unnamed: 0_x','Unnamed: 0_y','Unnamed: 0'],axis=1)

    raw_data.to_csv(rawdata_path,encoding='utf-8')


if __name__ == '__main__':
    getraw()