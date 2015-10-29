from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.exceptions import DontCloseSpider
from scrapy import signals
from content_processor import ContentProcessor


class GeneralSpider(Spider):
    name = 'general'

    def __init__(self, *args, **kwargs):
        super(GeneralSpider, self).__init__(*args, **kwargs)
        self.content_processor = ContentProcessor()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self):
        self.log("Spider idle signal caught.")
        raise DontCloseSpider

    def parse(self, response):
        if not isinstance(response, HtmlResponse):
            return
        pc = self.content_processor.process_response(response)
        for link in pc.links:
            r = Request(url=link.url)
            r.meta.update(link_text=link.text)
            yield r

