import scrapy
from scrapy.http import HtmlResponse
from unsplash.items import UnsplashItem
from scrapy.loader import ItemLoader

class UnsplashimgSpider(scrapy.Spider):
    name = "unsplashimg"
    allowed_domains = ["unsplash.com"]

    def __init__(self, query=None, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        if self.query:
            self.start_urls = [f"https://unsplash.com/s/photos/{self.query}"]
        else:
            self.start_urls = ["https://unsplash.com"] # Default URL if no query


    def parse(self, response: HtmlResponse):
        photo_links = response.xpath('//a[@itemprop="contentUrl"]/@href').getall()
        for link in photo_links:
            yield response.follow(link, self.parse_site)

    def parse_site(self, response: HtmlResponse):
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.add_xpath('name', '//h1[@class="vev3s"]/text()', re='(.*)') #Added re to remove extra whitespace
        loader.add_xpath('country', '//span[@class="IwfFI jhw7y dRzrK uoMSP"]/text()', re='(.*)') #Added re to remove extra whitespace
        loader.add_xpath('date', '//time/@datetime')
        loader.add_xpath('tag_title', '//div[@class="TQ1ci BOC6f"]/div[@class="zb0Hu atI7H"]//@title', re='(.*)')
        loader.add_xpath('tag_href', '//div[@class="TQ1ci BOC6f"]/div[@class="zb0Hu atI7H"]//@href', re='(.*)')
        loader.add_value('url', response.url)
        loader.add_xpath('photos', '//img/@srcset | //img/@src')
        yield loader.load_item()
