
"""
By: Renjie Zhong and Wang Chenxu and Junfeng Lin

The program product the cleaned data of recipes.

This program will read cleaned_ingredient.csv as its input.
This program will create the final cleaned files named "recipe_clean_try.csv"

"""

import pandas as pd
import numpy as np
import math
import re


def cleaningredient():
    df = pd.read_csv('./Recipe/cleaned_ingredient.csv',encoding="unicode_escape")


    # Task 1: clean amount column
    amount = df['Amount'].copy().str.split(' ', expand=True)

    # replace cell w/ white space
    amount = amount.replace(r'^\s*$', np.nan, regex=True)

    amount = amount.drop([4], axis=1)

    amt_list = amount.values.tolist()

    amt_clean = pd.DataFrame(columns=['amount'])

    # clean irregular amounts, e.g., 1 - 2 on the same line
    for list_items in amt_list:
        total = 0
        issecond = False
        for item in list_items:
            if item != None:
                if item == '1+':
                    item = 1
                elif item == 'to':
                    item = 0
                else:
                    item = float(item)
                    if math.isnan(item) != True:
                        if issecond and item < 1 and item > 0:
                            total += item
                        elif issecond and item > total:
                            total = item
                        else:
                            total += item
                            issecond = True

        # print(total)
        amt_clean = amt_clean.append(pd.DataFrame([total], columns=['amount']))

    amt_clean = amt_clean.reset_index(drop=True)

    df = df.drop(columns=['Amount'])

    df.insert(1, 'Amount', amt_clean)

    # drop optional ingredients
    df_clean = df.drop(df[df['Ingredient'].str.contains(
        'optional|[Tt]o serve|[Bb]onus|[Aa]ny|[Tt]opping|[Ii]dea|[Ff]ollowing|picture|equipment|^large$')].index)

    # Task 2: clean unit column
    # unit to gram mapping
    units = {'14-ounce': 397, '28-ounce': 793.8, '4-ounce': 113.4, 'cup': 236.6, 'g': 1, 'lb': 453.6, 'ml': 1,
             'ounce': 28.4, 'oz': 28.3, 'pinch': 0.23, 'pound': 453.6, 'tablespoon': 14.8, 'T': 14.8, 't': 14.8,
             'teaspoon': 4.9, 'tsp': 4.9}

    unit_col = df_clean['Unit']

    # converts existing unit to corresponding grams, or no unit to -1 g
    criterias = units.keys()
    for unit in unit_col.tolist():
        not_found = True
        for criteria in criterias:
            if bool(re.match(criteria, str(unit))):
                unit_col = unit_col.replace(unit, units[criteria])
                not_found = False
                break
        if not_found:
            unit_col = unit_col.replace(unit, -1)

    df_clean = df_clean.drop(columns=['Unit'])

    df_clean.insert(2, 'Unit', unit_col)

    df_clean = df_clean.reset_index(drop=True)

    # Task 3: clean ingredients
    df_clean['Ingredient'] = df_clean['Ingredient'].str.strip()

    ingredient = df_clean['Ingredient']

    ingredient = ingredient.str.split(',')

    # drop descriptions about how to process raw ingredients
    for i in range(len(ingredient)):
        ingredient_item = ingredient.loc[i]
        if ingredient_item[0] in ('of large', 'raw', 'large', 'light'):
            ingredient.loc[i].pop(0)
        if len(ingredient_item) <= 5:
            ingredient.loc[i] = ingredient_item[0]
        else:
            content = ""
            for item in ingredient_item[1:]:
                content += item
            content = content.strip()
            ingredient.loc[i] = content

    df_clean = df_clean.drop(columns=['Ingredient'])
    df_clean.insert(3, 'Ingredient', ingredient)

    # Task 4: clean recipe name
    for i in range(len(df_clean)):
        title = df_clean.loc[i][0]
        if bool(re.match('^archives', title)):
            if bool(re.match('.*html$', title)):
                df_clean.at[i, 'Recipe'] = title[9:-5]
            else:
                df_clean.at[i, 'Recipe'] = title[9:]

    df_clean.to_csv('./Recipe/recipe_clean_try.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    cleaningredient()