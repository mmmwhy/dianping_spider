# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shopname = scrapy.Field()
    userid = scrapy.Field()
    postion = scrapy.Field()
    rating = scrapy.Field()
    pass
