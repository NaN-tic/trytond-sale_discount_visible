# This file is part of the sale_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.pool import Pool
from .sale import *
from .invoice import *


def register():
    Pool.register(
        SaleLine,
        InvoiceLine,
        module='sale_discount_visible', type_='model')
