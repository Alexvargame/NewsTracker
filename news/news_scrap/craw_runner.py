from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

#from spiders.football_news_spider import NewsFootBallScrap

import re
import json


class NewsFootBallSpider(CrawlSpider):
    print('BRGIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
    name='footballnewsItems'
    allowed_domains =['football24.ua']
    start_urls=['https://football24.ua/ru/']
    rules=[Rule(LinkExtractor(allow=start_urls[0]),callback='parse_items',cb_kwargs={'is_article': True})]

    def parse_items(self, response, is_article):
        global news_lst
        news_lst = []
        explored = []
        COUNT_NEWS = 10
        if is_article:
            count = 0
            url = response.url
            print(url)
            lnks = response.xpath('//body/div[@class = "site"]'
                                  '/div[@class = "site-content container clear"]'
                                  '/div[@class = "content-area clear"]'
                                  '/div[@class = "site-main clear"]').xpath('.//a')
            print(len(lnks))
            for l in lnks:
                article = ArticleItem()
                if l.xpath('@href').extract_first().split('/')[-2].split('-')[0].isdigit() and l.xpath(
                        '@href').extract_first() not in explored:
                    # print(l, 'hr', l.xpath('@href').extract_first(),'count',count)
                    yield scrapy.Request(l.xpath('@href').extract_first(), callback=self.article_scr,
                                         meta={
                                             'link_l': l.xpath('@href').extract_first(),
                                         })
                    count += 1
                    explored.append(l.xpath('@href').extract_first())
                    explored.append(l.xpath('@href').extract_first() + '#respond')
                    if count > COUNT_NEWS:
                        return news_lst
        return save_news(news_lst)

    def article_scr(self, responce):
        print('AAAAADFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf')
        article = ArticleItem()
        pp = responce.xpath('//body/div[@class = "site"]'
                            '/div[@class = "site-content container clear"]'
                            '/div[@class = "content-area"]'
                            '/main[@class = "site-main"]').xpath('.//article')

        if pp:
            art_title = pp.xpath('.//p/text()').extract_first()
            art_body = ''.join(pp.xpath('.//p/text()').extract())
            if pp.xpath('//div[@class = "st-post-tags entry-header"]')[0].xpath('.//a').xpath('@title').extract():
                theme = \
                pp.xpath('//div[@class = "st-post-tags entry-header"]')[0].xpath('.//a').xpath('@title').extract()[
                    0].split('.')
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
        date_pub = date_pub[0].strip().split()[0] + ' ' + self.month_dict[date_pub[0].strip().split()[1]] + ' ' + \
                   date_pub[1].strip() + ' ' + date_pub[2].strip()
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

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    print('RRTeweawraqewrwarawer',NewsFootBallSpider)
    yield runner.crawl(NewsFootBallSpider)
    reactor.stop()

def main():
    crawl()
    reactor.run()

if __name__ == "__main__":
    main()