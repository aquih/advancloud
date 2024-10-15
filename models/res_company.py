# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.release import version_info

class ResCompany(models.Model):
    _inherit = "res.company"

    user_advancloud = fields.Char('User')
    password_advancloud = fields.Char('Password')
    url_advancloud = fields.Char('URL')
    app_advancloud = fields.Char('App')