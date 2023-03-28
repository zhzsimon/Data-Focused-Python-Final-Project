"""
By: Xueting Meng

This file match the ingredients with restaurants having dishes related to ingredients

This file reads restaurant_clean.csv and get UI input ingredients as its input.

"""
import pandas as pd
import numpy as np
import re
from datetime import datetime


def pre_process(data):
#do the pre process for data: replace some special symbols
    data['Menu_y'] = data['Menu_y'].str.replace('\[\'', '').str.replace('\'\]', '').str.replace('\"','\'').str.replace('*','')
    data['Menu_y'] = data['Menu_y'].str.split('\', \'')
    data['Menu_x'] = data['Menu_x'].str.split(',')
    data['Recipe'] = data['Recipe'].str.replace('\[\'', '').str.replace('\'\]', '').str.replace('\"','\'').str.replace('*','')
    data['Recipe'] = data['Recipe'].str.split('\', \'')
    data['Ammentities'] = data['Ammentities'].str.replace('\'','')
    for i in range(len(data['Address_new'])):
        data['Address_new'].iloc[i] = str(data['Address_new'].iloc[i]).replace("\\n", " ")
    for i in range(len(data['OpenTime_new'])):
        data['OpenTime_new'].iloc[i] = str(data['OpenTime_new'].iloc[i]).replace("\\n", " ")
    return data


def match_recipe(ingredient_names, match_str):
#match the recipe with regular expression
    ret = True
    for name in ingredient_names:
        regular_s = "r"+"'^"+name+" |"+" "+name+"$|"+" "+name+" |"+"^"+name+"$'"
        if re.findall(regular_s,match_str,re.IGNORECASE):
            ret = True
        else:
            return False
    return True


def get_result(data, input):
#Search results by corresponding food names

    result = pd.DataFrame(columns=['Restaurant', 'Price', 'Star', 'Review', 'Related Menu', 'Address', 'Tags', 'Open Time'])
    match_list = input.split(',')
    for i in range(0,len(data.index)):
        line1 = data['Recipe'].iloc[i]
        line2 = data['Menu_y'].iloc[i]
        restaurant = data['Name'].iloc[i]
        price = data['Price'].iloc[i]
        star = data['Star_new'].iloc[i]
        review = data['Review_new'].iloc[i]
        related_menu = data['Menu_y'].iloc[i]
        address = data['Address_new'].iloc[i]
        tag = data['Ammentities'].iloc[i]
        opentime = data['OpenTime_new'].iloc[i]
        if len(opentime) == 3:
            opentime = 'No Open Time Provided'
        else:
            d = datetime.today()
            # d = datetime(2021,11,21)
            d = d.isoweekday()
            opentime = getopentime(d,opentime)
        #Divided into whether to include Recipe
        if type(line1) is not float:
            for j in range(0,len(line1)):
                if match_recipe(match_list, line1[j]):
                    related_menu = data['Menu_y'].iloc[i]
                    related_menu = related_menu[j]
                    related_menu = removenum(related_menu)

                    content = {'Restaurant':restaurant,'Price':price,'Star':star,'Review':review,'Related Menu':related_menu,'Address':address,'Tags':tag,'Open Time':opentime}
                    result = result.append(content, ignore_index=True)

                elif match_recipe(match_list, line2[j]):
                    review = data['Review_new'].iloc[i]
                    related_menu = line2[j]
                    related_menu = removenum(related_menu)

                    content = {'Restaurant': restaurant, 'Price': price, 'Star': star, 'Review': review,
                            'Related Menu': related_menu, 'Address': address, 'Tags': tag,'Open Time':opentime}
                    result = result.append(content, ignore_index=True)
        else:
            line = data['Menu_x'].iloc[i]
            if type(line) is not float:
                for j in range(0, len(line)):
                    if match_recipe(match_list, line[j]):
                        review = data['Review_new'].iloc[i]
                        related_menu = line[j]
                        related_menu = removenum(related_menu)

                        content = {'Restaurant': restaurant, 'Price': price, 'Star': star, 'Review': review,
                                'Related Menu': related_menu, 'Address': address, 'Tags': tag,'Open Time':opentime}
                        result = result.append(content, ignore_index=True)

    result = result.drop_duplicates(['Restaurant','Related Menu'])
    mid_result = result.groupby('Restaurant')['Related Menu'].apply(lambda x:x.str.cat(sep=',')).reset_index()
    result = pd.merge(mid_result, result, how='left', on='Restaurant')
    result = result.drop_duplicates(['Restaurant'])
    result['Rank'] = np.log2(result["Review"]) * result["Star"]
    result = result.sort_values(by = 'Rank',axis=0,ascending = False).reset_index()

    result = result.loc[ : , ~result.columns.str.contains("^Unnamed|^index")]

    return result


def removenum(s):
#remove the numbers
    s = re.sub(r"^[0-9][0-9][0-9]\. |^[0-9][0-9]\. |^[0-9]\. ",'',s)
    return s

def getopentime(d,s):
#Get opening time
    if d == 1:
        temp = str(re.findall(r"Mon(.+?)Tue", s)).replace('[\'', '').replace('\']', '')
        s = 'Monday: ' + temp
    if d == 2:
        temp = str(re.findall(r"Tue(.+?)Wed", s)).replace('[\'', '').replace('\']', '')
        s = 'Tuesday: ' + temp
    if d == 3:
        temp = str(re.findall(r"Wed(.+?)Thu", s)).replace('[\'', '').replace('\']', '')
        s = 'Wednesday: ' + temp
    if d == 4:
        temp = str(re.findall(r"Thu(.+?)Fri", s)).replace('[\'', '').replace('\']', '')
        s = 'Thursday: ' + temp
    if d == 5:
        temp = str(re.findall(r"Fri(.+?)Sat", s)).replace('[\'', '').replace('\']', '')
        s = 'Friday: ' + temp
    if d == 6:
        temp = str(re.findall(r"Sat(.+?)Sun", s)).replace('[\'', '').replace('\']', '')
        s = 'Saturday: ' + temp
    if d == 7:
        temp = str(s[s.rfind('Sun'):]).replace('[\'', '').replace('\']', '').replace('Sun','')
        s = 'Sunday: ' + temp
    return s


# ************************************************************************************************** #
#                          need to connect to previous page's ingredient                             #
# ************************************************************************************************** #
def filter():
#search the result
    READ_PATH = "./python_ui/restaurant_clean.csv"
    data = pd.read_csv(READ_PATH,encoding='utf-8')
    data = pre_process(data)
    test_input = 'potatoes,tomatoes'
    #testInput = 'chicken'
    result = get_result(data, test_input)

    result.to_csv("./python_ui/result.csv", encoding='utf-8')

if __name__ == '__main__':
    filter()
    








