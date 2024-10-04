# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.release import version_info

class ResCompany(models.Model):
    _inherit = "res.company"

    user_advancloud = fields.Char('User AdvanCloud')
    password_advancloud = fields.Char('Password AdvanCloud')
    url_advancloud = fields.Char('URL AdvanCloud')
    app_advancloud = fields.Char('App AdvanCloud')