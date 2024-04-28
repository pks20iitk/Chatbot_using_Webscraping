import scrapy
from areadevelopment.items import AreadevelopmentItem


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.areadevelopment.com']
    start_urls = ['https://www.areadevelopment.com/newsItems/']

    def parse(self, response, **kwargs):
        # Extracting the content using css selectors
        news_items = response.css('div#newsItems article a::attr(href)').getall()

        for item in news_items:
            yield scrapy.Request(item, callback=self.parse_article)

    @staticmethod
    def parse_article(response):
        item = AreadevelopmentItem()
        item['title'] = response.css('h1::text').get()
        item['link'] = response.url
        item['article_text'] = response.css('section.areaArticleBody::text').getall()
        yield item
