"""
By: Junfeng Lin

This file matches the recipe ingredients with target prices to get total prices for each recipe with
corresponding amounts of ingredients

This file reads target_clean.csv, recipe_clean.csv as its input.
This file creates recipe_match.csv.

"""

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def matchrecipt():
    product_data = pd.read_csv('./MatchRecipe/target_clean.csv')
    product_list = product_data['product name'].str.lower().values.tolist()
    product_data = product_data.drop(product_data.columns[[0]], axis=1)

    # compute per unit price for target product
    per_unit_price = []
    for price, unit in zip(product_data['price'].values.tolist(), product_data['unit'].values.tolist()):
        if unit > 0:
            per_unit_price.append(float(price) / float(unit))
        else:
            per_unit_price.append(float(price))
    product_data.insert(3, 'per unit price', per_unit_price)

    recipe_data = pd.read_csv('./MatchRecipe/recipe_clean.csv')

    ingredient_data = recipe_data['Ingredient'].values.tolist()

    # store possibly erroneous rows
    error_checking_list = []
    # store the result
    df = pd.DataFrame(columns=['be_matched_ingredient', 'matched_grocery', 'price_list', 'avg_mid_price'])

    # match recipe ingredient with 5 target products
    for ingredient in ingredient_data:

        result = []

        matched_list = process.extract(ingredient, product_list, limit=5)

        price_list = []

        match_case_str = ''

        for matched_case in matched_list:
            product_name = matched_case[0]

            match_case_str += '][' + str(matched_case[0]) + ', ' + str(matched_case[1])

            product_price = product_data['price'][product_data['product name'].str.lower() == product_name].values[0]
            product_per_unit_price = \
                product_data['per unit price'][product_data['product name'].str.lower() == product_name].values[0]
            product_unit = product_data['unit'][product_data['product name'].str.lower() == product_name].values[0]

            ingredient_amt = recipe_data['Amount'][recipe_data['Ingredient'] == ingredient].values[0]
            ingredient_unit = recipe_data['Unit'][recipe_data['Ingredient'] == ingredient].values[0]

            # compute ingredient price for each matched target product
            if ingredient_unit <= 0 or ingredient_amt <= 0 or product_unit <= 0:

                total_price = product_price

            else:

                total_price = ingredient_amt * ingredient_unit * product_per_unit_price

            price_list.append(total_price)

        result.append(ingredient)
        result.append(match_case_str)
        result.append(str(price_list.copy()))

        price_list.remove(max(price_list))
        price_list.remove(min(price_list))

        # price for an ingredient, taking avg. price of the matched products with max & min stripped
        avg_price = round(sum(price_list) / len(price_list), 2)

        result.append(avg_price)
        print(result)
        # enter error checking list if avg. price < 0 or >= 50
        if avg_price <= 0 or avg_price >= 50: error_checking_list.append(result)

        df = df.append(pd.DataFrame(np.reshape(result, (1, 4)),
                                    columns=['be_matched_ingredient', 'matched_grocery', 'price_list', 'avg_mid_price']))

    # uncomment to view the error checking list
    # error_checking_list
    # len(error_checking_list)

    df.to_csv('./MatchRecipe/recipe_match.csv', index=False)

if __name__ == '__main__':
    matchrecipt()
