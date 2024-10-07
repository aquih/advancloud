# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import requests
import logging
import csv
import io

class SendToAdvanCloud(models.TransientModel):
    _name = 'advancloud.send_to_advancloud'

    def _default_company(self):
        return self.env.company.id

    def _default_productos(self):
        active_ids = self._context.get('active_ids', [])
        if len(active_ids) > 0:
            products = self.env['product.product'].browse(active_ids)
            return [(4, x, False) for x in active_ids]
        else:
            return None

    company_id = fields.Many2one('res.company', string='Company', required=True, default=_default_company)
    product_ids = fields.Many2many("product.template", string="Productos", default=_default_productos)

    def send_to_advancloud(self):
        data = {
            'grant_type': 'password',
            'username': self.company_id.user_advancloud,
            'password': self.company_id.password_advancloud,
            'client_id': 'cloud'
        }
        r = requests.post('https://{}/advancloud/oauth/token'.format(self.company_id.url_advancloud), data=data)
        logging.warning(r.text)

        access_token = r.json()['access_token']

        csv_file = io.StringIO()
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(['itemtype', 'productid', 'skuid, code', 'colour.code', 'colour.name', 'buyurl', 'currency', 'price', 'name', 'description', 'name_es', 'description_es', 'material_es', 'material', 'images[0]', 'images[1]', 'images[2]', 'images[3]', 'images[4]', 'images[5]', 'images[6]', 'images[7]', 'recommended[0]', 'recommended[1]', 'recommended[2]', 'retailer'])

        for p in self.product_ids:
            csv_writer.writerow(['sku', p.id, p.barcode, '', '', '', p.company_id.currency_id.symbol, p.list_price, p.name, p.description_sale, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        csv_file.seek(0)
        result = csv_file.getvalue()
        logging.warning(result)

        headers = { 'Authorization': 'Bearer '+access_token }
        data = {
            'username': self.company_id.user_advancloud,
            'password': self.company_id.password_advancloud,
            'token': self.company_id.app_advancloud,
            'operation': 'import',
        }
        files = { 'file': ('import.csv', csv_file) }
        r = requests.post('https://{}/advancloud/import/upload'.format(self.company_id.url_advancloud), data=data, headers=headers, files=files)
        logging.warning(r.text)