# -*- coding: utf-8 -*-
import csv
import json
import random
import re
import sys
import traceback
from json import JSONDecodeError

import scrapy

from project.items import ProjectItem


class StartupParser(scrapy.Spider):
    name = 'startup_parser'

    def start_requests(self):
        with open('startups.csv', 'r') as urls_file:
            urls_list = csv.reader(urls_file, delimiter=',')
            data = sum([i for i in urls_list], [])
            selected_urls = random.sample(data, 20000)
            for url in selected_urls:
                url = url + '?json'
                print(url)
                yield scrapy.Request(url, callback=self.parse, errback=self.errback)

    def parse(self, response):
        selector = scrapy.Selector(response, type="html")

        description_short = selector.xpath('//div[@class="row"]/div[@class="col-md-10"]/div[@class="row"]/div['
                                           '@class="col-md-12"]/div/text()').extract_first()
        description = '\n'.join(selector.xpath('//p[@class="profile-desc-text"]/text()').extract())

        yield {'company_name': selector.xpath("//h1[@class='profile-startup']/text()").extract_first(),
               'request_url': response.request.url[:-5],
               'request_company_url': selector.xpath('//div[@class="mbt"]/span[1]/a/@href').extract_first(),
               'location': selector.xpath('//div[@class="mbt"]/span[3]/a/text()').extract_first(),
               'tags': ', '.join(selector.xpath('//div[@class="row"]/div[@class="col-md-10"]/div[@class="row"]/div['
                                                '@class="col-md-12"]/div[3]/span/a/text()').extract()),
               'founding_date': selector.xpath('//div[@class="row"]/div[@class="col-md-10"]/div[@class="row"]/div['
                                               '@class="col-md-12"]/p/span/text()').extract_first(),
               'urls': ', '.join(selector.xpath("//div[contains(@class,'col-md-5 socials pdt text-right')]/a/@href")
                                 .extract()),
               'description_short': description_short,
               'description': description,
               'phones': ', '.join(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', description + description_short)),
               'founders': ', '.join(selector.xpath("//div[@class='desc']/span[@class='item-label bold']/a/text()").extract())
               }

        # founders_sel = selector.xpath('//div[@class="portlet box-view followers team _yeti_done"]').getall()
        # print(founders_sel)

    def errback(self, failure):
        """handle failed url (failure.request.url)"""
        pass
# scrapy runspider urls_parser.py
# scrapy runspider project/spiders/get_data_spider.py -o results.csv
