# This is the scrapy spider main file which scrapes target website
# over every grocery category

import scrapy
from ..codes import CODE
from ..items import TargetprojectItem


class TargetSpider(scrapy.Spider):
    name = 'target'
    allowed_domains = ['www.target.com']
    base_url = 'https://www.target.com/c//-/'
    url_index = 0
    Nao = 0
    cur_page = 1

    def start_requests(self):
        yield scrapy.Request(url=self.base_url + CODE[self.url_index], callback=self.parse)

    def parse(self, response):
        items = TargetprojectItem()
        card_list = response.xpath('//div[@data-test="productCardBody"]')
        page_num = response.xpath('//button[@data-test="select"]/div/div[1]//text()').extract()
        if page_num:
            page_num = int(page_num[0].split()[-1])
        else:
            page_num = 1

        for i in card_list:
            items['product_name'] = i.xpath('./div/div/div/div/div/a/@aria-label').get()
            items['price'] = i.xpath('./div/div/div/div/div/div[@data-test="current-price"]//text()').extract()[0]
            yield items

        # Switch page in the same category if the current page still in range
        # Otherwise go to next category
        if self.cur_page < page_num:
            self.Nao += 24
            self.cur_page += 1
            url = self.base_url + CODE[self.url_index] + '/?Nao=' + str(self.Nao)
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            self.Nao = 0
            self.cur_page = 1
            self.url_index += 1
            print(self.url_index)
            if self.url_index < len(CODE):
                print(1)
                url = self.base_url + CODE[self.url_index]
                yield scrapy.Request(url=url, callback=self.parse)
