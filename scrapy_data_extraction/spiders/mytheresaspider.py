import scrapy
import time


class MytheresaSpider(scrapy.Spider):
    name = 'mytheresa'
    start_urls = ['https://www.mytheresa.com/int_en/men/shoes.html']

    def parse(self, response):
        for link in response.css('li.item a').xpath("@href"):
            try:
                yield response.follow(link.get(), callback=self.parse_products)
            except:
                continue
        time.sleep(10)
        next_page = response.css('li.next a').xpath('@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_products(self, response):
        product = response.xpath("//div[@class='main']")

        sizes_details = product.xpath("//div[@class='product-shop'] //ul[@class='sizes'] //span/text()").getall()
        sizes = []
        for size in sizes_details:
            size=size.replace("/"," ").strip(" ").split("  ")
            for i in size:
                sizes.append(i)
        listing_price = product.xpath("//div[@class='product-shop'] //span[@class='regular-price'] //span[@class='price']/text()").get()
        if listing_price == None:
            listing_price = product.xpath("//div[@class='product-shop'] //p[@class='old-price'] //span[@class='price']/text()").get()

        yield {
            "breadcrumbs": product.xpath("//div[@class='breadcrumbs'] //span/text()").getall()[0:-1],
            "image_url": f"https:{product.css('img.gallery-image').xpath('@src').get()}",
            "brand": product.xpath("//a[@class='text-000000']/text()").get(),
            "product_name": product.xpath("//div[@class='product-name'] //span/text()").get(),
            "listing_price": listing_price,
            "offer_price": product.xpath("//div[@class='product-shop'] //p[@class='special-price'] //span[@class='price']/text()").get(),
            "discount":  product.xpath("//div[@class='product-shop'] //span[@class='price-reduction-notice']/text()").get(),
            "product_id": product.xpath("//span[@class='h1']/text()").get()[-9:],
            "sizes": sizes,
            "description": (str(product.css('p.pa1-rmm.product-description::text').get())) + ' '.join(product.xpath("//li[@class='pa1-rmm']/text()").getall()),
            "other_images": product.css('img.gallery-image').xpath('@data-src').getall()
        }
