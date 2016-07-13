import scrapy
_trojanTypeList = ('backdoor', 'exploit', 'rootkit', 'adware', 'trojan', 'trojan-banker', 'trojan-ddos', 'trojan-downloader', 'trojan-dropper', 'trojan-fakeav', 'trojan-gamethief ', 'trojan-im', 'trojan-ransom', 'trojan-sms', 'trojan-spy', 'trojan-mailfinder', 'trojan-arcbomb', 'trojan-clicker', 'trojan-notifier', 'trojan-proxy', 'trojan-psw')

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
        virusName = content[0].lower()
        virusType = virusName.split('.')[0]
        if virusType in _trojanTypeList:
            yield {
                'name': virusName,
                'type': virusType,
                'time': content[1],
                'grade': content[2],
                'url': response.url }
