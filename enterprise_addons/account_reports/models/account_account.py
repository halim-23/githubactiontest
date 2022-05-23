from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    exclude_from_aged_reports = fields.Boolean(
        default=False, help="Exclude this account from aged reports"
    )
