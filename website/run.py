from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.dmoz_spider import DmozSpider

settings = get_project_settings()
process = CrawlerProcess(settings=settings)

process.crawl(DmozSpider)

process.start()