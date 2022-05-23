from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    consolidation_journal_line_ids = fields.Many2many(
        "consolidation.journal.line", string="Consolidation Journal Line"
    )
