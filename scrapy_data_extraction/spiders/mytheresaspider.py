import scrapy

class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        for products in response.css('li.item'):
            yield{
                'link': products.css('a.product-image').attrib['href'],
            }
        next_page=response.css('li.next').css('a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)