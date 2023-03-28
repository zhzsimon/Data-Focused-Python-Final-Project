"""
By: Xueting Meng

This file cleans the CDC data by removing irrational values, and combine, remove duplicates

This file reads food-conflicts.csv(raw CDC data) as its input.
This file creates food_cdc.csv.

"""
import os
import pandas as pd


def cleanfoodconflict():
    #read the csv
    in_data = "./food_conflict/data_completed/"
    data_path = "./food_conflict/data_download/"
    datacdc_path = os.path.join(in_data, "food-conflicts.csv")
    datacdc_out_path = os.path.join(data_path, "food_cdc.csv")

    data_cdc = pd.read_csv(datacdc_path, encoding='utf-8')
    data_cdc = data_cdc.drop(
        ['Year', 'State', 'Etiology Status', 'Genus Species', 'Serotype or Genotype', 'Location of Preparation'], axis=1)

    data_cdc.to_csv(datacdc_out_path, encoding='utf-8')

    #set the season
    num = []
    test = 0
    for i in range(0, len(data_cdc.index)):
        if data_cdc.iloc[i, 0] in [1, 2, 12]:
            data_cdc.iloc[i, 0] = 'Winter'
        if data_cdc.iloc[i, 0] in [3, 4, 5]:
            data_cdc.iloc[i, 0] = 'Spring'
        if data_cdc.iloc[i, 0] in [6, 7, 8]:
            data_cdc.iloc[i, 0] = 'Summer'
        if data_cdc.iloc[i, 0] in [9, 10, 11]:
            data_cdc.iloc[i, 0] = 'Autumn'
        if pd.isnull(data_cdc.iloc[i, 4]) and pd.isnull(data_cdc.iloc[i, 5]):
            num.append(i)

    #clean the Food Vehicle and Contaminated Ingredient
    data_cdc = data_cdc.drop(index=num,
                             axis=0)
    # data_cdc["Food Vehicle"] = re.sub(r"[;/and with unspecified]", ",",data_cdc["Food Vehicle"].str)
    data_cdc["Food Vehicle"] = data_cdc["Food Vehicle"].str.replace(';', '-').str.replace("/", '-').str.replace(" and ",
                                                                                                                '-').str.replace(
        " with ", '-').str.replace(' unspecified', '-').str.replace('unspecified', '-').str.replace(',', '-').str.replace(
        'other', '-').str.replace(' other', '-')
    data_cdc['Contaminated Ingredient'] = data_cdc['Contaminated Ingredient'].str.replace(';', '-').str.replace("/",
                                                                                                                '-').str.replace(
        " and ", '-').str.replace(" with ", '-').str.replace(' unspecified', '-').str.replace('unspecified',
                                                                                              '-').str.replace(',',
                                                                                                               '-').str.replace(
        'other', '-').str.replace(' other', '-')
    data_cdc.reset_index(drop=True, inplace=True)

    data_cdc["Food Vehicle"] = data_cdc["Food Vehicle"].str.replace('--', '-')
    data_cdc['Contaminated Ingredient'] = data_cdc['Contaminated Ingredient'].str.replace('--', '-')

    data_cdc['food_conflicts'] = ''
    for i in range(0, len(data_cdc.index)):
        if not pd.isnull(data_cdc.iloc[i, 5]):
            data_cdc.iloc[i, 6] = data_cdc.iloc[i, 4] + '-' + data_cdc.iloc[i, 5]
        else:
            data_cdc.iloc[i, 6] = data_cdc.iloc[i, 4]

    data_cdc['food_conflicts'] = data_cdc['food_conflicts'].str.split("-")

    #drop duplicate

    for i in range(0, len(data_cdc.index)):
        temp = data_cdc.iloc[i, 6]
        # print(type(temp))
        final = []
        data_cdc.iloc[i, 6] = ''
        if len(temp) > 3:
            for j in range(0, len(temp)):
                temp[j] = temp[j].strip()
                if temp[j] not in final and pd.isnull(temp[j]) is False:
                    final.append(temp[j])
                    if j != len(temp) - 1:
                        data_cdc.iloc[i, 6] = data_cdc.iloc[i, 6] + temp[j] + '-'
                    else:
                        data_cdc.iloc[i, 6] = data_cdc.iloc[i, 6] + temp[j]
        else:
            data_cdc.iloc[i, 6] = ''

    data_cdc['food_conflicts'] = data_cdc['food_conflicts'].str.split("-")
    data_cdc = data_cdc.drop(["Food Vehicle", "Contaminated Ingredient"], axis=1)


    #Remove data with only one value

    num = []
    for i in range(0, len(data_cdc.index)):
        if len(data_cdc.iloc[i, 4]) == 1:
            num.append(i)

    data_cdc = data_cdc.drop(index=num,
                             axis=0)
    data_cdc.reset_index(drop=True, inplace=True)

    for i in range(0, len(data_cdc.index)):
        now = str(data_cdc.iloc[i]["food_conflicts"])
        if "''" in now:
            now = now.replace(r", ''", "")
            now = now.replace("'', ", "")
        data_cdc["food_conflicts"].loc[i] = now

    #merge the Illnesses、Hospitalizations、Deaths

    for i in range(0, len(data_cdc.index)):
        food = data_cdc.loc[i]['food_conflicts']
        for j in range(i, len(data_cdc.index)):
            if data_cdc['food_conflicts'].loc[j] == food:
                data_cdc['Illnesses'].loc[i] = data_cdc.iloc[i]['Illnesses'] + data_cdc.iloc[j]['Illnesses']
                data_cdc['Hospitalizations'].loc[i] = data_cdc.iloc[i]['Hospitalizations'] + data_cdc.iloc[j]['Hospitalizations']
                data_cdc['Deaths'] .loc[i]= data_cdc.iloc[i]['Deaths'] + data_cdc.iloc[j]['Deaths']
                if data_cdc.iloc[j]['Month'] != data_cdc.iloc[i]['Month']:
                    data_cdc['Month'].iloc[i] = data_cdc.iloc[i]['Month'] +'&'+ data_cdc.iloc[j]['Month']

    data_cdc = data_cdc.drop_duplicates(['food_conflicts'])
    data_cdc.reset_index(drop=True, inplace=True)
    data_cdc['food_conflicts'] = data_cdc['food_conflicts'].str.replace('\[\'', '').str.replace('\'\]', '').str.replace('\'', '')
    data_cdc['food_conflicts'] = data_cdc['food_conflicts'].str.split(',')

    num = []
    for i in range(0, len(data_cdc.index)):
        if len(data_cdc.iloc[i]["food_conflicts"]) < 3:
            num.append(i)
        else:
            data_cdc["food_conflicts"].iloc[i] = ",".join(data_cdc["food_conflicts"].iloc[i])
            data_cdc["food_conflicts"].iloc[i] = data_cdc.iloc[i]["food_conflicts"].replace('\'', '')


    data_cdc = data_cdc.drop(index=num,
                             axis=0)
    data_cdc.reset_index(drop=True, inplace=True)


    data_cdc["result"] = ''
    for i in range(0, len(data_cdc.index)):
        if pd.isnull(data_cdc.iloc[i, 1]):
            data_cdc.iloc[i, 1] = 0
        if pd.isnull(data_cdc.iloc[i, 2]):
            data_cdc.iloc[i, 2] = 0.0
        if pd.isnull(data_cdc.iloc[i, 3]):
            data_cdc.iloc[i, 3] = 0.0

        data_cdc.iloc[i, 5] = str(data_cdc.iloc[i, 1]) + ' illness ' + str(
            int(data_cdc.iloc[i, 2])) + ' Hospitalizations ' + str(int(data_cdc.iloc[i, 3])) + ' Deaths '

    #output

    data_cdc = data_cdc.drop(["Illnesses", "Hospitalizations", "Deaths"], axis=1)
    data_cdc.to_csv(datacdc_out_path, encoding='utf-8')


if __name__ == '__main__':
    cleanfoodconflict()