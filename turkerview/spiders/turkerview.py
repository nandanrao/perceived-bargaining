from scrapy import Spider, Request

class TurkerviewSpider(Spider):
    name = 'turkerview'
    start_urls = ['https://turkerview.com/requesters/?id=A997L0DDC5EAE#']

    def parse(self, response):
        links = response.css('div.panel-body div.row #user-info .userText a ::attr(href)').extract()
        for url in links:
            yield Request(url = response.urljoin(url), callback = self.parse_profile)

    def parse_profile(self, response):
        reviews = response.xpath("//div[contains(h3, 'Latest Reviews')]/div")
        for r in reviews:
            wage_node = r.xpath(".//h4[contains(small, 'hour')]/text()").extract()
            wage = [i.strip() for i in wage_node if i.strip()][0]
            user = response.css('h3.panel-title ::text').extract_first()
            yield { 'wage': wage, 'user': user }
        # continue to more pages...
