# Part of Odoo. See LICENSE file for full copyright and licensing details.

import math

from dateutil.relativedelta import relativedelta

from odoo import models


class HRPayslip(models.Model):
    _inherit = "hr.payslip"

    def _get_base_local_dict(self):
        res = super()._get_base_local_dict()
        res.update({"relativedelta": relativedelta, "ceil": math.ceil})
        return res
