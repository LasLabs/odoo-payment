# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Dave Lasley <dave@laslabs.com>
#    Copyright: 2015 LasLabs, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, api, fields
from openerp.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _authorize_form_get_tx_from_data(self, data):
        """ Overload original method to create transaction if none exists """

        try:
            return super(PaymentTransaction, self).\
                _authorize_form_get_tx_from_data(data)
        except ValidationError as original_error:
            pass

        reference = data.get('x_invoice_num')
        trans_id = data.get('x_trans_id', 0)
        fingerprint = data.get('x_MD5_Hash')
        pay_amount = float(data.get('x_amount'))

        if not reference or not trans_id or not fingerprint:
            raise original_error

        tx = self.search([
            ('reference', '=like', '%s%%' % reference),
            ('state', '=', 'draft'),
            ('amount', '=', pay_amount),
        ])

        if not tx:
            invoice_id = self.env['account.invoice'].search([
                ('number', '=', reference)
            ], limit=1)
            acquirer_id = self.env['payment.acquirer'].search([
                ('provider', '=', 'authorize'),
                ('company_id', '=', invoice_id.company_id.id)
            ], limit=1)

            tx_vals = {
                'reference': '%s [%s]' % (reference, trans_id),
                'acquirer_id': acquirer_id.id,
                'amount': pay_amount,
                'state': 'draft',
                'currency_id': invoice_id.currency_id.id,
                'partner_id': invoice_id.partner_id.id,
                'partner_country_id': invoice_id.partner_id.country_id.id,
                'account_id': invoice_id.account_id.id,
                'partner_state': data.get('x_state'),
                'partner_city': data.get('x_city'),
                'partner_street': data.get('x_address'),
            }
            _logger.debug('Creating tx with %s', tx_vals)
            tx = self.create(tx_vals)

        elif len(tx) > 1:
            raise original_error

        return tx

    @api.model
    def _authorize_form_validate(self, tx, data, ):
        status_code = int(data.get('x_response_code', '0'))
        valid_status = self._authorize_valid_tx_status
        if status_code == valid_status and tx.state != 'done':
            reference = data.get('x_invoice_num')
            invoice_id = self.env['account.invoice'].search([
                ('number', '=', reference)
            ], limit=1)
            acquirer_id = self.env['payment.acquirer'].search([
                ('provider', '=', 'authorize'),
                ('company_id', '=', invoice_id.company_id.id)
            ], limit=1)
            if acquirer_id.journal_id:
                date = fields.Date.today()
                trans_id = data.get('x_trans_id', 0)
                pay_amount = float(data.get('x_amount'))

                name = '%s Transaction ID %s' % (acquirer_id.name, trans_id)
                partner_id = invoice_id.partner_id
                if partner_id.parent_id:
                    partner_id = partner_id.parent_id
                account_id = partner_id.property_account_receivable_id
                voucher_id = self.env['account.voucher'].create({
                    'name': name,
                    'amount': pay_amount,
                    'company_id': invoice_id.company_id.id,
                    'journal_id': acquirer_id.journal_id.id,
                    'account_id': account_id.id,
                    'partner_id': partner_id.id,
                    'type': 'receipt',
                    'line_ids': [(0, 0, {
                        'name': name,
                        'payment_option': 'without_writeoff',
                        'amount': pay_amount,
                        'partner_id': partner_id.id,
                        'account_id': account_id.id,
                        'type': 'cr',
                        'move_line_id': invoice_id.move_id.line_ids[0].id,
                    })]
                })
                voucher_id.signal_workflow('proforma_voucher')
        return super(PaymentTransaction, self)._authorize_form_validate(
            tx, data
        )
