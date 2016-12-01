"""
This spider is used to crawl property information in Wellington Region,
including useful information like location, price, area and so on...
"""
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from wellington_property.items import WellingtonPropertyItem


class PropertySpider(CrawlSpider):
    name = 'property_hunt'
    allowed_domains = ['trademe.co.nz']
    start_urls = ['http://www.trademe.co.nz/property/residential-property-for-sale']

    rules = (
        Rule(LinkExtractor(allow=('auction-\d*\.htm',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = WellingtonPropertyItem()
        sel = Selector(response)

        # Filter the data only from city Wellington
        if len(sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()) == 4:
            city = sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()[3].strip()
        else:
            city = sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()[2].strip()

        if city == 'Wellington':
            # Location
            item['city'] = city

            if len(sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()) == 4:
                item['suburb'] = sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()[2]
                item['address'] = sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()[0] + ' ' + \
                    sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()[1]
            else:
                item['suburb'] = sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()[1]
                item['address'] = sel.xpath('//*[@id="ListingAttributes"]/tr[1]/td/text()').extract()[0]

            # Property type
            item['type'] = sel.xpath('//*[@id="ListingAttributes"]/tr[3]/td/text()').extract()[0]

            # Price and RV price
            item['rv_price'] = sel.xpath('//*[@id="ListingAttributes"]/tr[6]/td/text()').extract()[0]
            item['price'] = sel.xpath('//*[@id="ListingAttributes"]/tr[7]/td/text()').extract()[0]

            # Land area & floor area
            item['land_area'] = sel.xpath('//*[@id="ListingAttributes"]/tr[5]/td/text()').extract()[0]
            item['floor_area'] = sel.xpath('//*[@id="ListingAttributes"]/tr[4]/td/text()').extract()[0]

            # Bedroom & bathroom amounts
            item['bedroom'] = sel.xpath('//*[@id="ListingAttributes"]/tr[2]/td/text()').extract()[0].split(',')[0]
            item['bathroom'] = sel.xpath('//*[@id="ListingAttributes"]/tr[2]/td/text()').extract()[0].split(',')[1]

            # TradeMe URL
            item['url'] = response.url

        return {k: v.strip() for k, v in item.items()}