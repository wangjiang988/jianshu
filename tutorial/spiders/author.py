# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import UserItem
from urllib import parse


class AuthorSpider(scrapy.Spider):
    name = 'author'
    allowed_domains = ['jianshu.com']
    domain = 'http://www.jianshu.com'
    start_url = 'http://www.jianshu.com/recommendations/collections?order_by=hot&page={page}'
    start_urls = ['http://jianshu.com/']
    current_page = 1
    perPage = 10

    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(page=self.current_page), callback=self.parse)

    def parse(self, response):
        try:
            page = response.css('div#list-container')
            list = page.css('div.collection-wrap')
            categoryCount = len(list)
            self.log('cateCount: %d' % categoryCount)
            #进入分类详情，解析用户主页
            for wrap in list:
                category_url = wrap.css('div.count a::attr(href)').extract_first()
                category_url = self.domain + category_url
                self.log('category_url:%s'  % category_url)
                yield scrapy.Request(url=category_url, callback=self.parse_category)
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
        
    # 爬取分类页面
    # TODO  验证
    def parse_category(self, response):
        # 开始路由
        # 这里也要循环 加上 ?order_by=added_at&page=2
        # like   http://www.jianshu.com/c/bDHhpK?order_by=added_at&page=2
        start_category_url = response.url
        self.log("--------------------------------" )
        self.log("当前爬取页面:%s" % start_category_url)
        self.log("--------------------------------" )
        
        # 解析page参数
        url_dict = parse.urlparse(start_category_url)
        params = parse.parse_qs(url_dict.query, True)
        print(url_dict);
        base_url = self.domain+url_dict.path
        self.log("base_url:%s" % base_url)
        page = 1
        if params.get('page'):
            self.log("page:%s" % params)
            page = int(params['page'][0])

        list = response.css(".note-list li")
        #列表数
        count = len(list) 
        self.log('count: %d' % count)
        for short_post in list:
            # 这里需要去重，重复抓取的用户页面要跳过。
            # 在pipline里边加  
            user_url = short_post.css('a.nickname ::attr(href)').extract_first()
            user_url = self.domain + user_url
            self.log('user_url:%s'  % user_url)
            # 爬取用户页面，最终我们要爬取的数据在这里
            yield scrapy.Request(url=user_url, callback=self.parse_user)

        if  page == 1:
            self.perPage = count

        self.log('perPage: %d' % self.perPage)
        if  count == self.perPage:
            page = page + 1
            next_page = base_url+'?order_by=added_at&page={page}'
            self.log("parse next category page:%s" % page)
            yield response.follow(url=next_page.format(page=page), callback=self.parse_category)
        else:
            self.log('该页爬取结束')
       
    
    #爬取用户首页
    def parse_user(self, response):
        user = UserItem()
        meta = response.css('div.main-top')
        title = meta.css('div.title')
        info = meta.css('div.info li')
        description = response.css('.aside div.description')
        user['name'] = title.css('a.name::text').extract_first()
        user['siteUrl']  = title.css('a.name::attr(href)').extract_first()
        user['description']  = description.css('.js-intro::text').extract_first()
        user['focus'] = info[0].css('p::text').extract_first()
        user['fansCount'] = info[1].css('p::text').extract_first()
        user['postCount'] = info[2].css('p::text').extract_first()
        user['wordsCount'] = info[3].css('p::text').extract_first()
        user['likeCount'] = info[4].css('p::text').extract_first()

        yield user


              