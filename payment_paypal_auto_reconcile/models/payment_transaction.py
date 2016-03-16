# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields
from openerp.addons.payment.models.payment_acquirer import ValidationError
import logging


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _paypal_form_get_tx_from_data(self, data):
        """ Overload original method to create transaction if none exists """

        try:
            return super(PaymentTransaction, self).\
                _paypal_form_get_tx_from_data(data)
        except ValidationError as original_error:
            pass

        reference = data.get('item_number')
        trans_id = data.get('txn_id', 0)
        pay_amount = float(data.get('payment_gross'))

        if not reference or not trans_id:
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
                limit=1
            )
            acquirer_id = self.env['payment.acquirer'].search([
                ('provider', '=', 'authorize'),
                ('company_id', '=', invoice_id.company_id.id),
            ],
                limit=1
            )
            currency_id = self.env['res.currency'].search([
                ('name', '=', data.get('mc_currency')),
            ],
                limit=1
            )
            if not len(currency_id):
                currency_id = invoice_id.currency_id

            tx_vals = {
                'reference': '%s [%s]' % (reference, trans_id),
                'acquirer_id': acquirer_id.id,
                'amount': pay_amount,
                'state': 'draft',
                'currency_id': currency_id.id,
                'partner_id': invoice_id.partner_id.id,
                'partner_country_id': invoice_id.partner_id.country_id.id,
                'account_id': invoice_id.account_id.id,
                'partner_state': data.get('address_state'),
                'partner_city': data.get('address_city'),
                'partner_street': data.get('address_street'),
            }
            _logger.debug('Creating tx with %s', tx_vals)
            tx = self.create(tx_vals)

        elif len(tx) > 1:
            raise original_error

        return tx

    @api.model
    def _paypal_form_validate(self, tx, data):
        status = data.get('payment_status')
        if status in ['Completed', 'Processed']:
            reference = data.get('item_number')
            invoice_id = self.env['account.invoice'].search([
                ('number', '=', reference)
            ],
                limit=1,
            )
            acquirer_id = self.env['payment.acquirer'].search([
                ('provider', '=', 'paypal'),
                ('company_id', '=', invoice_id.company_id.id),
                ('paypal_email_account', '=', data.get('business')),
            ],
                limit=1
            )
            if acquirer_id.journal_id:
                date = fields.Date.today()
                trans_id = data.get('txn_id', 0)
                pay_amount = float(data.get('payment_gross'))

                period_id = self.env['account.period'].find(date)
                name = '%s Transaction ID %s' % (acquirer_id.name, trans_id)
                partner_id = invoice_id.partner_id
                if partner_id.parent_id:
                    partner_id = partner_id.parent_id
                account_id = partner_id.property_account_receivable.id
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
        return super(PaymentTransaction, self)._paypal_form_validate(
            tx, data
        )
