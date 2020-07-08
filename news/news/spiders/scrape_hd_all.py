import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from news.news.spiders.scrape_hd import HinduArticleSpider
from scrapy.utils.log import configure_logging

# Crawl and parse the Hindu listing page.
# Extract link for each news article

class HinduListingSpider(scrapy.Spider):
    name = "scrape_hd_all"
    allowed_domains = ['thehindu.com']
    start_urls = ['https://www.thehindu.com/']

    def __init__(self, section="national" , *args, **kwargs):
        super(HinduListingSpider, self).__init__(*args, **kwargs)
        self.section = section
        self.log('Section: %s' % self.section)

    def start_requests(self):
        url = "https://www.thehindu.com/news/" + self.section + "/?page={}"
        link_urls = [url.format(i) for i in range(1, 3)]
        for link in link_urls:
            yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):
        filename = '/Users/ayushisharma/projects/Search/news/news/resources/hindu-urls-{}.txt'.format(self.section)
        f = open(filename, 'a')
        for i in range(1, 7):
            url = response.xpath(f'//*[@id="section_3"]/div[2]/div/div[2]/div[{i}]/div/div/a/@href').get()
            f.write(url + "\n")

    @defer.inlineCallbacks
    def crawl(self):
        configure_logging()
        runner = CrawlerRunner()
        yield runner.crawl(HinduListingSpider)
        yield runner.crawl(HinduArticleSpider, self.section)
        reactor.stop()

    def main(self):
        self.crawl()
        reactor.run()


if __name__ == "__main__":
    HinduListingSpider().main()
