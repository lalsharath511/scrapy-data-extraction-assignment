import scrapy
import time

class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        for link in response.css('li.item a::attr(href)'):
            try:
               yield response.follow(link.get(), callback=self.parse_products)
            except:
                continue
        time.sleep(10) 
        next_page=response.css('li.next').css('a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    def parse_products(self, response):
        product = response.css('div.main')
        a=response.css('li.pa1-rmm::text').getall()
        a=' '.join(a)
        b=str(product.css('p.pa1-rmm.product-description::text').get())
        description=b+a
        



        # sizes = response.css('ul.sizes span::text').getall()
        # for size in sizes:
        #     size.strip(" ")
        breadcrumbs=response.css('div.breadcrumbs span::text').getall()
        sizes_details=response.css('ul.sizes span::text').getall()
        sizes=[]

        for size in sizes_details:
            size=size.strip(" ")
            size=size.split("/")
            if size[1]=="":
                sizes.append(size[0].strip(" "))
            else:
                for i in size:
                    sizes.append(i.strip(" "))
        listing_price=response.css('span.regular-price span.price::text').get()
        if listing_price==None:
            listing_price=response.css('p.old-price span.price::text').get() 
       

        yield {
                "breadcrumbs":breadcrumbs[0:-1],
                "image_url":f"https:{response.css('img.gallery-image ::attr(src)').get()}",
                "brand": product.css('a.text-000000::text').get(),
                "product_name": product.css('span.pb2.pa1-rmm-name::text').get(),
                "listing_price": listing_price,
                "offer_price": response.css('p.special-price span.price::text').get(),
                "discount": product.css('span.price-reduction-notice::text').get(),
                "product_id": response.css('span.h1::text').get()[-9:],
                "sizes": sizes,
                "description":description,
                "other_images":response.css('img.gallery-image ::attr(data-src)').getall()
                }

