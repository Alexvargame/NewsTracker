

import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news_scrap.items import ArticleItem
#from ..views import save_news

import re
import json
from datetime import datetime

class NewsHokkeySpider(CrawlSpider):
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
    name='hockeynewsItems'
    allowed_domains =['sport.ua']
    start_urls=['https://sport.ua/hockey']
    rules=[Rule(LinkExtractor(allow=r'hockey/[a-z0-9]*'),callback='parse_items',cb_kwargs={'is_article': True})]
    def parse_items(self, response,is_article):
        global news_lst
        news_lst = []
        explored = []
        COUNT_NEWS = 15
        if is_article:
            count=0
            url = response.url
            print('URL',url)
            lnks = response.xpath('//body/div[@id = "outer-top"]'
                                  '/div[@class = "wrap"]'
                                  '/main[@class = "main"]'
                                  '/aside[@class = "main-sidebar"]'
                                  '/div[@class = "news news-mob"]/div[@class = "news-items"]').xpath('.//a')

            for l in lnks:
                article=ArticleItem()
                if l.xpath('@href').extract_first().split('/')[-1].split('-')[0].isdigit() and l.xpath('@href').extract_first() not in explored:
                    yield scrapy.Request(l.xpath('@href').extract_first(), callback = self.article_scr,
                                         meta={
                                            'link_l':l.xpath('@href').extract_first(),
                                             'theme_par_l': url.split('/')[-2],
                                             'theme_art_r': url.split('/')[-1],
                                         })
                    count+=1
                    explored.append(l.xpath('@href').extract_first())
                    explored.append(l.xpath('@href').extract_first()+'#respond')
                    if  count >COUNT_NEWS:
                        return news_lst
        return news_lst
    def article_scr(self,responce):
        article=ArticleItem()
        pp = responce.xpath('//body/div[@id = "outer-top"]'
                            '/div[@class = "wrap"]'
                            '/main[@class = "main news-page"]'
                            '/div[@class = "main-inner-wrap"]'
                            '/section[@class = "main-inner-content"]').xpath('.//div')

        if pp:
            art_title = pp.xpath('//h1[@class = "news-v-title"]/text()').extract_first()
            text_pp = pp.xpath('//div[@class = "news-v-content"]/div[@class = "news-v-inner"]/div[@id = "news_text"]')
            art_body = ''.join(text_pp.xpath('.//p/text()').extract())
        else:
            art_title = f"No data"
            art_body = f"No data"
        hour_min = pp.xpath('//div[@class = "news-v-head desktop fl-c"]/span[@class = "news-v-head-date"]/a/text()').extract_first().split(',')[1].strip().split(':')
        date_pub = pp.xpath('//div[@class = "news-v-head desktop fl-c"]/span[@class = "news-v-head-date"]/a').xpath('@href').extract_first()
        date_pub = datetime(int(date_pub.split('/')[-3]),int(date_pub.split('/')[-2]),int(date_pub.split('/')[-1]),int(hour_min[0]),int(hour_min[1]))
        # date_pub=date_pub[0].strip().split()[0]+' '+self.month_dict[date_pub[0].strip().split()[1]]+' '+date_pub[1].strip()+' '+date_pub[2].strip()
        # date_pub = datetime.strptime(date_pub, "%d %B %Y %H:%M")

        article = {
            'title': art_title,
            'link': responce.meta['link_l'],
            'body': art_body,
            'theme': responce.meta['theme_par_l'],
            'theme_ch': responce.meta['theme_art_r'],
            'date_pub': date_pub
        }
        news_lst.append(article)
        return article
