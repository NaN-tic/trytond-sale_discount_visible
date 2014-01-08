# This file is part of the sale_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['InvoiceLine']
__metaclass__ = PoolMeta


class InvoiceLine:
    __name__ = 'account.invoice.line'

    def update_prices(self):
        res = super(InvoiceLine, self).update_prices()
        if hasattr(self, 'product') and hasattr(self, 'invoice'):
            with Transaction().set_context({
                    'price_list': self.invoice.party.sale_price_list,
                    'customer': self.invoice.party.id,
                    }):
                Product = Pool().get('product.product')
                unit_price = Product.get_sale_price([self.product],
                    self.quantity or 0)[self.product.id]
                if unit_price:
                    res['unit_price'] = unit_price.quantize(
                        Decimal(1) / 10 ** self.__class__.unit_price.digits[1])
                    res['discount'] = 1 - (res['unit_price'] /
                        res['gross_unit_price'])
        return res
