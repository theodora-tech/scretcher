import scrapy

from scrapy.selector import Selector

class PortfolioCompaniesSpider(scrapy.Spider):
    name = "portfolio_companies"

    def start_requests(self):
        urls = [
            "https://eqtgroup.com/current-portfolio/",
            "https://eqtgroup.com/current-portfolio/divestments/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for company_item in response.xpath("//ul[@class='sm:border-t sm:border-neutral-light']/li"):
            keys = company_item.xpath("div[2]/div/ul/li/span[1]/node()").getall()
            values = company_item.xpath("div[2]/div/ul/li/span[2]/node()").getall()
            company_data = {key.lower(): value for key, value in zip(keys, values)}
            company_data["fund"] = Selector(text=company_data["fund"]).xpath(".//ul/li/a/text()").getall()
            company_data["company_name"] = company_item.css("span.inline-block").xpath("text()").get()

            yield company_data