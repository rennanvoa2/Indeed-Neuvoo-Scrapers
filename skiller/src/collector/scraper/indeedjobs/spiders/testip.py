# -*- coding: utf-8 -*-
import scrapy


class IndeedUsSpider(scrapy.Spider):
    name = 'ipscraper'
    start_urls = [f'https://www.expressvpn.com/what-is-my-ip']
    allowed_domains = ['www.expressvpn.com']

    def parse(self, response):
        ip = response.xpath("//p[@class='ip-address']").get()
        yield {"ip":ip}