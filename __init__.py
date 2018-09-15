# This file is part of the sale_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale
from . import invoice


def register():
    Pool.register(
        sale.SaleLine,
        invoice.InvoiceLine,
        module='sale_discount_visible', type_='model')
