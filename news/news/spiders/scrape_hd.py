import scrapy
from scrapy.crawler import CrawlerProcess
# Crawl and parse the Hindu.
# Extract relevant info
# Current imp tags:
# section, headline, create date, publish date, modified date, news_keywords, intro, body, ld json schemas

class HinduSpider(scrapy.Spider):
    name = "scrape_hd"
    count = 1

    def start_requests(self):
        urls = [
            'https://www.thehindu.com/news/international/hip-hop-musician-kanye-west-announces-white-house-bid/article31993131.ece?homepage=true',
            'https://www.thehindu.com/news/international/days-after-demarche-china-doubles-down-on-claims-on-eastern-bhutan-boundary/article31993470.ece?homepage=true'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = '/Users/ayushisharma/projects/Search/news/news/spiders/results/hindu-%s.txt' % HinduSpider.count
        HinduSpider.count = HinduSpider.count + 1
        with open(filename, 'w') as f:
            useful_data = self.extract(response)
            # for itemlist in useful_data:
            f.write("\n".join(useful_data))
        self.log('Saved file %s' % filename)

    def extract(self, response):
        useful_data = []
        section = response.css('.section-name::text').get()
        published_date = response.xpath("//meta[@name='publish-date']/@content").get()
        created_date = response.xpath("//meta[@name='created-date']/@content").get()
        modified_date = response.xpath("//meta[@name='modified-date']/@content").get()
        news_keywords = response.xpath("//meta[@name='news_keywords']/@content").get()
        headline = response.css('title::text').get() # response.selector.xpath('//title/text()').get()
        intro = response.css('.intro::text').get()

        # div = response.selector.css('div[id*="content-body"]').get()
        # for p in div.xpath('.//p'):
        #     print(p.xpath('.//text()').extract())
        content_tag = response.css('div[id*="content-body"]')
        content_strs = [
            ' '.join(
                line.strip()
                for line in p.xpath('.//text()').extract()
                if line.strip()
            )
            for p in content_tag.xpath('.//p')
        ]
        body = ' '.join(filter(None, content_strs))
        ld_json_schemas = "\n".join(response.xpath("//script[@type='application/ld+json']//text()").extract())
        useful_data.extend([section, published_date, created_date, modified_date, news_keywords, headline, intro, body, ld_json_schemas])
        return useful_data

    def main(self):
        process = CrawlerProcess()
        process.crawl(HinduSpider)
        process.start() # the script will block here until the crawling is finished

if __name__ == "__main__":
        HinduSpider().main()






