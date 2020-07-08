import scrapy
from scrapy.crawler import CrawlerProcess
# Crawl and parse the Hindu listing page.
# Extract link for each news article

class HinduListingSpider(scrapy.Spider):
    name = "scrape_hd_all"
    allowed_domains = ['thehindu.com']
    start_urls = ['https://www.thehindu.com/']

    def start_requests(self):
        url = "https://www.thehindu.com/news/national/?page={}"

        link_urls = [url.format(i) for i in range(1,10)]
        for link in link_urls:
            yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):
        # top_stories_urls = []
        filename = '/Users/ayushisharma/projects/Search/news/news/resources/hindu-urls.txt'
        f = open(filename, 'w')
        for i in range(1,7):
            url = response.xpath(f'//*[@id="section_3"]/div[2]/div/div[2]/div[{i}]/div/div/a/@href').get()
            f.write(url + "\n")
            # top_stories_urls.append(url)
        # return ','.join(top_stories_urls)

    def main(self):
        process = CrawlerProcess()
        process.crawl(HinduListingSpider)
        process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
        HinduListingSpider().main()
