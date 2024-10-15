# -*- encoding: utf-8 -*-

from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError, ValidationError

import requests
import re
import logging

class Stock(models.Model):
    _name = 'advancloud.stock'
    _rec_name = 'code'
    _order = 'date desc'
    _check_company_auto = True

    code = fields.Char('Code', index=True)
    epc = fields.Integer('# EPC')
    sku = fields.Integer('# SKU')
    date = fields.Datetime('Date')
    company_id = fields.Many2one('res.company', string='Company', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True, check_company=True)
    location_id = fields.Many2one('stock.location', string='Location', required=True, check_company=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', index=True, readonly=True, tracking=True)

    _sql_constraints = [
        ('uniq_name', 'unique(code)', 'This stock already exists.'),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done(self):
        if any(m.state == 'done' for m in self):
            raise UserError(_("You can't delete a done stock"))

    def create_inventories(self):
        for w in self:
            data = {
                'grant_type': 'password',
                'username': self.company_id.user_advancloud,
                'password': self.company_id.password_advancloud,
                'client_id': 'cloud'
            }
            r = requests.post('https://{}/advancloud/oauth/token'.format(self.company_id.url_advancloud), data=data)
            logging.warning(r.text)

            access_token = r.json()['access_token']

            headers = { 'Authorization': 'Bearer '+access_token }
            data = {
                'username': self.company_id.user_advancloud,
                'password': self.company_id.password_advancloud,
                'token': self.company_id.app_advancloud,
                'shop': self.warehouse_id.shop_id_advancloud,
                'reporttype': 'json',
            }
            r = requests.post('https://{}/advancloud/import/stock/download/{}'.format(self.company_id.url_advancloud, self.code), data=data, headers=headers)
            logging.warning(r.text)

            result = r.json()

            products = {}
            for data in result['data']:
                product_id = 0
                if 'productid' in data:
                    product_id = data['productid']
                elif self.location_id.decode_epc_advancloud:
                    loc = {}
                    exec(self.location_id.decode_epc_advancloud, { 'epc': data['epc'], 're': re }, loc)
                    product_id = loc['product_id']

                if product_id not in products:
                    products[product_id] = { 'product_id': int(product_id), 'location_id': self.location_id.id, 'inventory_quantity': 0 }
                products[product_id]['inventory_quantity'] += 1

            self.env['stock.quant'].with_context(inventory_mode=True).create(products.values())
            self.state = 'done'

        return self.env['stock.quant'].action_view_inventory()

    def button_draft(self):
        self.state = 'draft'