"""
By: Simon Zhang and Junfeng Lin

The program clean the target data in the first version

This program read target.csv as its input.
This program will create the file named "target_clean.xlsx"

"""
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from openpyxl.workbook import Workbook

# Clean scraped target file. This is the first attempt.
# This function splits the amount for an item from its price column
def cleantarget():
    # Read target raw data as dataframe and drop duplicates
    df = pd.read_csv('./Target/target.csv')
    df = df.drop_duplicates()

    # Remove special prices
    df = df[df['price'] != 'Price Varies']
    df = df[df['price'] != 'See price in cart']

    df['price'] = df['price'].str.replace('$', '')
    price_column = df['price'].copy().str.split(" - ", expand=True)
    price_column = price_column.fillna(0)

    price_column.iloc[:, 0] = price_column.iloc[:, 0].astype(float)
    price_column.iloc[:, 1] = price_column.iloc[:, 1].astype(float)

    mask = price_column.iloc[:, 1] != 0
    new_price = (price_column[mask][0] + price_column[mask][1]) / 2
    price_column['price'] = new_price
    price_column['price'] = price_column['price'].fillna(price_column.iloc[:, 0])

    # Handle trademarks
    pattern = '|'.join([' - Good & Gather™', ' - Favorite Day™', '- Archer Farms™', ' - Market Pantry™', ' - Cake Candles',
                        ' - Wondershop™',
                        ' - Hyde & EEK! Boutique™'])
    product_details = df['product_name'].copy().str.replace(pattern, '')
    product_details = product_details.to_frame()

    # Deal with various product name - amount label
    pattern_new = '|'.join([' - ', ' -', '- ', ' – ', '– ', ' –', ' — ', ' —', '— '])
    product_details['product_name'] = product_details['product_name'].str.replace(pattern_new, ' - ')
    product_details = product_details['product_name'].copy().str.replace(pattern, '')
    product_details = product_details.str.split(" - ")

    # Create new dataframe contain cleaned data
    product_details_df = pd.DataFrame()
    for product_detail in product_details:
        if len(product_detail) > 1:
            details = [''.join(str(e) for e in product_detail[:-1]), product_detail[-1]]
        else:
            details = [product_detail[0], '']
        product_details_df = product_details_df.append(pd.DataFrame(np.array(details).reshape(1, 2),
                                                                    columns=['product name', 'unit']), ignore_index=True)

    # Reset df index
    product_details_df = product_details_df.reset_index(drop=True)
    price_column_join = price_column.reset_index(drop=True)
    product_details_df = product_details_df.join(price_column_join['price'])

    # Store as xlsx file
    writer = ExcelWriter('./Target/target_clean.xlsx')
    product_details_df.to_excel(writer, index=False)
    writer.save()

    # product_details_df.to_csv('target_clean.csv')
