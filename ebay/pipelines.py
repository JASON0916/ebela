from ebay.models.EbayProduct import EbayProduct
from ebay.models import DBSession


class Pipeline(object):
    session = None

    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        EbayProduct.add(self.session,
                        name=item['name'],
                        picture=item['picture'],
                        create_date=item['create_date'],
                        price=item['price'],
                        price_unit=item['price_unit'],
                        seller=item['seller'],
                        seller_href=item['seller_href'],
                        shipping_price=item['shipping_price'],
                        shipping_unit=item['shipping_unit'],
                        href=item['href'])

    def close_spider(self, spider):
        self.session.close()
