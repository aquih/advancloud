# -*- encoding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import requests
import logging
import csv
import io

class StockLocation(models.Model):
    _inherit = 'stock.location'

    zone_id_advancloud = fields.Char('Zone ID AdvanCloud')