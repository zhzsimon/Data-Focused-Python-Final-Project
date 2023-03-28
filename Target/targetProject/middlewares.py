# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# Defines the middle processing unit during the spider
# Process each scraping request in simulated browser
class SeleniumMiddleware(object):
    def __init__(self):
        self.timeout = 50
        # Initialize simulated chrome browser
        options = webdriver.ChromeOptions()
        # Open browser
        self.browser = webdriver.Chrome(chrome_options=options)
        # set browser sizes
        self.browser.set_window_size(1400, 700)
        # set timeout time
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    # process url for scraping
    def process_request(self, request, spider):
        # when the request url is not the current url
        # switch to the request url and open it
        if self.browser.current_url != request.url:
            # get the page
            self.browser.get(request.url)
            time.sleep(6)
        for i in range(4):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source,
                            encoding="utf-8", request=request)

    # close the browser and spider when finished
    def spider_closed(self):
        self.browser.close()
        pass

    @classmethod
    def from_crawler(cls, crawler):
        # when a request finished go to another one
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s


# Middle ware of a scraping program
# process the scraping process
class TargetprojectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# The downloader middleware is a framework of hooks into Scrapy’s request/response processing.
# It’s a light, low-level system for globally altering Scrapy’s requests and responses.
class TargetprojectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
