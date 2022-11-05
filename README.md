
![Logo](https://i.pinimg.com/originals/93/7f/b9/937fb93ba0cea82292f1af4ed827b347.png)


# Scrapy Data Extraction Assignment

This is a scrapy data extraction assignment where you need to use Scrapy Framework for data
extraction.



![GitHub last commit](https://img.shields.io/github/last-commit/lalsharath511/scrapy-data-extraction-assignment?style=plastic)
![GitHub repo size](https://img.shields.io/github/repo-size/lalsharath511/scrapy-data-extraction-assignment?style=plastic)


## Installation

  #### step 1

  Clone the project
```bash
   git clone https://github.com/lalsharath511/scrapy-data-extraction-assignment.git
```
 #### step 2
 Go to the project directory
```bash
   cd scrapy-data-extraction-assignment/
```
 #### step 3
 Install dependencies
```bash
   pip install -r requirements.txt
```
## Usage/Examples
### Crawling

Going through each of the URLs from the URL provided and going through
each and every page.

```python
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
```

### Parsing, Cleaning & Data Structuring
Parsing is to be done in the last depth, where we find product/person/
property details, all of the fields required.The extracted data should be cleaned properly and the data should be
structured in the specified format.

```python
      def parse_products(self, response):
        product = response.xpath("//div[@class='main']")

        sizes_details = product.xpath("//div[@class='product-shop'] //ul[@class='sizes'] //span/text()").getall()
        sizes = []
        for size in sizes_details:
            size = size.replace("/", " ").strip(" ").split("  ")
            for i in size:
                sizes.append(i)
        listing_price = product.xpath(
            "//div[@class='product-shop'] //span[@class='regular-price'] //span[@class='price']/text()").get()
        if listing_price == None:
            listing_price = product.xpath(
                "//div[@class='product-shop'] //p[@class='old-price'] //span[@class='price']/text()").get()

        yield {
            "breadcrumbs": product.xpath("//div[@class='breadcrumbs'] //span/text()").getall()[0:-1],
            "image_url": f"https:{product.css('img.gallery-image').xpath('@src').get()}",
            "brand": product.xpath("//a[@class='text-000000']/text()").get(),
            "product_name": product.xpath("//div[@class='product-name'] //span/text()").get(),
            "listing_price": listing_price,
            "offer_price": product.xpath(
                "//div[@class='product-shop'] //p[@class='special-price'] //span[@class='price']/text()").get(),
            "discount": product.xpath(
                "//div[@class='product-shop'] //span[@class='price-reduction-notice']/text()").get(),
            "product_id": product.xpath("//span[@class='h1']/text()").get()[-9:],
            "sizes": sizes,
            "description": (str(product.css('p.pa1-rmm.product-description::text').get())) + ' '.join(
                product.xpath("//li[@class='pa1-rmm']/text()").getall()),
            "other_images": product.css('img.gallery-image').xpath('@data-src').getall()
        }

```



## Running Tests

To run tests, run the following command

```bash
  scrapy crawl mytheresa
```
To extract data in JSON file format

```bash
  scrapy crawl mytheresa -O filename.json
```
To extract data in CSV file format

```bash
  scrapy crawl mytheresa -O filename.csv
```


## Related

Here are some related projects

- [GaanaSongsInfoScrapingProject](https://github.com/lalsharath511/GaanaSongsInfoScrapingProject)

