# This file is part of the sale_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['InvoiceLine']


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    def update_prices_visible_discount(self):
        if not hasattr(self, 'product') or not hasattr(self, 'invoice'):
            return

        Product = Pool().get('product.product')

        with Transaction().set_context({
                'price_list': self.invoice.party.sale_price_list \
                    if self.invoice else self.party.sale_price_list,
                'customer': self.invoice.party.id \
                    if self.invoice else self.party.id,
                }):
            gross_unit_price = self.gross_unit_price_wo_round
            discount = Decimal(0)

            prices = Product.get_sale_price([self.product], self.quantity or 0)
            unit_price = prices[self.product.id]

            if unit_price:
                unit_price_digits = self.__class__.unit_price.digits[1]
                discount_digits = self.__class__.discount.digits[1]
                unit_price = unit_price.quantize(
                    Decimal(str(10.0 ** -unit_price_digits)))
                discount = 1 - (unit_price / gross_unit_price)
                discount = discount.quantize(
                    Decimal(str(10.0 ** -discount_digits)))

            self.discount = discount
            self.unit_price = unit_price

    @fields.depends('invoice_type', 'invoice', 'gross_unit_price',
        'gross_unit_price_wo_round')
    def on_change_product(self):
        super(InvoiceLine, self).on_change_product()
        if not self.product:
            return
        invoice_type = self.invoice_type or self.invoice and self.invoice.type
        if invoice_type == 'out' and self.gross_unit_price:
            self.gross_unit_price_wo_round = self.gross_unit_price_wo_round
            self.update_prices_visible_discount()

    @fields.depends('product', 'quantity', 'invoice_type', 'party', 'invoice',
        'gross_unit_price', 'gross_unit_price_wo_round', '_parent_invoice.type', '_parent_invoice.party')
    def on_change_quantity(self):
        super(InvoiceLine, self).on_change_product()
        invoice_type = self.invoice_type or self.invoice and self.invoice.type
        if invoice_type == 'out':
            if self.gross_unit_price:
                self.gross_unit_price_wo_round = self.gross_unit_price_wo_round
                self.update_prices_visible_discount()
