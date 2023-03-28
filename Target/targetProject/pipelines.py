# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# The pipeline is used to process each scraped item
# Here, we print each scrape item for verification and debugging purpose
class TargetprojectPipeline:
    def process_item(self, item, spider):
        print(item)
        return item
