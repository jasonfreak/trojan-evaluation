import scrapy

class StackOverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    start_urls = [ 'http://www.micropoint.com.cn/NewVirus/NewVirus/index_%d.html' % i for i in range(1, 33) ]
    
    def parse(self, response):
        for href in response.css('.name a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback = self.parse_virus)

    def parse_virus(self, response):
        content = response.css('.div_contenttext p::text').extract()
        content = map(lambda x: x.strip(), content)
        content = filter(lambda x: len(x) > 0, content)
        if content[0][0:6] == 'Trojan':
            yield {
                'name': content[0],
                'time': content[1],
                'grade': content[2],
                'url': response.url }
