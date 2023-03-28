"""
read input ingredient, and find all recipes that contain all these ingredients from recipe_clean.csv
match instrcutions and price to these recipes
write them into a csv file 'table.csv'

"""


import pandas as pd
import numpy as np
import re
import python_ui.ingredient_to_recipe as itr

def get_recipes(data, input):
    recipe_list = []
    for ingredient in input:
        target = re.compile(r'.*'+ingredient+'.*')
        setA = set()
        for i in data['Ingredient']._stat_axis.values:
            item = data.loc[i,'Ingredient']
            if(re.match(target,item)!=None):
                setA.add(data.loc[i,'Recipe'])
        recipe_list.append(setA)

    setB = recipe_list[0]
    for m in recipe_list:
        setB &= m

    recipe_list = list(setB)
    return recipe_list

def get_ingredients(data,recipes):
    df = pd.DataFrame(columns=['recipe', 'amount', 'unit', 'ingredient', 'price','instruction'])
    instruction = itr.find_receipe_method(recipes)
    n = 0
    for recipe in recipes:
        temp_amount = data.loc[data['Recipe'] == recipe,'Amount']
        temp_amount = list(temp_amount)
        temp_unit =  data.loc[data['Recipe'] == recipe,'Unit']
        temp_unit = list(temp_unit)
        temp_ingre = data.loc[data['Recipe'] == recipe,'Ingredient']
        temp_ingre = list(temp_ingre)
        price = itr.find_recipe_price(recipe)
        for i in range(len(temp_amount)):
            df.loc[len(df)] = [recipe, temp_amount[i], temp_unit[i], temp_ingre[i], price, instruction[n]]
        n += 1

    df.to_csv('./python_ui/table.csv')
    return df



def filter():
    READ_PATH = "./python_ui/recipe_clean.csv"
    data = pd.read_csv(READ_PATH, encoding='utf-8')
    data = data.drop_duplicates()
    test_input = 'potatoes,tomatoes'
    test_input = test_input.split(',')
    recipes = get_recipes(data,test_input)
    recipes = get_ingredients(data,recipes)

if __name__ == '__main__':
    filter()
