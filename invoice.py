# This file is part of the sale_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['InvoiceLine']
__metaclass__ = PoolMeta


class InvoiceLine:
    __name__ = 'account.invoice.line'

    def update_prices_visible_discount(self):
        if not hasattr(self, 'product') or not hasattr(self, 'invoice'):
            return {}
        with Transaction().set_context({
                'price_list': self.invoice.party.sale_price_list,
                'customer': self.invoice.party.id,
                }):
            Product = Pool().get('product.product')
            gross_unit_price = self.gross_unit_price
            discount = Decimal(0)
            unit_price = Product.get_sale_price([self.product],
                    self.quantity or 0)[self.product.id]
            if unit_price:
                unit_price_digits = self.__class__.unit_price.digits[1]
                discount_digits = self.__class__.discount.digits[1]
                unit_price = unit_price.quantize(
                    Decimal(str(10.0 ** -unit_price_digits)))
                discount = 1 - (unit_price / gross_unit_price)
                discount = discount.quantize(
                    Decimal(str(10.0 ** -discount_digits)))
            return {
                'gross_unit_price': gross_unit_price,
                'discount': discount,
                'unit_price': unit_price,
                }

    def on_change_product(self):
        res = super(InvoiceLine, self).on_change_product()
        invoice_type = self.invoice_type or self.invoice and self.invoice.type
        if (invoice_type in ('out_invoice', 'out_credit_note') and
                'gross_unit_price' in res):
            self.gross_unit_price = res['gross_unit_price']
            res.update(self.update_prices_visible_discount())
        return res

    @fields.depends('product', 'quantity', 'invoice_type', 'party', 'invoice',
        '_parent_invoice.type', '_parent_invoice.party')
    def on_change_quantity(self):
        res = {}
        invoice_type = self.invoice_type or self.invoice and self.invoice.type
        if invoice_type in ('out_invoice', 'out_credit_note'):
            res = super(InvoiceLine, self).on_change_product()
            if 'gross_unit_price' in res:
                self.gross_unit_price = res['gross_unit_price']
                res.update(self.update_prices_visible_discount())
        return res
