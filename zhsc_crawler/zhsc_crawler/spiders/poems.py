import scrapy
from scrapy.loader import ItemLoader

from ..items import ZhscCrawlerItem
from ..processors import find_author_url


class PoemsSpider(scrapy.Spider):
    name = 'poems'
    allowed_domains = ['www.zhsc.net']
    start_urls = ['https://www.zhsc.net/Index/shi_more.html']

    def parse(self, response):
        """
        处理种子页
        """
        author = getattr(self, 'author', None)  # 从命令行传入的作者名字
        author_links = response.css('.ci_lei1>.ci_lei1>.ci_lei1_xuan>.ci_lei1_xuan2 a').getall()  # 当前页面中所有作者链接
        if author is not None:
            # 只对启动爬虫时传入的作者进行爬取
            for link in author_links:
                poems_list_page_url = find_author_url(link, author)
                if poems_list_page_url is not None:
                    yield response.follow(poems_list_page_url, self.parse_list)
        return ZhscCrawlerItem()

    def parse_list(self, response):
        """
        处理列表页
        """
        detail_urls = response.css('.zh_sou_jie>.zh_jie_con a::attr(href)').getall()  # 详情页地址
        for url in detail_urls:
            yield response.follow(url, self.parse_item)
        next_page_urls = response.css('.page a::attr(href)').getall()  # 其他列表页地址
        for url in next_page_urls:
            yield response.follow(url, self.parse_list)

    def parse_item(self, response):
        """
        处理详情页
        """
        loader = ItemLoader(item=ZhscCrawlerItem(), response=response)
        loader.add_css('title', '.zh_shi_xiang1>span::text,.zh_shi_xiang1>span>*::text')
        loader.add_css('times', '.zh_shi_xiang1>p::text')
        loader.add_css('author', '.zh_shi_xiang1>p::text')
        loader.add_css('content', '.zh_shi_xiang1>div::text,.zh_shi_xiang1>div>*::text')
        return loader.load_item()
