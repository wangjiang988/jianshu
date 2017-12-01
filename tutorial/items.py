# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UserItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    siteUrl = scrapy.Field() #主页地址
    focus = scrapy.Field() #关注数
    fansCount = scrapy.Field()  #粉丝数
    postCount = scrapy.Field() # 文章数
    wordsCount = scrapy.Field() #字数统计
    likeCount = scrapy.Field() #收获喜欢数


class CategoryItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field() #分类路由
    postCount = scrapy.Field() #文章数
    focusCount = scrapy.Field() #关注人数