# -*- encoding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import logging

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    inventory_advancloud = fields.Char('Inventory AdvanCloud')

    @api.model
    def _get_inventory_fields_create(self):
        return super()._get_inventory_fields_create() + ['inventory_advancloud']
