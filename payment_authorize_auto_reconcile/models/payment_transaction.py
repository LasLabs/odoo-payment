# -*- coding: utf-8 -*-
# © 2015-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields
import logging


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _authorize_form_get_tx_from_data(self, data):
        """ Overload original method to create transaction if none exists """

        # try:
        #     return super(PaymentTransaction, self).\
        #         _authorize_form_get_tx_from_data(data)
        # except Exception as original_error:
        #     pass

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
                ('number', '=', reference),
            ],
                limit=1,
            )
            acquirer_id = self.env['payment.acquirer'].sudo().search([
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
                'partner_city': data.get('x_city'),
                'partner_address': data.get('x_address'),
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
            # @TODO: Better multi acquirer support. Maybe x_account_number?
            acquirer_ids = self.env['payment.acquirer'].search([
                ('provider', '=', 'authorize'),
                ('company_id', '=', invoice_id.company_id.id),
            ])
            # @TODO: Journal ID search was being lame
            acquirer_ids = acquirer_ids.filtered(lambda r: bool(r.journal_id))
            if acquirer_ids:
                acquirer_id = acquirer_ids[0]
                date = fields.Date.today()
                trans_id = data.get('x_trans_id', 0)
                pay_amount = float(data.get('x_amount'))
                period_id = self.env['account.period'].find(date)
                name = '%s Transaction ID %s' % (acquirer_id.name, trans_id)
                partner_id = invoice_id.partner_id
                if partner_id.commercial_partner_id:
                    partner_id = partner_id.commercial_partner_id
                account_id = partner_id.property_account_receivable
                voucher_id = self.env['account.voucher'].create({
                    'name': name,
                    'amount': pay_amount,
                    'company_id': invoice_id.company_id.id,
                    'journal_id': acquirer_id.journal_id.id,
                    'account_id': account_id.id,
                    'period_id': period_id.id,
                    'partner_id': partner_id.id,
                    'type': 'receipt',
                    'line_ids': [(0, 0, {
                        'name': name,
                        'payment_option': 'without_writeoff',
                        'amount': pay_amount,
                        'partner_id': partner_id.id,
                        'account_id': account_id.id,
                        'type': 'cr',
                        'move_line_id': invoice_id.move_id.line_id[0].id,
                    })]
                })
                voucher_id.signal_workflow('proforma_voucher')
        return super(PaymentTransaction, self)._authorize_form_validate(
            tx, data
        )
