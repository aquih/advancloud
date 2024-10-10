# -*- encoding: utf-8 -*-

from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError, ValidationError

import requests
import logging
import csv
import io

class GetStock(models.TransientModel):
    _name = 'advancloud.get_stock'

    def _default_company(self):
        return self.env.company.id
        
    company_id = fields.Many2one('res.company', string='Company', required=True, default=_default_company)

    def get(self):
        for w in self:
            logging.warning(self.company_id)
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
            }
            r = requests.post('https://{}/advancloud/import/stock/searchex'.format(self.company_id.url_advancloud), data=data, headers=headers)
            logging.warning(r.text)

            result = r.json()

            self.env['advancloud.stock'].create([ { 'code': s['code'] } for s in result['inventories'] ])