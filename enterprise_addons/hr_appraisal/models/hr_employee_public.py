# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    last_appraisal_id = fields.Many2one(readonly=True)
