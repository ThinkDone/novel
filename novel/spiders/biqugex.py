# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from novel.items import NovelItem


class BiqugexSpider(scrapy.Spider):
    name = "biqugex"
    allowed_domains = ["biqugex.com"]
    start_urls = ['http://biqugex.com/book_26796/11560883.html']

    def parse(self, response):
        with open('xjzm.txt', 'a+') as f:
            f.write(response.css('title::text').extract_first().encode(response.encoding))
            