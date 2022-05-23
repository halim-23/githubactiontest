# -*- coding: utf-8 -*-
import base64

from odoo import _, _lt, models, fields
from odoo.exceptions import UserError
from odoo.tools import html_escape


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_cl_daily_sales_book_id = fields.Many2one('l10n_cl.daily.sales.book')

    def _l10n_cl_edi_post_validation(self):
        if self.l10n_latam_document_type_id.code == '39':
            if self.line_ids.filtered(lambda x: x.tax_group_id.id in [
                    self.env.ref('l10n_cl.tax_group_ila').id, self.env.ref('l10n_cl.tax_group_retenciones').id]):
                raise UserError(_('Receipts with withholding taxes are not allowed'))
            if any(self.invoice_line_ids.mapped('tax_ids.price_include')):
                raise UserError(_('Tax included in price is not supported for boletas. '
                                  'Please change the tax to not included in price.'))

            daily_sales_book = self.env['l10n_cl.daily.sales.book'].search([
                ('l10n_cl_dte_status', '!=', 'rejected'), ('date', '=', self.invoice_date)])
            if daily_sales_book:
                raise UserError(_('The Daily Sales Book for this ticket has already been sent. '
                                  'Please select a different date for this ticket.'))
        super()._l10n_cl_edi_post_validation()

    def l10n_cl_send_dte_to_sii(self, retry_send=True):
        if not self.l10n_latam_document_type_id._is_doc_type_ticket():
            return super().l10n_cl_send_dte_to_sii(retry_send)
        digital_signature = self.company_id._get_digital_signature(user_id=self.env.user.id)
        response = self._send_xml_to_sii_rest(
            self.company_id.l10n_cl_dte_service_provider,
            self.company_id.vat,
            self.l10n_cl_sii_send_file.name,
            base64.b64decode(self.l10n_cl_sii_send_file.datas),
            digital_signature
        )
        if not response:
            return None

        self.l10n_cl_sii_send_ident = response.get('trackid')
        sii_response_status = response.get('estado')
        self.l10n_cl_dte_status = 'ask_for_status' if sii_response_status == 'REC' else 'rejected'
        self.message_post(body=_('DTE has been sent to SII with response: %s') %
                               self._l10n_cl_get_sii_reception_status_message_rest(sii_response_status))

    def l10n_cl_verify_dte_status(self, send_dte_to_partner=True):
        if not self.l10n_latam_document_type_id._is_doc_type_ticket():
            return super().l10n_cl_verify_dte_status(send_dte_to_partner)

        digital_signature = self.company_id._get_digital_signature(user_id=self.env.user.id)
        response = self._get_send_status_rest(
            self.company_id.l10n_cl_dte_service_provider,
            self.l10n_cl_sii_send_ident,
            self._l10n_cl_format_vat(self.company_id.vat),
            digital_signature)
        if not response:
            self.l10n_cl_dte_status = 'ask_for_status'
            return None

        self.l10n_cl_dte_status = self._analyze_sii_result_rest(response)
        if self.l10n_cl_dte_status in ['accepted', 'objected']:
            self.l10n_cl_dte_partner_status = 'not_sent'
            if send_dte_to_partner:
                self._l10n_cl_send_dte_to_partner()
        self.message_post(body=self._l10n_cl_get_verify_status_msg_rest(response))

    def _l10n_cl_get_verify_status_msg_rest(self, data):
        msg = _('Asking for DTE status with response:')
        if self.l10n_cl_dte_status in ['rejected', 'objected']:
            detail = data['detalle_rep_rech']
            if detail:
                msg += '<br/><li><b>ESTADO</b>: %s</li>' % html_escape(detail[0]['estado'])
                errors = detail[0].get('error', [])
                for error in errors:
                    msg += '<br/><li><b>ERROR</b>: %s %s</li>' % (
                        html_escape(error['descripcion']), html_escape(error['detalle']) or "")
                return msg

        return msg + '<br/><li><b>ESTADO</b>: %s</li>' % html_escape(data['estado'])

    def _l10n_cl_get_sii_reception_status_message_rest(self, sii_response_status):
        return {
            'REC': _lt('Submission received'),
            'EPR': _lt('Submission processed'),
            'CRT': _lt('Cover OK'),
            'FOK': _lt('Submission signature validated'),
            'PRD': _lt('Submission in process'),
            'RCH': _lt('Rejected due to information errors'),
            'RCO': _lt('Rejected for consistency'),
            'VOF': _lt('The .xml file was not found'),
            'RFR': _lt('Rejected due to error in signature'),
            'RPR': _lt('Accepted with objections'),
            'RPT': _lt('Repeat submission rejected'),
            'RSC': _lt('Rejected by schema'),
            'SOK': _lt('Validated schema'),
            'RCT': _lt('Rejected by error in covert'),
        }.get(sii_response_status, sii_response_status)
