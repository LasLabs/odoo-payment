# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestPaymentTransaction(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestPaymentTransaction, self).setUp(*args, **kwargs)
        self.journal_id = self.env['account.journal'].create({
            'name': 'Journal',
            'code': 'BNK',
            'type': 'bank',
            'company_id': self.env.ref('base.main_company').id,
        })
        self.acquirer_id = self.env['payment.acquirer'].search([
            ('provider', '=', 'authorize'),
            ('company_id', '=', self.env.ref('base.main_company').id),
        ], limit=1)
        self.acquirer_id.write({'journal_id': self.journal_id.id})
        self.partner_id = self.env['res.partner'].create({'name': 'Partner',
                                                          'country_id': 1,
                                                          })
        self.product_id = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 123.45,
        })
        self.account_type_id = self.env['account.account.type'].create({
            'name': 'Test Account Type',
            'code': 'TestType',
        })
        self.account_id = self.env['account.account'].create({
            'name': 'Test Account',
            'code': 'TEST',
            'user_type': self.account_type_id.id,
            'company_id': self.env.ref('base.main_company').id,
        })
        self.invoice_id = self.env['account.invoice'].create({
            'partner_id': self.partner_id.id,
            'account_id': self.account_id.id,
            'company_id': self.env.ref('base.main_company').id,
            'state': 'open',
            'invoice_line': [(0, 0, {
                'product_id': self.product_id.id,
                'account_id': self.account_id.id,
                'name': 'Test Line',
                'price_unit': 123.45,
                'quantity': 1,
            })],
        })
        self.invoice_id.action_move_create()
        self.PaymentTransaction = self.env['payment.transaction']
        self.authorize_post_data = {
            'return_url': u'/shop/payment/validate',
            'x_MD5_Hash': u'7934485E1C105940BE854208D10FAB4F',
            'x_account_number': u'XXXX0027',
            'x_address': u'Huge Street 2/543',
            'x_amount': u'123.45',
            'x_auth_code': u'E4W7IU',
            'x_avs_code': u'Y',
            'x_card_type': u'Visa',
            'x_cavv_response': u'2',
            'x_city': u'Sun City',
            'x_company': u'',
            'x_country': u'Belgium',
            'x_cust_id': u'',
            'x_cvv2_resp_code': u'',
            'x_description': u'',
            'x_duty': u'0.00',
            'x_email': u'norbert.buyer@exampl',
            'x_fax': u'',
            'x_first_name': u'Norbert',
            'x_freight': u'0.00',
            'x_invoice_num': self.invoice_id.number,
            'x_last_name': u'Buyer',
            'x_method': u'CC',
            'x_phone': u'0032 12 34 56 78',
            'x_po_num': u'',
            'x_response_code': u'0',
            'x_response_reason_code': u'1',
            'x_response_reason_text': u'This transaction has been approved.',
            'x_ship_to_address': u'Huge Street 2/543',
            'x_ship_to_city': u'Sun City',
            'x_ship_to_company': u'',
            'x_ship_to_country': u'Belgium',
            'x_ship_to_first_name': u'Norbert',
            'x_ship_to_last_name': u'Buyer',
            'x_ship_to_state': u'',
            'x_ship_to_zip': u'1000',
            'x_state': u'',
            'x_tax': u'0.00',
            'x_tax_exempt': u'FALSE',
            'x_test_request': u'false',
            'x_trans_id': u'2217460311',
            'x_type': u'auth_capture',
            'x_zip': u'1000'
        }

    def _new_txn(self, state='draft'):
        return self.env['payment.transaction'].create({
            'reference': 'Test',
            'acquirer_id': self.acquirer_id.id,
            'amount': 123.45,
            'state': state,
            'currency_id': self.invoice_id.currency_id.id,
            'partner_id': self.invoice_id.partner_id.id,
            'partner_country_id': self.invoice_id.partner_id.country_id.id,
            'partner_city': self.authorize_post_data.get('x_city'),
            'partner_address': self.authorize_post_data.get('x_address'),
        })

    def test_authorize_form_get_tx_from_data_tx_create(self):
        """ Validate that transaction is created when one doesn't exist """
        tx_id = self.PaymentTransaction._authorize_form_get_tx_from_data(
            self.authorize_post_data,
        )
        self.assertEqual(
            tx_id.reference, '%s [%s]' % (
                self.invoice_id.number, self.authorize_post_data['x_trans_id']
            ),
        )
        self.assertEqual(
            tx_id.state, 'draft',
        )

    # @TODO: Figure out the account/line wire crossing in this test
    # def test_authorize_form_validate_does_voucher(self):
    #     """ Validate that transaction is completed on right Authorize res"""
    #     self.authorize_post_data['x_response_code'] = 1
    #     tx_id = self._new_txn()
    #     self.PaymentTransaction._authorize_form_validate(
    #         tx_id, self.authorize_post_data,
    #     )
    #     voucher_ids = self.env['account.voucher'].search([
    #         ('partner_id', '=', self.partner_id.id),
    #     ])
    #     self.assertEqual(
    #         1, len(voucher_ids),
    #     )

    def test_authorize_form_validate_does_not_voucher(self):
        """ Validate that transaction is left alone unless valid """
        self.authorize_post_data['x_response_code'] = 0
        tx_id = self._new_txn()
        self.PaymentTransaction._authorize_form_validate(
            tx_id, self.authorize_post_data,
        )
        voucher_ids = self.env['account.voucher'].search([
            ('partner_id', '=', self.partner_id.id),
        ])
        self.assertEqual(
            0, len(voucher_ids)
        )
