# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Dave Lasley <dave@laslabs.com>
#    Copyright: 2016-TODAY LasLabs, Inc. [https://laslabs.com]
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

from openerp.tests.common import TransactionCase
# from hashlib import md5


class TestPaymentTransaction(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestPaymentTransaction, self).setUp(*args, **kwargs)

        self.invoice_id = self.env['account.invoice'].search([], limit=1)

        self.data_vals = {
            'x_invoice_num': self.invoice_id.reference,
            'x_trans_id': 1234,
            # 'x_MD5_Hash': md5().update('TEST').hexdigest(),
            'x_amount': self.invoice_id.residual,
        }

    def test_authorize_form_get_tx_from_data_tx_create(self):
        """ Validate that transaction is created when once doesn't exist """
        pass
