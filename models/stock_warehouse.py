# -*- encoding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import requests
import logging
import csv
import io

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    shop_id_advancloud = fields.Char('Shop ID AdvanCloud')