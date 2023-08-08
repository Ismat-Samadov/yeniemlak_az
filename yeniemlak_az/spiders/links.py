import scrapy


class LinksAndPhoneNumbersSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["yeniemlak.az"]
    start_urls = [
        'https://yeniemlak.az/elan/axtar?emlak=1&elan_nov=1&seher%5B%5D=0&metro%5B%5D=0&qiymet=&qiymet2=&mertebe=&mertebe2=&otaq=&otaq2=&sahe_m=&sahe_m2=&sahe_s=&sahe_s2=&page=1'
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,  # 1 second between requests

        'DOWNLOAD_DELAY': 1.0  # Limit concurrent requests to 1
    }

    def parse(self, response):
        # Extract and yield the hrefs on the current page
        hrefs = response.css('.list a:first-child[class="detail"]::attr(href)').getall()
        for href in hrefs:
            yield scrapy.Request(url=response.urljoin(href), callback=self.parse_details, meta={"href": href})

        # Extract the next page link and follow it
        next_page_relative = response.css('.pagination a:last-child::attr(href)').get()
        if next_page_relative:
            next_page_absolute = response.urljoin(next_page_relative)
            yield scrapy.Request(url=next_page_absolute, callback=self.parse)

    def parse_details(self, response):
        href = response.request.meta['href'],
        phone_numbers = response.css('div.tel img::attr(src)').getall()
        for phone_number in phone_numbers:
            yield {
                "href": href,
                "phone_number": phone_number
            }
