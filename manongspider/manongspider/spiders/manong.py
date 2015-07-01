#coding=utf8

import scrapy
from manongspider.items import ManongItem

class ManongSpider(scrapy.Spider):
    name = 'manong'
    start_urls = ['http://weekly.manong.io/issues/']

    def parse(self, resp):
        for a in resp.xpath('//div[@class="issue"]/h4/a'):
            url = a.css('a::attr(href)')[0].extract()
            _issue = int(a.re(ur'第(\d+)期')[0])
            item = ManongItem()
            item['issue'] = _issue
            yield scrapy.Request(url,
                                 meta={'item': item},
                                 callback=self.parse_issue)

    def parse_issue(self, resp):
        for h in resp.xpath('//h4'):
            _title = h.xpath('a/text()')[0].extract()
            _link = h.css('a::attr(href)')[0].extract()
            _desc = u' '.join(h.xpath('following::p[1]//text()').extract())
            item = resp.request.meta['item']
            item['title'] = _title
            item['link'] = _link
            item['desc'] = _desc
            yield item
