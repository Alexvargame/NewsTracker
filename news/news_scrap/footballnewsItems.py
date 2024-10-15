

import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news_scrap.items import ArticleItem
#from ..views import save_news

import re
import json
from datetime import datetime

class NewsFootBallSpider(CrawlSpider):
    month_dict = {
        'января': 'January',
        'февраля': 'Fabruary',
        'марта': 'Marth',
        'апреля': 'April',
        'мая': 'May',
        'июня': 'June',
        'июля': 'July',
        'августа': 'August',
        'сентября': 'September',
        'октября': 'October',
        'ноября': 'November',
        'декабря': 'December'
    }
    name='footballnewsItems'
    allowed_domains =['profootball.ua']
    start_urls=['https://profootball.ua/latest/']
    rules=[Rule(LinkExtractor(allow=start_urls[0]),callback='parse_items',cb_kwargs={'is_article': True})]
    #Rule(LinkExtractor(allow=r'page\/(?:2|3)/'), callback='parse_items', cb_kwargs={'is_article': True})
    # print('d',dir(rules[0]))
    # print('dd',rules[0].cb_kwargs,rules[0].follow)
    # print('eee',dir(rules[0].link_extractor))
    #print(rules[0].link_extractor.allow_domains)
    # print(rules[0].link_extractor.allow_res)
    def parse_items(self, response,is_article):
        global news_lst
        news_lst = []
        explored = []
        COUNT_NEWS = 20
        if is_article:
            count=0
            url = response.url
            print(url)
            lnks = response.xpath('//body/div[@class = "site"]'
                                  '/div[@class = "site-content container clear"]'
                                  '/div[@class = "content-area clear"]'
                                  '/div[@class = "site-main clear"]').xpath('.//a')
            print(len(lnks))
            for l in lnks:
                article=ArticleItem()
                if l.xpath('@href').extract_first().split('/')[-2].split('-')[0].isdigit() and l.xpath('@href').extract_first() not in explored:
                    # print(l, 'hr', l.xpath('@href').extract_first(),'count',count)
                    yield scrapy.Request(l.xpath('@href').extract_first(), callback = self.article_scr,
                                         meta={
                                            'link_l':l.xpath('@href').extract_first(),
                                         })
                    count+=1
                    explored.append(l.xpath('@href').extract_first())
                    explored.append(l.xpath('@href').extract_first()+'#respond')
                    if  count >COUNT_NEWS:
                        return news_lst
        return news_lst
    def article_scr(self,responce):
        # print('AAAAA')
        article=ArticleItem()
        pp = responce.xpath('//body/div[@class = "site"]'
                                  '/div[@class = "site-content container clear"]'
                                  '/div[@class = "content-area"]'
                                  '/main[@class = "site-main"]').xpath('.//article')

        if pp:
            art_title = pp.xpath('.//p/text()').extract_first()
            art_body = ''.join(pp.xpath('.//p/text()').extract())
            if pp.xpath('//div[@class = "st-post-tags entry-header"]')[0].xpath('.//a').xpath('@title').extract():
                theme = pp.xpath('//div[@class = "st-post-tags entry-header"]')[0].xpath('.//a').xpath('@title').extract()[0].split('.')
                if "Чемпионат" in [th.strip() for th in theme[0].split()]:
                    theme_par = ' '.join([th.strip() for th in theme[0].split()][:2])
                    theme_art = theme[1].strip()
                else:
                    theme_par = 'Футбол'
                    theme_art = ''
        else:
            art_title = f"No data"
            art_body = f"No data"
        date_pub = responce.xpath('//body/div[@class = "site"]'
                            '/div[@class = "site-content container clear"]'
                            '/div[@class = "content-area"]'
                            '/main[@class = "site-main"]'
                            '/div[@class = "entry-meta clear"]'
                            '/span[@class = "entry-date"]/text()').extract()
        date_pub = date_pub[0].split(',')
        date_pub=date_pub[0].strip().split()[0]+' '+self.month_dict[date_pub[0].strip().split()[1]]+' '+date_pub[1].strip()+' '+date_pub[2].strip()
        date_pub = datetime.strptime(date_pub, "%d %B %Y %H:%M")

        article = {
            'title': art_title,
            'link': responce.meta['link_l'],
            'body': art_body,
            'theme': theme_par,
            'theme_ch': theme_art,
            'date_pub': date_pub
        }
        news_lst.append(article)
        return article
