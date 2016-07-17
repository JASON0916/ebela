# -*- coding: utf-8 -*-

import os
import yaml
from scrapy.spiders import CrawlSpider
from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from ebay.items import EbayProduct

# http://www.ebay.com/sch/Computer-Components-Parts/175673/i.html?LH_Sold=1&LH_Complete=1&LH_LocatedIn=3&_pppn=r1&scp=ce0&_ipg=200
URL_TEMPLATE = 'http://www.ebay.com/sch/{section}/{section_id}/i.html?' \
               'LH_Sold=1' \
               '&LH_Complete=1' \
               '&LH_LocatedIn={location}' \
               '&_pppn=r1' \
               '&scp=ce0&_ipg=200'

PATH = '/'.join(os.path.abspath('EbaySpider.py').split('/')[:-3])
YAML_PATH = os.path.join(PATH, 'spider_target.yaml')

def get_start_urls(path=PATH):
    yaml_content = yaml.load(open(path, 'rb'))
    val = [section[:] + [location] for section in yaml_content.get('section')
           for location in yaml_content.get('location')]
    url_map = map(lambda x: dict(zip(['section', 'section_id', 'location'], x)), val)
    return list(set(URL_TEMPLATE.format(**data) for data in url_map))


class EbaySpider(CrawlSpider):
    name = "ebay"
    allowed_domains = ["http://www.ebay.com"]
    start_urls = get_start_urls()

    def parse(self, response):
        for res in response.xpath('//w-root//ul[@id="ListViewInner"]/li'):
            item = EbayProduct()
            item['href'] = res.xpath('h3/a/@href').extract()[0]
            item['picture'] = res.xpath('div/div[@class="lvpicinner full-width picW"]//img/@src').extract()[0]
            item['name'] = res.xpath('h3/a/text()').extract()[0]
            item['price_unit'] = res.xpath('ul/li[@class="lvprice prc"]/span/b/text()').extract()[0]
            item['price'] = filter(lambda x: x, res.xpath('ul/li[@class="lvprice prc"]/span/text()').re('\S*'))[0]
            item['create_date'] = res.xpath('ul[@class="lvdetails left '
                                            'space-zero full-width"]/li/span/span/text()').extract()[0]
            request = Request(item['href'],
                              callback=self.parse_detail,
                              errback=self.error_handle,
                              dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        ship_info = response.xpath(
                '//span[@id="fshippingCost"]/span/text()'
            ).extract()
        try:
            item['shipping_unit'], item['shipping_price'] = ship_info[0].split()
        except ValueError, IndentationError:
            item['shipping_unit'] = ''
            item['shipping_price'] = 0.0
        item['seller'] = response.xpath('//div[@class="mbg vi-VR-margBtm3"]/a/span/text()').extract()[0]
        item['seller_href'] = response.xpath('//div[@class="mbg vi-VR-margBtm3"]/a/@href').extract()[0]
        return item

    def error_handle(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
