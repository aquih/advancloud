# -*- encoding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
import io

from epc.schemes import SGTIN

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_epc(self, serial):
        self.ensure_one()
        if self.barcode:
            sgtin = SGTIN()
            sgtin.decode_gtin(self.barcode, 6, serial_number=serial)
            sgtin.filter(1)

            return ('%x' % sgtin).upper()
        else:
            return ''