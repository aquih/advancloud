# -*- encoding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
import io
import random

from epc.schemes import SGTIN

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_epc(self, serial=None):
        self.ensure_one()
        if self.barcode:
            sgtin = SGTIN()
            s = random.randint(1,99999999999)
            if serial:
                s = serial
            
            sgtin.decode_gtin(self.barcode, 6, serial_number=s)
            sgtin.filter(1)

            return ('%x' % sgtin).upper()
        else:
            return ''
