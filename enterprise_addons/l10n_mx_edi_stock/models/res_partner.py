from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    l10n_mx_edi_operator_licence = fields.Char("Operator Licence")
