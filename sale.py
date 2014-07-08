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
        if hasattr(self, 'product') and self.discount == Decimal(0):
            self.discount = Decimal(0)
            res = super(SaleLine, self).update_prices()
            Product = Pool().get('product.product')
            gross_unit_price = Product.get_sale_price([self.product],
                    self.quantity or 0)[self.product.id]
            if gross_unit_price:
                unit_price_digits = self.__class__.gross_unit_price.digits[1]
                discount_digits = self.__class__.discount.digits[1]
                res['gross_unit_price'] = gross_unit_price.quantize(
                    Decimal(str(10.0 ** -unit_price_digits)))
                discount = 1 - (res['unit_price'] / res['gross_unit_price'])
                res['discount'] = discount.quantize(
                    Decimal(str(10.0 ** -discount_digits)))
        else:
            res = super(SaleLine, self).update_prices()
        return res
