import logging
from ebay.models.EbayProduct import EbayProduct
from ebay.models import DBSession
from sqlalchemy.exc import SQLAlchemyError
from scrapy.exceptions import DropItem


class Pipeline(object):
    session = None

    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        try:
            data = EbayProduct(name=item['name'],
                               picture=item['picture'],
                               create_date=item['create_date'],
                               price=item['price'],
                               price_unit=item['price_unit'],
                               seller=item['seller'],
                               seller_href=item['seller_href'],
                               shipping_price=item['shipping_price'],
                               shipping_unit=item['shipping_unit'],
                               href=item['href'])
        except KeyError:
            raise DropItem

        try:
            self.session.add(data)
            self.session.commit()
            logging.info('add data {}'.format(data))
        except (SQLAlchemyError, Exception) as exc:
            logging.error(exc.message)
            self.session.rollback()

    def close_spider(self, spider):
        self.session.close()
