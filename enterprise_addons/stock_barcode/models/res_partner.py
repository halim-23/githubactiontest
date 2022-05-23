# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_fields_stock_barcode(self):
        return ["display_name"]
