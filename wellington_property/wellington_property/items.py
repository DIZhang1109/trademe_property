# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field


class WellingtonPropertyItem(Item):
    # Location
    city = Field()
    suburb = Field()
    address = Field()

    # Property type
    type = Field()

    # Price and RV price
    rv_price = Field()
    price = Field()

    # Land area & floor area
    land_area = Field()
    floor_area = Field()

    # Bedroom & bathroom amounts
    bedroom = Field()
    bathroom = Field()

    # TradeMe URL
    url = Field()
