import scrapy


class LinksAndPhoneNumbersSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["yeniemlak.az"]
    start_urls = [
        'https://yeniemlak.az/elan/axtar?elan_nov=1&emlak=0&menzil_nov=&qiymet=&qiymet2=&mertebe=&mertebe2=&otaq=&otaq2=&sahe_m=&sahe_m2=&sahe_s=&sahe_s2='
    ]

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
        href = response.request.meta['href']

        data = {
            "href": f'yeniemlak.az{href}',
            "price": None,
            "view_counts": None,
            "date": None,
            "id": None,
            "property_category": None,
            "room_count": None,
            "area": None,
            "doc_type": None,
            "flat": None,
            "address": None,
            "address_2": None,
            "description": None,
            "check": None,
            "owner_number": None,
            "owner_name": None,
            "owner_category": None

        }

        try:
            data["price"] = response.css('.title price::text').get()
        except Exception as price_error:
            self.logger.error(f"Error while extracting price: {price_error}")

        try:
            details = response.css('titem b::text').getall()[:3]
            data["view_counts"], data["date"], data["id"] = details
        except Exception as details_error:
            self.logger.error(f"Error while extracting details: {details_error}")

        try:
            data["property_category"] = response.css('.box emlak::text').get()
        except Exception as category_error:
            self.logger.error(f"Error while extracting property category: {category_error}")

        try:
            values = response.css('.params b::text').getall()[:5]
            data["room_count"], data["area"], data["doc_type"], data["flat"], data["address"], data[
                "address_2"] = values
        except Exception as room_error:
            self.logger.error(f"Error while extracting room count: {room_error}")
        try:
            data["description"] = response.css('.text::text').getall()
        except Exception as description_error:
            self.logger.error(f"Error while extracting room count: {description_error}")

        try:
            data["check"] = response.css('.check::text').getall()
        except Exception as check_error:
            self.logger.error(f"Error while extracting phone numbers: {check_error}")
        try:
            data["owner_category"] = response.css('.elvrn::text').getall()
        except Exception as owner_category_error:
            self.logger.error(f"Error while extracting phone numbers: {owner_category_error}")
        try:
            data["owner_name"] = response.css('.ad::text').getall()
        except Exception as name_error:
            self.logger.error(f"Error while extracting room count: {name_error}")
        try:
            data["owner_number"] = response.css('.tel img::attr(src)').getall()
        except Exception as phone_error:
            self.logger.error(f"Error while extracting phone numbers: {phone_error}")

        yield data
