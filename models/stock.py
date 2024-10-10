# -*- encoding: utf-8 -*-

from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError, ValidationError

class Stock(models.Model):
    _name = 'advancloud.stock'
    _rec_name = 'code'

    code = fields.Char('Code')