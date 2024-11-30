from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.utils.reactor import install_reactor
from unsplash.spiders.unsplashimg import UnsplashimgSpider


if __name__ == '__main__':
    USER_AGENT = "jobparser (+http://www.yourdomain.com)"
    configure_logging()
    # settings = get_project_settings()
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    process = CrawlerProcess(get_project_settings())
    process.crawl(UnsplashimgSpider, query='ocean')
    process.start()