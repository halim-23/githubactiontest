# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from .common import SpreadsheetTestCommon


@tagged("post_install", "-at_install")
class TestSpreadsheetOpenPivot(SpreadsheetTestCommon, HttpCase):
    def test_01_spreadsheet_open_pivot_as_admin(self):
        self.start_tour("/web", "spreadsheet_open_pivot_sheet", login="admin")

    def test_01_spreadsheet_open_pivot_as_user(self):
        self.start_tour("/web", "spreadsheet_open_pivot_sheet", login="spreadsheetDude")
