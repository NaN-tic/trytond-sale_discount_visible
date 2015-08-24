# This file is part of the sale_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool, PoolMeta
from trytond.model import fields

__all__ = ['SaleLine']
__metaclass__ = PoolMeta


class SaleLine:
    __name__ = 'sale.line'

    def update_prices_visible_discount(self):
        Product = Pool().get('product.product')

        unit_price = self.gross_unit_price
        unit_price_wo_round = self.gross_unit_price_wo_round
        discount = Decimal(0)

        prices = Product.get_sale_price([self.product], self.quantity or 0)
        gross_unit_price = prices[self.product.id]

        if gross_unit_price:
            unit_price_digits = self.__class__.gross_unit_price.digits[1]
            discount_digits = self.__class__.discount.digits[1]
            gross_unit_price = gross_unit_price.quantize(
                Decimal(str(10.0 ** -unit_price_digits)))
            discount = 1 - (unit_price_wo_round / gross_unit_price)
            discount = discount.quantize(
                Decimal(str(10.0 ** -discount_digits)))

        self.gross_unit_price = gross_unit_price
        self.discount = discount
        self.unit_price = unit_price

    @fields.depends('gross_unit_price', 'gross_unit_price_wo_round')
    def on_change_product(self):
        super(SaleLine, self).on_change_product()
        if not self.product:
            return
        if self.gross_unit_price:
            self.gross_unit_price_wo_round = self.gross_unit_price_wo_round
            self.update_prices_visible_discount()

    @fields.depends('gross_unit_price', 'gross_unit_price_wo_round')
    def on_change_quantity(self):
        super(SaleLine, self).on_change_quantity()
        if self.gross_unit_price:
            self.gross_unit_price_wo_round = self.gross_unit_price_wo_round
            self.update_prices_visible_discount()
