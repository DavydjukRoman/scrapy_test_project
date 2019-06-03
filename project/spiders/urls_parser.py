# -*- coding: utf-8 -*-
import json
import re

import scrapy

from project.items import ProjectItem


class UrlsParserSpider(scrapy.Spider):
    name = 'urls_parser'
    page = 0
    quotes_base_url = 'https://e27.co/startups/load_startups_ajax?all&per_page=%s'
    start_urls = [quotes_base_url % page]

    def start_requests(self):
        for i in range(1, 28000):
            self.page = self.page + 1
            yield scrapy.Request(self.quotes_base_url % self.page, callback=self.parse, errback=self.errback)

    def parse(self, response):
        print("Existing settings: %s" % self.settings.attributes.keys())
        content = json.loads(response.body)['pagecontent']
        #print(content)
        #for block in response.css('div.startup-block'):
        #    print("Current block:")
        #    print(block)
        #    yield {
        #        'company-name': block.css('span.company-name::company-name').get(),
        #    }


        urls = re.findall('https?://e27.co/startup/(?:[-\w.]|(?:%[\da-fA-F]{2}))+', content)
        counter = 1
        for link in urls:
            print(counter)
            print(link)
            counter += 1
            yield {'url': link}

    def errback(self, failure):
        '''handle failed url (failure.request.url)'''
        pass
# scrapy runspider urls_parser.py
#scrapy runspider project/spiders/urls_parser.py -o startups.csv
