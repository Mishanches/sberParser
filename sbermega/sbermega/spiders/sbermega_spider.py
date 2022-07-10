import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class SberMegaItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    shop = scrapy.Field()
    price = scrapy.Field()
    product_url = scrapy.Field()

class SpiderSpider(CrawlSpider):
    name = 'sbermega'
    allowed_domains = ['sbermegamarket.ru']
    L = []
    for i in range(1, 29):
        L.append('https://sbermegamarket.ru/catalog/page-'+ str(i) +'?q=%D1%87%D0%B5%D1%85%D0%BE%D0%BB%20guess')
    start_urls = L

    rules = [Rule(LinkExtractor(allow=('.+chehol.+guess.+|.+guess.+chehol.+'),deny=('otzyvy')),
             callback='parse_prod', follow=True), ]

    def parse_prod(self, response):
        item = SberMegaItem()

        code = str(response.xpath('//div[@class = "pdp-first-screen__sku desktop-only"]/text()').get())
        han_code = re.sub('\D', '', code)

        price = str(response.xpath('//span[@class = "pdp-sales-block__price-final"]/text()').get())
        handle_price = re.sub(' ', '', re.sub(' ₽', '', price))

        item['code'] = han_code
        item['name'] = response.xpath('//h1[@class = "pdp-header__title page-title"]/text()').get()
        item['shop'] = response.xpath(
            '//div[@class = "pdp-sales-block__merchant"]//span//a[@class="pdp-offer-block__merchant-link"]/text()').get()
        item['price'] = handle_price
        item['product_url'] = response.url
        yield item


