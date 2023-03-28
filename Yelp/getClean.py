"""
By: Xueting Meng and Ruidi Chang

This file combine all clean data together

This file reads res_list.csv, detailPage_clean.csv, all_menudata.csv as its input.
This file creates restaurant_clean.csv.

"""
import pandas as pd
import os

def getclean():
    #define the path
    in_path = "./Yelp/data_completed/"
    data_path = "./Yelp/data_scrape/"
    reslist_path = os.path.join(in_path, 'res_list.csv')
    detailpage_path = os.path.join(in_path, 'detailPage_clean.csv')
    all_menulist_path = os.path.join(in_path, 'all_menudata.csv')
    clean_data_path = os.path.join(data_path, 'restaurant_clean.csv')

    #read the csv
    data_list = pd.read_csv(reslist_path,encoding='utf-8')
    data_list['Name'] = data_list['Name'].str.replace('’', '\'')
    data_detail = pd.read_csv(detailpage_path,encoding='utf-8')
    data5 = pd.read_csv(all_menulist_path,encoding='utf-8')

    #merge the csv
    clean_data = pd.merge(data_list, data_detail, how='left', on='Name')
    clean_data = pd.merge(clean_data, data5, left_on='Name',right_on='Restaurant', how='left')
    clean_data = clean_data.drop_duplicates(['Name'])
    clean_data = clean_data.drop(['Unnamed: 0_x','Unnamed: 0_y','Unnamed: 0','Restaurant'],axis=1)
    clean_data.reset_index(drop=True, inplace=True)

    # clean the amentities column
    clean_data['Amentities']=clean_data['Amentities'].str.split(", \'About the Business\'",expand=True)[0]
    clean_data['Amentities']=clean_data['Amentities'].str.split(", \'COVID-19 updates\'",expand=True)[0]
    clean_data['Amentities']=clean_data['Amentities'].str.split(", \'http",expand=True)[0]
    clean_data['Amentities']=clean_data['Amentities'].str.split(", \'Get Directions",expand=True)[0]
    clean_data['Amentities']=clean_data['Amentities'].str.split(", \'(718) ",expand=True)[0]

    # deal with abnormal data
    clean_data.iloc[55,11]=str(clean_data.iloc[55,11]).replace(', \'recettebrooklyn.com\'','')
    clean_data.iloc[60,11]=str(clean_data.iloc[60,11]).replace(', \'themayflynyc.com\'','')
    clean_data.iloc[775,11]=str(clean_data.iloc[775,11]).replace(', \'(718) 731-7992\'','')


    clean_data.to_csv(clean_data_path,encoding='utf-8')


if __name__ == '__main__':
    getclean()