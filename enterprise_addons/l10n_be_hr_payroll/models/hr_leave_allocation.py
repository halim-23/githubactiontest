from odoo import fields, models


class PaidTimeOffAllocation(models.Model):
    _name = "hr.leave.allocation"
    _inherit = "hr.leave.allocation"

    max_leaves_allocated = fields.Float(
        string="Max Leaves Allocated", default=20, readonly=True
    )
