import scrapy
from scrapy.crawler import CrawlerProcess
from news.news.spiders.scrape_hd_all import HinduListingSpider
# Spin off spiders for all sections of Hindu

class MasterSpider(scrapy.Spider):
    name = "master"

    def main(self):
        process = CrawlerProcess()
        process.crawl(HinduListingSpider, section = "national")
        process.start()

if __name__ == "__main__":
        MasterSpider().main()
