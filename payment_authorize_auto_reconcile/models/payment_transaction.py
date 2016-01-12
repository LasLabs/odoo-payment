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
        """
        Given a data dict coming from authorize, verify it and find the related
        transaction record. Create transaction record if one doesn't exist.
        """

        reference = data.get('x_invoice_num')
        trans_id = data.get('x_trans_id')
        fingerprint = data.get('x_MD5_Hash')

        if not reference or not trans_id or not fingerprint:
            error_msg = 'Authorize: received data with missing reference ' +\
                '(%s) or trans_id (%s) or fingerprint (%s)' % (
                    reference, trans_id, fingerprint
                )
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        tx = self.search([('reference', '=', reference)])
        invoice = self.env['account.invoice'].search([
            ('number', '=', reference)
        ], limit=1)
        acquirer = self.env['payment.acquirer'].search([
            ('provider', '=', 'authorize'),
            ('company_id', '=', invoice.company_id.id)
        ], limit=1)
        pay_amount = float(data.get('x_amount'))

        if not tx:

            tx_vals = {
                'reference': reference,
                'acquirer_id': acquirer.id,
                'amount': pay_amount,
                'state': 'draft',
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_country_id': invoice.partner_id.country_id.id,
                'account_id': invoice.account_id.id,
                'partner_state': data.get('x_state'),
                'partner_city': data.get('x_city'),
                'partner_street': data.get('x_address'),
            }
            _logger.debug('Creating tx with %s', tx_vals)
            tx = [self.create(tx_vals)]

        elif len(tx) > 1:
            error_msg = 'Authorize: received data for reference %s' % (
                reference
            )
            error_msg += '; multiple orders found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        trans_id = data.get('x_trans_id', 0)
        _type = invoice.type in (
            'out_invoice','out_refund'
        ) and 'receipt' or 'payment'

        # voucher_obj = self.env['account.voucher'].with_context({},
        #     invoice_id=invoice.id,
        #     invoice_type=invoice.type,
        #     payment_expected_currency=invoice.currency_id.id,
        # )
        # voucher_id = voucher_obj.create({
        #     'partner_id': invoice.partner_id.id,
        #     'amount': pay_amount,
        #     'journal_id': acquirer.journal_id.id,
        #     'date': fields.Date.today(),
        #     'reference':'Authorize.net Transaction ID %s' % trans_id,
        #     'currency_id': invoice.currency_id.id,
        #     'name': 'Invoice %s' % invoice.number,
        #     'company_id': invoice.company_id.id,
        #     'account_id': invoice.account_id.id,
        #     'payment_option': 'without_writeoff',
        #     'type': _type,
        # })
        # voucher_id.action_move_line_create()

        return tx[0]
