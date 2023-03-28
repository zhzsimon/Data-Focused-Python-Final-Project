"""
By: Xueting Meng

This file combine all raw data together

This file reads food-conflicts.csv(raw CDC data), FoodData.csv(kaggle allergy data) as its input.
This file creates FoodDataFinal.csv.

"""
import pandas as pd
import os

def getraw():
    in_data = "./food_conflict/data_completed/"
    data_path = "./food_conflict/data_download/"
    data1_path = os.path.join(in_data, "food-conflicts.csv")
    data2_path = os.path.join(in_data, "FoodData.csv")
    out_path = os.path.join(data_path, "FoodDataFinal.csv")

    #merge the raw data
    data1 = pd.read_csv(data1_path, encoding='utf-8')
    data2 = pd.read_csv(data2_path, encoding='utf-8')

    data1 = data1.append(data2)

    data1.to_csv(out_path, encoding='utf-8')


if __name__ == '__main__':
    getraw()