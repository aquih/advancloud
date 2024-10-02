# -*- encoding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError

import requests
import logging
import csv
import io

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def send_to_advancloud(self):
        data = {
            'grant_type': 'password',
            'username': 'demoaquih',
            'password': 'aquiHPM21',
            'client_id': 'cloud'
        }
        r = requests.post('https://aquih.keonn.com/advancloud/oauth/token', data=data)
        logging.warning(r.text)

        access_token = r.json()['access_token']

        csv_file = io.StringIO()
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(['itemtype', 'productid', 'skuid, code', 'colour.code', 'colour.name', 'buyurl', 'currency', 'price', 'name', 'description', 'name_es', 'description_es', 'material_es', 'material', 'images[0]', 'images[1]', 'images[2]', 'images[3]', 'images[4]', 'images[5]', 'images[6]', 'images[7]', 'recommended[0]', 'recommended[1]', 'recommended[2]', 'retailer'])

        for p in self:
            csv_writer.writerow(['sku', p.id, p.barcode, '', '', '', p.company_id.currency_id.symbol, p.list_price, p.name, p.description_sale, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

        csv_file.seek(0)
        result = csv_file.getvalue()
        logging.warning(result)

        headers = { 'Authorization': 'Bearer '+access_token }
        data = {
            'username': 'demoaquih',
            'password': 'aquiHPM21',
            'token': 'aquihpro',
            'operation': 'import',
        }
        files = { 'file': ('import.csv', csv_file) }
        r = requests.post('https://aquih.keonn.com/advancloud/import/upload', data=data, headers=headers, files=files)
        logging.warning(r.text)