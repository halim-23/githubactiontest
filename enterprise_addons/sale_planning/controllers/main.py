# Part of Odoo. See LICENSE file for full copyright and licens

from odoo import _
from odoo.http import request

from odoo.addons.planning.controllers.main import ShiftController


class ShiftControllerProject(ShiftController):
    def _planning_get(self, planning_token, employee_token, message=False):
        result = super()._planning_get(planning_token, employee_token, message)
        if not result:
            # one of the token does not match an employee/planning
            return
        employee_fullcalendar_data = result["employee_slots_fullcalendar_data"]
        new_employee_fullcalendar_data = []
        mapped_data = {
            slot_data["slot_id"]: slot_data for slot_data in employee_fullcalendar_data
        }
        slot_ids = request.env["planning.slot"].sudo().browse(list(mapped_data.keys()))
        for slot_sudo in slot_ids:
            slot_data = mapped_data[slot_sudo.id]
            slot_data["sale_line"] = slot_sudo.sale_line_id.name
            # Reset the title according to the project and task name
            title = slot_sudo.role_id.name or ""
            title_full = " - ".join(
                [x for x in (title, slot_sudo.sale_line_id.name) if x]
            )
            if not title_full:
                title_full = _("Shift")
            if slot_sudo.name:
                title_full += " \U0001F4AC"
            slot_data["title"] = title_full
            new_employee_fullcalendar_data.append(slot_data)
        result["employee_slots_fullcalendar_data"] = new_employee_fullcalendar_data
        open_slots = result["open_slots_ids"]
        result["has_sale_line"] = any(s.sale_line_id for s in open_slots)
        return result
