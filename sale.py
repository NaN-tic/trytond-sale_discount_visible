# This file is part of the sale_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool, PoolMeta

__all__ = ['SaleLine']
__metaclass__ = PoolMeta


class SaleLine:
    __name__ = 'sale.line'

    def update_prices_visible_discount(self):
        Product = Pool().get('product.product')
        unit_price = self.gross_unit_price
        unit_price_wo_round = self.gross_unit_price_wo_round
        discount = Decimal(0)
        gross_unit_price = Product.get_sale_price([self.product],
                self.quantity or 0)[self.product.id]
        if gross_unit_price:
            unit_price_digits = self.__class__.gross_unit_price.digits[1]
            discount_digits = self.__class__.discount.digits[1]
            gross_unit_price = gross_unit_price.quantize(
                Decimal(str(10.0 ** -unit_price_digits)))
            discount = 1 - (unit_price_wo_round / gross_unit_price)
            discount = discount.quantize(
                Decimal(str(10.0 ** -discount_digits)))
        return {
            'gross_unit_price': gross_unit_price,
            'discount': discount,
            'unit_price': unit_price,
            }

    def on_change_product(self):
        res = super(SaleLine, self).on_change_product()
        if 'gross_unit_price' in res:
            self.gross_unit_price = res['gross_unit_price']
            self.gross_unit_price_wo_round = res['gross_unit_price_wo_round']
            res.update(self.update_prices_visible_discount())
        return res

    def on_change_quantity(self):
        res = super(SaleLine, self).on_change_quantity()
        if 'gross_unit_price' in res:
            self.gross_unit_price = res['gross_unit_price']
            self.gross_unit_price_wo_round = res['gross_unit_price_wo_round']
            res.update(self.update_prices_visible_discount())
        return res
