# -*- encoding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import logging

class StockLocation(models.Model):
    _inherit = 'stock.location'

    zone_id_advancloud = fields.Char('Zone ID')
    decode_epc_advancloud = fields.Text('Decode EPC', help='The variable "epc" has the EPC value. You can access the regular expression library with the "re" variable. Assign the variable product_id with the desired value after decoding the EPC.')