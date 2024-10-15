
import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()
    theme = scrapy.Field()
    theme_ch = scrapy.Field()
    date_pub = scrapy.Field()

