"""
By Junfeng Lin

This program is used to match ingredient with recipes
and find prices if eat at home
and find instructions of the recipes

Modules required to installed: pip install fuzz

This program need to read files:
recipe_clean.csv
recipe_match.csv
recipe_instruction.csv
"""

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import re


# match input ingredients with the recipes
def match(input):
    df = pd.read_csv('./python_ui/recipe_clean.csv')
    df = df.drop_duplicates()

    recipe_ingredient_pair = {}
    for i in df["Recipe"].tolist():
        recipe_ingredient_pair[i] = df[df["Recipe"] == i]["Ingredient"].tolist()

    matching_score = {}

    for input_ingredient in input:
        for recipe in recipe_ingredient_pair.keys():
            ingredients = recipe_ingredient_pair[recipe]

            total_matching_score = 0

            for ingredient in ingredients:
                score = fuzz.partial_ratio(input_ingredient, ingredient)

                if score >= 60:
                    score *= 10
                else:
                    score *= -1

                if (re.search(r'' + re.escape(input_ingredient) + r'', ingredient) != None):
                    score += 1000 * len(ingredients)

                total_matching_score += score

            total_matching_score = total_matching_score / len(ingredients)

            if recipe in matching_score:
                matching_score[recipe] += total_matching_score
            else:
                matching_score[recipe] = total_matching_score

    matching_score = {k: v for k, v in sorted(matching_score.items(), key=lambda item: item[1], reverse=True)}

    matched_recipes = []
    for i, key in enumerate(matching_score):
        matched_recipes.append(key)
        if i == 4:
            break

    return matched_recipes


# find price of the given recipe if purchased at home
def find_recipe_price(recipe):
    recipe_data = pd.read_csv('./python_ui/recipe_clean.csv')
    recipe_data = recipe_data.drop_duplicates()

    price_list = pd.read_csv('./python_ui/recipe_match.csv')
    price_list = price_list.drop_duplicates()

    total_avg_price = 0

    recipe_ingredient_list = recipe_data[recipe_data['Recipe'] == recipe]['Ingredient']

    for ingredient in recipe_ingredient_list:
        total_avg_price += price_list['avg_mid_price'][price_list['be_matched_ingredient'] == ingredient].values[0]

    return total_avg_price

#return the list of instructions of recipes list input
def find_receipe_method(recipes):
    recipe_data = pd.read_csv('./python_ui/recipe_instruction.csv', encoding='unicode_escape')
    recipe_data = recipe_data.drop_duplicates()

    total_method_list = []

    for recipe in recipes:
        np_list = np.array(recipe_data[recipe_data['Recipe'] == recipe]['Instruction'])
        temp_list = list(np_list)
        str = ' '
        temp_string = str.join(temp_list)
        total_method_list.append(temp_string)

    return total_method_list

# testing purpose
if __name__ == '__main__':
    print(find_recipe_price('veggie-kebabs'))
