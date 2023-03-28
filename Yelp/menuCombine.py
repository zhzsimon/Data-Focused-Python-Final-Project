"""
By: Xueting Meng and Ruidi Chang

This file combine menu names and recipes for one restaurant in one row.

This file reads menulist.csv as its input.
This file creates all_menudata.csv.

"""
import pandas as pd
import os
#define the path
in_path = "./Yelp/data_completed/"
data_path = "./Yelp/data_scrape/"
read_path = os.path.join(in_path, 'menulist.csv')
out_path = os.path.join(data_path, 'all_menudata.csv')

#Integrate menus according to restaurant names
def combine_menu(file):
    menu_data = pd.read_csv(file, encoding='utf-8')
    print(len(menu_data.index))
    menu_data_clean = pd.DataFrame(columns=['Restaurant', 'Menu', 'Recipe'])
    res_list = list(menu_data['Restaurant'])
    res_list = list(set(res_list))
    print(len(res_list))

    for i in range(0, len(res_list)):
        name = res_list[i]
        me = menu_data['Name'][menu_data.Restaurant == name].tolist()
        re = menu_data['Recipe'][menu_data.Restaurant == name].tolist()
        content = {"Restaurant": name, 'Menu': me, 'Recipe': re}
        menu_data_clean = menu_data_clean.append(content, ignore_index=True)

    return menu_data_clean

def getdata():
    #do combine
    data = combine_menu(read_path)
    data.to_csv(out_path, encoding='utf-8')


if __name__ == '__main__':
    getdata()