# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from novel.items import NovelItem


class CommonSpider(scrapy.Spider):
    name = "common"

    def __init__(self, url, *args, **kwargs):
        # Note super() only works for new-style classes.
        super(CommonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        encoding = response.encoding

        chapter_name = response.xpath('//h1//text()').extract_first().encode(encoding, 'ignore')

        with open(chapter_name + '.txt', 'w') as f:
            f.write('{0}\n{1}\n\n'.format(chapter_name, response.url))
            content = '\n'.join(response.css('#content').xpath('.//text()').extract())
            f.write(content.encode(encoding, 'ignore'))

        # Avoid using contains(.//text(), 'search text')
        next_chapter_path = response.xpath(u'//a[contains(., "下一章")]/@href').extract_first()
        if next_chapter_path == '' or next_chapter_path == 'index.html':
            return

        next_chapter_url = response.urljoin(next_chapter_path)
        return scrapy.Request(url=next_chapter_url, callback=self.parse)
