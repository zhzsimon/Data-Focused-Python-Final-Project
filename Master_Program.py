"""
By: Group6
This is the main program to run all the codes. Please use this to test our codes, do not run
py files individually since the path will be different from running in the main or running in each code

This file import all scrape, clean, ui files.

"""
from Yelp import yelpScrape, detailPage, yelpmenuScrape, menuCombine, restaurantClean, getClean, getRaw
from Recipe import scrape_method, recipename_clean
from Target import clean_target_data, clean_clean_target_data
from food_conflict import clean_food_conflicts, getRaw_fc, getClean_fc
from MatchRecipe import match_recipe_clean
from python_ui import main1
from Target.run import Scraper


# all codes for scraping, includes target, yelp and 101cookbook
def scrapedata():
    # target
    print("start scraping Target \n")
    target = Scraper()
    target.run_spiders()
    print("finish scraping Target \n")

    # result data in Target\target.csv

    # yelp
    print("start scraping Yelp \n")
    yelpScrape.runyelplist()
    detailPage.runyelpdetail()
    yelpmenuScrape.runyelpmenu()
    print("finish scraping Yelp \n")

    # result data in Yelp\data_completed\raw_data.csv

    # 101cookbook
    print("start scraping 101cookbook \n")
    scrape_method.runcookbook()
    print("finish scraping 101cookbook \n")
    # result data in Recipe\recipe_instruction.csv


def cleandata():
    # clean target
    clean_target_data.cleantarget()
    # result data in Target\target_clean.xlsx
    clean_clean_target_data.cleancleanedtarget()
    # result data in Target\clean_clean_target.xlsx

    # clean yelp
    # clean the detail page data
    restaurantClean.cleandetail()
    # combine raw data together
    getRaw.getraw()
    # result data in Yelp\data_scrape\raw_data.csv
    # combine menu
    menuCombine.getdata()
    # result data in Yelp\data_scrape\all_menudata.csv
    # combine clean data together
    getClean.getclean()
    # result data in Yelp\data_scrape\restaurant_clean.csv

    # clean recipe
    recipename_clean.cleaningredient()
    # result data in Recipe\recipe_clean_try.csv

    # clean CDC data
    clean_food_conflicts.cleanfoodconflict()
    # result data in food_conflicrs\data_download\food_cdc.csv
    # get raw data
    getRaw_fc.getraw()
    # result data in food_conflicrs\data_download\FoodDataFinal.csv
    # get clean data
    getClean_fc.getclean()
    # result data in food_conflicrs\data_download\FoodDataFinalClean.csv


def matchrecipe():
    match_recipe_clean.matchrecipt()


def runui():
    main1.runUI()


def runtogether():
    # scraping data takes a looooonnnng time, so we comment it
    # if you really want to run it, please erase the comment
    # scrapedata()
    # cleandata()
    # matchrecipe()
    runui()


if __name__ == '__main__':
    runtogether()
