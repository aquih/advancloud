# -*- encoding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import requests
import logging
import csv
import io

class ProductTemplate(models.Model):
    _inherit = 'product.template'
