# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrPayrollStructureType(models.Model):
    _inherit = "hr.payroll.structure.type"
    _description = "Salary Structure Type"

    salary_advantage_ids = fields.One2many(
        "hr.contract.salary.advantage", "structure_type_id"
    )
