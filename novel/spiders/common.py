# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from novel.items import NovelItem


class CommonSpider(scrapy.Spider):
    name = "common"
    start_urls = ['http://biqugex.com/book_26796/11560883.html']

    def parse(self, response):
        chapter_name = response.css('#box_con > div.bookname > h1::text').extract_first().encode(response.encoding)

        with open(chapter_name + '.txt', 'w') as f:
            f.write(chapter_name)
            f.write('\n')
            f.write('{0}\n\n'.format(response.url))
            for line in response.css('#content ::text').extract():
                f.write(line.encode(response.encoding))
        next_chapter_path = response.xpath('//*[@id="box_con"]/div[5]/a[4]/@href').extract_first()

        # the latest chapter
        if next_chapter_path == '/book_26796/':
            return

        next_chapter_url = response.urljoin(next_chapter_path)
        return scrapy.Request(url=next_chapter_url, callback=self.parse)