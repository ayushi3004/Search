import scrapy
from scrapy.crawler import CrawlerProcess
# Crawl and parse the Hindu.
# Extract relevant info
# Current imp tags:
# section, headline, create date, publish date, modified date, news_keywords, intro, body, ld json schemas

class HinduSpider(scrapy.Spider):
    name = "scrape_hd_all"
    allowed_domains = ['thehindu.com']
    start_urls = ['https://www.thehindu.com/']

    def start_requests(self):
        url = "https://www.thehindu.com/news/national/?page={}"

        link_urls = [url.format(i) for i in range(1,2)]
        for link in link_urls:
            yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):
        top_stories_urls = []
        for i in range(1,7):
            url = response.xpath(f'//*[@id="section_3"]/div[2]/div/div[2]/div[{i}]/div/div/a/@href').get()
            top_stories_urls.append(url)
        return ','.join(top_stories_urls)

    def main(self):
        process = CrawlerProcess()
        process.crawl(HinduSpider)
        process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
        HinduSpider().main()






