# This file is part of the sale_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool, PoolMeta

__all__ = ['SaleLine']
__metaclass__ = PoolMeta


class SaleLine:
    __name__ = 'sale.line'

    def update_prices(self):
        if hasattr(self, 'product'):
            self.discount = Decimal(0)
            res = super(SaleLine, self).update_prices()
            Product = Pool().get('product.product')
            gross_unit_price = Product.get_sale_price([self.product],
                    self.quantity or 0)[self.product.id]
            if gross_unit_price:
                res['gross_unit_price'] = gross_unit_price.quantize(
                    Decimal(1) / 10 ** self.__class__.unit_price.digits[1])
                discount = 1 - (res['unit_price'] /
                     res['gross_unit_price'])
                res['discount'] = Decimal("%0.4f" % (discount))
        else:
            res = super(SaleLine, self).update_prices()
        return res
