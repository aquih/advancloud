# -*- encoding: utf-8 -*-

from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError, ValidationError

import requests
import logging

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
                if not self.env['stock.quant'].search([('product_id','=',data['productid']), ('inventory_advancloud','=',result['properties']['code'])]):
                if data['productid'] not in products:
                    products[data['productid']] = { 'product_id': 26, 'location_id': self.location_id.id, 'inventory_quantity': 0, 'inventory_advancloud': result['properties']['code'] }
                products[data['productid']]['inventory_quantity'] += 1
            logging.warning(products.values())

            self.env['stock.quant'].with_context(inventory_mode=True).create(products.values())

        return self.env['stock.quant'].action_view_inventory()