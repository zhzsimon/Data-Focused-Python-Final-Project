"""
By: Renjie Zhong and Wang Chenxu

The program scrape the instruction and ingredient of the recipes from the 101cookbook website. 
This program also changed all invalid number in the amount column into valid data pattern.

This program will create three files named "reciperaw.txt"(stores the raw data scraped from the website),
"recipe_instruction_try.csv"(contains recipe name and instruction),
and "cleaned_ingredient_try.csv"(contains recipe name, amount, unit and ingredidents)

"""
from math import e
import re
from lxml import etree
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

ingredients = []
instructions = []


# scarpe the instruction of the cookbook
def scrapeInstruction(website, fout):
    html = urlopen(website)
    bsyc = BeautifulSoup(html.read(), "lxml")
    # find all of the line match the tag name and class name
    select_xml = bsyc.find_all('ol', 'wprm-recipe-instructions')
    fout.write(str(select_xml))
    for i in select_xml:
        recipe = BeautifulSoup(str(i), 'xml')
        instruction = recipe.find_all('div', 'wprm-recipe-instruction-text')
        for j in instruction:
            list = []
            list.append(str(website[28:]).strip('/').strip('"'))
            list.append(j.get_text())
            if len(list):
                instructions.append(list)
    return


# scrape the ingredient of the cookbook
def scrapeIngredients(website, fout):
    html = urlopen(website)
    bsyc = BeautifulSoup(html.read(), "lxml")
    # find all of the line match the tag name and class name
    select_xml = bsyc.find_all('li', 'wprm-recipe-ingredient')
    fout.write(str(select_xml))
    for i in select_xml:
        list = []
        list.append(str(website[28:]).strip('/').strip('"'))
        recipe = BeautifulSoup(str(i), 'xml')
        try:
            amount = recipe.find('span', 'wprm-recipe-ingredient-amount')
            list.append(reformatAmount(amount.get_text()))
        except:
            list.append('')
        try:
            unit = recipe.find('span', 'wprm-recipe-ingredient-unit')
            list.append(unit.get_text())
        except:
            list.append('')
        try:
            name = recipe.find('span', 'wprm-recipe-ingredient-name')
            list.append(name.get_text())
        except:
            list.append('')
        if len(list):
            ingredients.append(list)


# scrape the content of the cookbook
def ScrapingCookbook(url):
    r = requests.get(url)
    content = etree.HTML(r.content)
    html_data = content.xpath('//div[@class="archiverecipe"]/a/@href')
    return html_data


# clean the ingredient amount
def reformatAmount(s):
    if "-" in s:
        s = s.split("-")[0].strip()
    if s == "1/2":
        return 0.5
    elif s == "1/3":
        return 0.33
    elif s == "1/4":
        return 0.25
    elif s == "2/3":
        return 0.67
    elif s == "3/4":
        return 0.75
    elif s == "1/8":
        return 0.125
    elif s == "1 1/2":
        return 1.5
    elif s == "2 1/2":
        return 2.5
    elif s == "3 1/2":
        return 3.5
    elif s == "4 1/2":
        return 4.5
    elif s == "1 1/3":
        return 1.33
    elif s == "1 1/4":
        return 1.25
    elif s == "2 1/4":
        return 2.25
    elif s == "1 3/4":
        return 1.75
    elif s == "1 3":
        return 3
    elif s == "1 12":
        return 12
    elif s == "1 14":
        return 14
    elif s == "2 14":
        return 28
    elif s == "1 15":
        return 15
    elif s == "1 28":
        return 28
    elif s == "½":
        return 0.5
    elif s == "¼":
        return 0.25
    elif s == "1 ½":
        return 1.5
    elif s == "1/4+":
        return 0.25
    elif s == "1+":
        return 1
    else:
        return s


def runcookbook():
    url = "https://www.101cookbooks.com/archives.html#100+%20Vegetarian%20Recipes"
    websites = ScrapingCookbook(url)[0:30]
    fout = open('./Recipe/reciperaw.txt', 'a', encoding='utf-8')
    time = 0
    for i in websites:
        scrapeInstruction(i, fout)
        scrapeIngredients(i, fout)
        time += 1
        print(time)
    fout.close()
    ingredientsdf = pd.DataFrame(ingredients, columns=['Recipe', 'Amount', 'Unit', 'Ingredient'])
    instructionsdf = pd.DataFrame(instructions, columns=['Recipe', 'Instruction'])
    ingredientsdf.drop_duplicates()
    instructionsdf.drop_duplicates()
    ingredientsdf.to_csv('./Recipe/cleaned_ingredient_try.csv', index=None,
                         header=True, encoding="utf-8-sig")
    instructionsdf.to_csv('./Recipe/recipe_instruction_try.csv',
                          index=None, header=True, encoding="utf-8-sig")


if __name__ == '__main__':
    runcookbook()
