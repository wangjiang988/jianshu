# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import CategoryItem
from scrapy.selector import Selector

# 爬去简书最作者，及相关数据
class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['http://www.jianshu.com/']
    start_url = 'http://www.jianshu.com/recommendations/collections?order_by=hot&page={page}'
    current_page = 1
    perPage = 10

    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(page=self.current_page), callback=self.parse)
        self.log('current_page:%d' % self.current_page)

    def parse(self, response):
        try:
            page = response.css('div#list-container')
            list = page.css('div.collection-wrap')
            categoryCount = len(list)
            self.log('cateCount: %d' % categoryCount)
            for wrap in list:
                category  = CategoryItem()
                category['name'] = wrap.css('h4.name::text').extract_first()
                category['url'] = wrap.css('div.count a::attr(href)').extract_first()
                category['postCount'] = wrap.css('div.count a::text').extract_first()
                category['focusCount'] = wrap.css('div.count::text').extract_first()
                yield category
            if(self.current_page == 1 ):
                self.perPage = categoryCount
            if (categoryCount == self.perPage) :
                self.current_page += 1
                self.log('current_page:%d' % self.current_page)
                yield response.follow(url=self.start_url.format(page=self.current_page), callback=self.parse)
            else:
                self.log('爬取结束')
                    
        except Exception as e:
            print("发生错误")
        
    