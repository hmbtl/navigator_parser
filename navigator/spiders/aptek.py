# -*- coding: utf-8 -*-
import scrapy 

class AptekSpider(scrapy.Spider):
  name = 'aptek'
  allowed_domains = ['navigator.az']
  start_urls = ['https://www.navigator.az/catalogue/16/40']

  def parse(self, response):
    for jobs in response.xpath('//div[@class="company-main mt-4"]'):
      url = jobs.xpath(".//h3[@class='company-name']/a/@href").get()
      yield scrapy.Request(response.urljoin(url), callback=self.parse_detail)

    next_page = response.xpath('//li[@class="page-item  pagination-active"]/following-sibling::li/a/@href').get()
    has_next = response.xpath('//li[@class="page-item  pagination-active"]/following-sibling::li').getall()

    if len(has_next) > 1:
     yield scrapy.Request(response.urljoin(next_page))

  def parse_detail(self, response):
    phones = []
    for phone in response.xpath('//span[@class="contact-text-call"]/text()').getall():
        phoneC = phone.strip();
        if phoneC:
            phones.append(phoneC)

    address = response.xpath('//span[@class="contact-text-location"]/text()').get().strip();
    address = ' '.join(address.split())
    name = response.xpath('//p[@class="contact-top-text"]/text()').get();


    # yield values
    yield {
      'url': response.url,
      'name': name,
      'address': address,
      'phone': phones
    }
