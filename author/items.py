# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Id=scrapy.Field()
    Username = scrapy.Field()
    Profile = scrapy.Field()
    Src = scrapy.Field()
    Img = scrapy.Field()
    Sex = scrapy.Field()
    Attention = scrapy.Field()
    Fans = scrapy.Field()
    Article = scrapy.Field()
    WordNum = scrapy.Field()
    LikeNum = scrapy.Field()
