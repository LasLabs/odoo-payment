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
from openerp import models, api
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
            ('provider', '=', 'Authorize.Net'),
            ('company_id', '=', invoice.company_id.id)
        ], limit=1)

        pay_amount = data.get('x_amount')

        if not tx:

            tx_vals = {
                'reference': reference,
                'acquirer_id': acquirer.id,
                'amount': pay_amount,
                'state': 'draft',
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_country_id': invoice.partner_id.country_id.id,
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
        _logger.debug('Paying %s on %s', pay_amount, invoice)
        invoice.pay_and_reconcile(
            pay_amount=pay_amount,
            pay_account_id=invoice.account_id.id,
            period_id=invoice.period_id.id,
            pay_journal_id=invoice.journal_id.id,
            writeoff_acc_id=invoice.account_id.id,
            writeoff_period_id=invoice.period_id.id,
            writeoff_journal_id=invoice.journal_id.id,
            name='Authorize.net Transaction ID %s' % trans_id,
        )

        return tx[0]
