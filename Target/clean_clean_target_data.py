
"""
By: Simon Zhang and Junfeng Lin

# This file is to clean the target data second time.
# It converts all units to g/ml to simplify calculations and drop all items
# that do not have a unit.
# Note: Special units are converted to -1
This program read target_clean.xlsx as its input.
This program creates clean_clean_target.xlsx which is the final version of cleaned target data

"""
import pandas as pd
import numpy as np
import re
from openpyxl.workbook import Workbook

# This function performs a second clean on the target data.
# It reads the target_clean.xlsx as its input and converts all units to g/ml to
# simplify calculations and drop all items
# that do not have a unit.
def cleancleanedtarget():
    df = pd.read_excel("./Target/target_clean.xlsx")

    # Drop null in unit
    null_df = df.copy().loc[df.isna().any(axis=1)].index
    df = df.drop(null_df)
    df['unit'] = df['unit'].str.replace('0z', 'oz') # Replace 0z with oz

    for i in df['unit'].index:
        unit = df.loc[i]['unit']
        number = re.findall('[0-9]+[.]*[0-9]*', unit)
        if len(number) == 0:
            df.at[i, 'unit'] = '-1.0'

    df = df.drop(8947) # Drop special case

    # convert special cases to -1 and price per lb to 453.592 grams
    liquid_units = {'fl oz': 29.5735, 'ml': 1.0, 'sticks': -1.0,
                    'oz': 28.3495, 'lb': 453.592, 'lbs': 453.592, 'g': 1.0, 'liter': 1000, 'l': 1000}
    for i in df.index:
        unit = df.loc[i]['unit']
        unit = unit.lower().strip()
        if unit == 'each':
            df.at[i, 'unit'] = '-1'
            continue

        if unit == 'price per lb':
            df.at[i, 'unit'] = '453.592'
            continue

        trade_marks = ['General Mills', "Kellogg's", "Chocolate Chip Cookie Dough",
                       "Chocolate Chip", "Milk Chocolate", "Milk Chocolate Delight", "Chocolate",
                       "(Select Count)", "Simply Balanced™", "California Roots™", "Jingle & Mingle™",
                       "The Collection", 'Wine Cube™', 'Spritzer™']
        if unit in trade_marks:
            df.at[i, 'unit'] = '-1'
            continue

    # Handle cases where there are slashes in the unit
    for i in df.index:
        unit = df.loc[i]['unit']
        if str(unit) == 'nan':
            continue
        unit = unit.lower()
        slash_list = unit.split('/')
        if len(slash_list) == 2:
            if 'ct' in unit:
                for l in slash_list:
                    if "ct" not in l:
                        df.at[i, 'unit'] = l
                        break

            if 'slices' in unit:
                for l in slash_list:
                    if "slices" not in l:
                        df.at[i, 'unit'] = l
                        break

            p = re.findall('pl$', unit)
            if p:
                for l in slash_list:
                    if "pl" not in l:
                        df.at[i, 'unit'] = l
                        break

            if '"' in unit:
                for l in slash_list:
                    if '"' not in l:
                        df.at[i, 'unit'] = l
                        break

            if 'tablets' in unit:
                for l in slash_list:
                    if 'tablets' not in l:
                        df.at[i, 'unit'] = l
                        break

            if 'ft' in unit:
                for l in slash_list:
                    if 'ft' not in l:
                        df.at[i, 'unit'] = l
                        break

    # Keep deal with / cases
    unit_list = df['unit'].str.split('/', expand=True)
    temp = unit_list[unit_list.iloc[:, 1].notnull()]

    # In these slash cases, slash means per, so we need to multiply
    # two numbers together to get its total volume
    for i in temp.index:
        unit = df.loc[i]['unit'].lower()
        # print(i)
        if 'pk' in unit:
            # print(unit)
            l = [unit]
            for s in re.findall('[0-9]+[.]*[0-9]*', unit):
                l.append(float(s))

            result = l[1] * l[2]
            slash_list = unit.split('/')
            # print(slash_list)
            for s in slash_list:
                for k in liquid_units.keys():
                    if k in s:
                        df.at[i, 'unit'] = str(result * liquid_units[k])
                        break

    test = df['unit'].str.split('/', expand=True)
    for i in test[test.iloc[:, 1].notnull()].index:
        df.at[i, 'unit'] = test.loc[i][0]

    # Drop all duplicate items
    df = df.drop_duplicates(subset=['product name'])
    df = df.drop(df.loc[df.isna().any(axis=1)].index)

    # Handle various units and convert them to g/ml
    liquid_units = {'fl oz': 29.5735, 'sticks': -1.0, 'ounce': 28.3495, 'gal': 4546.09,
                    'oz': 28.3495, 'lb': 453.592, 'lbs': 453.592, 'ml': 1.0, 'cups': 220,
                    'liter': 1000, 'ml': 1.0, 'pk': -1.0, "ct": -1.0, "pc": -1.0,
                    'price per lb.': -1.0, 'priced per lb': -1.0, 'serves': -1.0, 'piece': -1.0, '1.55o': -1.0,
                    'nestle': -1.0, 'pcs': -1.0, 'sharing': -1.0, 'stick': -1.0, 'good': -1.0, 'breyers': -1.0,
                    'pack': -1.0,  'pks': -1.0, 'farm': -1.0, '2.12z': -1.0, '"': -1.0, '15z': -1.0, 'qt': -1.0,
                    'pt': -1.0, 'box': -1.0, 'l ': 1000, 'l': 1000, 'g': 1.0}
    for i in df.index:
        unit = df.loc[i]['unit'].lower()
        number = re.findall('[0-9]+[.]*[0-9]*', unit)
        for k in liquid_units.keys():
            if k in unit:
                if len(number) == 2:
                    # print(unit)
                    result = float(number[0]) * float(number[1])
                    df.at[i, 'unit'] = result * liquid_units[k]
                    break
                if len(number) == 4:
                    df.at[i, 'unit'] = float(number[0]) * liquid_units[k]
                    break
                if len(number) == 1:
                    df.at[i, 'unit'] = float(number[0]) * liquid_units[k]
                    break

    # Set special cases units
    df.at[8907, 'unit'] = 200
    df.at[8830, 'unit'] = 180

    # Output to xlsx file
    df.to_excel("./Target/clean_clean_target.xlsx")
