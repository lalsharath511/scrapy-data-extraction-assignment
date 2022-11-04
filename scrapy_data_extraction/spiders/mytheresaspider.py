import scrapy

class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        for link in response.css('li.item a::attr(href)'):
            try:
               yield response.follow(link.get(), callback=self.parse_products)
            except:
                continue
          
        # next_page=response.css('li.next').css('a').attrib['href']
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
    def parse_products(self, response):
        product = response.css('div.main')
        # sizes = response.css('ul.sizes span::text').getall()
        # for size in sizes:
        #     size.strip(" ")
        
        # yield {
        #     'brand':product.css('a.text-000000::text').get(),
        #     'product_name':product.css('span.pb2.pa1-rmm-name::text').get(),
        #     'listing_price':product.css('span.price::text').get(),
        #     'product_id':product.css('span.h1::text').get()
        # }
        yield {
                "breadcrumbs":response.css('div.breadcrumbs span::text').getall(),
                "image_url":response.css('img.gallery-image ::attr(src)').get(),
                "brand": product.css('a.text-000000::text').get(),
                "product_name": product.css('span.pb2.pa1-rmm-name::text').get(),
                "listing_price": product.css('span.price::text').get(),
                "offer_price": "€ 559",
                "discount": "30% off",
                "product_id": product.css('span.h1::text').get(),
                "sizes": response.css('ul.sizes span::text').getall(),
                "description":product.css('span.h1::text').get(),
                "other_images":response.css('img.gallery-image ::attr(data-src)').getall()
                }

