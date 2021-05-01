# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.item import Field, Item

from .processors import get_author, get_times, parse_content


class ZhscCrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义爬取数据的结构，并且对字段内容进行处理
    title = Field(input_processor=MapCompose(str.strip, stop_on_none=True), output_processor=TakeFirst())
    times = Field(input_processor=MapCompose(get_times, stop_on_none=True), output_processor=TakeFirst())
    author = Field(input_processor=MapCompose(get_author, stop_on_none=True), output_processor=TakeFirst())
    content = Field(input_processor=MapCompose(parse_content, stop_on_none=True), output_processor=Join(''))
