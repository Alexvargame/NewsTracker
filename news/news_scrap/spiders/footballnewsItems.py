import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ArticleItem
import re
import json


class NewsFootBallSpider(CrawlSpider):

    name='footballnewsItems'
    allowed_domains =['football24.ua']#,'kinotochka.co']
    start_urls=['https://football24.ua/ru/']
    rules=[Rule(LinkExtractor(allow=r'ru/\w*/'),callback='parse_items',cb_kwargs={'is_article': True}),
           Rule(LinkExtractor(allow=start_urls[0]),callback='parse_items',cb_kwargs={'is_article': True})]
    # print('d',dir(rules[0]))
    # print('dd',rules[0].cb_kwargs,rules[0].follow)
    # print('eee',dir(rules[0].link_extractor))
    # print(rules[0].link_extractor.allow_domains)
    # print(rules[0].link_extractor.allow_res)
    def parse_items(self, response,is_article):
        print('ERRRRRRRRRRRRRRRRRRRRRRRRR')

        global news_lst
        news_lst = []

        COUNT_NEWS = 1
        if is_article:
            count=0
            url = response.url

            lnks = response.xpath(
                '//div[@class = "layout layout_with_sidebar"]/section[@class = "content content_type_catalog"]'
                '/rz-grid[@class = "ng-star-inserted"]/ul[@class = "catalog-grid ng-star-inserted"]'
                '/li[@class = "catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted"]').xpath('.//a')
            for l in lnks:
                smart=SmartItem()
                if l.xpath('@title').extract_first() != '':
                    yield scrapy.Request(l.xpath('@href').extract_first(), callback = self.parse_os,
                                         meta={
                                            'title_l':' '.join(l.xpath('@title').extract_first().split()[2:]),
                                            'link_l':l.xpath('@href').extract_first(),

                                         })
                    count+=1
                    if  count >COUNT_SMART:
                        return smarts_lst
        return smarts_lst
    # def parse_os(self,responce):
    #     smart=SmartItem()
    #     if responce.xpath('//p[@class = "product-about__brief ng-star-inserted"]/text()').extract_first():
    #         smart_os = responce.xpath('//p[@class = "product-about__brief ng-star-inserted"]/text()').extract_first()
    #         smart_os=[os.strip().split() for os in smart_os.split('/')]
    #         smart_os = ' '.join([os for os in smart_os if os[0] in ['Android', 'iOS']][0])
    #     else:
    #         smart_os = f'No data'
    #     price = responce.xpath('//div[@class = "product-price__wrap ng-star-inserted"]')\
    #         .xpath('.//p[contains(@class,"product-price__big")]/text()').extract_first()
    #     price = ' '.join(price.split("xa"))
    #     smart = {
    #         'title': responce.meta['title_l'],
    #         'link': responce.meta['link_l'],
    #         'smart_os': smart_os,
    #         'price': price,
    #
    #     }
    #     smarts_lst.append(smart)
    #     return smart
