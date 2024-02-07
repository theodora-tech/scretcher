from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://eqtgroup.com/current-portfolio/funds/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"scraped-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")