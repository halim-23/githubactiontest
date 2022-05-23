# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class Box1099(models.Model):
    _name = "l10n_us.1099_box"
    _description = "Represents a box on a 1099 box."

    name = fields.Char("Name")
