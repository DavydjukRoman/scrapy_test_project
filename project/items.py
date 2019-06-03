# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectItem(scrapy.Item):
    company_name = scrapy.Field
    request_url = scrapy.Field
    response_url = scrapy.Field
    request_company_url = scrapy.Field
    location = scrapy.Field
    tags = scrapy.Field
    founding_date = scrapy.Field
    founders = scrapy.Field
    employee_range = scrapy.Field
    urls = scrapy.Field
    emails = scrapy.Field
    phones = scrapy.Field
    description_short = scrapy.Field
    description = scrapy.Field
