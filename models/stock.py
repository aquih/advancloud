# -*- encoding: utf-8 -*-

from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError, ValidationError

class Stock(models.Model):
    _name = 'advancloud.stock'
    _rec_name = 'code'
    _order = 'date desc'
    _check_company_auto = True

    code = fields.Char('Code')
    epc = fields.Integer('# EPC')
    sku = fields.Integer('# SKU')
    date = fields.Datetime('Date')
    company_id = fields.Many2one('res.company', string='Company', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True, check_company=True)
    location_id = fields.Many2one('stock.location', string='Location', required=True, check_company=True)
