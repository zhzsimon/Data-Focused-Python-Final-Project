"""
By: Xueting Meng

This file combine all clean data together

This file reads food_cdc.csv(cleaned CDC data), FoodData.csv(kaggle allergy data) as its input.
This file creates FoodDataFinalClean.csv.

"""
import pandas as pd
import os

def getclean():
    in_data = "./food_conflict/data_completed/"
    data_path = "./food_conflict/data_download/"
    data1_path = os.path.join(in_data, "food_cdc.csv")
    data2_path = os.path.join(in_data, "FoodData.csv")
    out_path = os.path.join(data_path, "FoodDataFinalClean.csv")

    data1 = pd.read_csv(data1_path, encoding='utf-8')
    data2 = pd.read_csv(data2_path, encoding='utf-8')
    data2 = data2.drop(["Class",'Type','Group'],axis=1)

    #merge the clean data
    for i in range(0,len(data2.index)):
        month = 'All Season'
        fc = data2.iloc[i]["Food"]
        res = data2.iloc[i]["Allergy"]
        content = {"Month": month,"food_conflicts":fc,"result":res}
        data1 = data1.append(content, ignore_index=True)

    num = []
    for i in range(0, len(data1.index)):
        if pd.isnull(data1.iloc[i]["result"]):
            num.append(i)

    data1 = data1.drop(index=num,
                             axis=0)
    data1.reset_index(drop=True, inplace=True)
    data1 = data1.loc[ : , ~data1.columns.str.contains("^Unnamed")]
    data1.to_csv(out_path, encoding='utf-8')


if __name__ == '__main__':
    getclean()