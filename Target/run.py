from scrapy import cmdline
from Target.targetProject.spiders.target import TargetSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


# Run the target spider to scrape each item's name and price from each target grocery website

class Scraper:
    def __init__(self):
        settings_file_path = 'Target.targetProject.settings'  # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        setting = get_project_settings()
        setting['FEED_FORMAT'] = 'csv'
        setting['FEED_URI'] = 'Target/target.csv'
        setting['FEED_EXPORT_ENCODING'] = 'utf-8'
        self.process = CrawlerProcess(setting)

        self.spider = TargetSpider  # The spider you want to crawl

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start(stop_after_crawl=True)
