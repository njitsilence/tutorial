# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class PeopleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickname = Field()
    zhihuid = Field()
    busniess = Field()
    img_url = Field()
    gender = Field()
    following_count = Field()
    follower_count = Field()
    # following_url = scrapy.Field()

class MyImageItem(Item):
    image_urls =Field()
    images = Field()
    image_paths = Field()