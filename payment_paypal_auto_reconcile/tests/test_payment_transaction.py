# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
# from hashlib import md5


class TestPaymentTransaction(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestPaymentTransaction, self).setUp(*args, **kwargs)

        self.invoice_id = self.env['account.invoice'].search([], limit=1)

        self.data_vals = {
            'item_number': self.invoice_id.reference,
            'trans_id': 1234,
            'mc_currency': u'USD',
            # 'x_MD5_Hash': md5().update('TEST').hexdigest(),
            'x_amount': self.invoice_id.residual,
        }

    def test_authorize_form_get_tx_from_data_tx_create(self):
        """ Validate that transaction is created when once doesn't exist """
        pass
