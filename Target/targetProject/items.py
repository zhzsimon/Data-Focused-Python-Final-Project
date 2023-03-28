# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# This class defines an item scraped from the target website
# product name - the name of each grocery item
# price - price of each grocery item
class TargetprojectItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    price = scrapy.Field()

