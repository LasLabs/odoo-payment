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


post_return = {'return_url': u'',
 'x_MD5_Hash': u'FDE26C3F82AD9928D49C8877B7CEE330',
 'x_account_number': u'XXXX0002',
 'x_address': u'123 Test Ave',
 'x_amount': u'5.00',
 'x_auth_code': u'000000',
 'x_avs_code': u'P',
 'x_card_type': u'American Express',
 'x_cavv_response': u'',
 'x_city': u'Henderson',
 'x_company': u'LasLabs Inc.',
 'x_country': u'United States',
 'x_cust_id': u'',
 'x_cvv2_resp_code': u'',
 'x_description': u'',
 'x_duty': u'0.00',
 'x_email': u'test@example.com',
 'x_fax': u'8888888888',
 'x_first_name': u'Test',
 'x_freight': u'0.00',
 'x_invoice_num': u'SAJ/2016/0032',
 'x_last_name': u'Dude',
 'x_method': u'CC',
 'x_phone': u'7025088894',
 'x_po_num': u'',
 'x_response_code': u'1',
 'x_response_reason_code': u'1',
 'x_response_reason_text': u'(TESTMODE) This transaction has been approved.',
 'x_ship_to_address': u'',
 'x_ship_to_city': u'',
 'x_ship_to_company': u'',
 'x_ship_to_country': u'',
 'x_ship_to_first_name': u'',
 'x_ship_to_last_name': u'',
 'x_ship_to_state': u'',
 'x_ship_to_zip': u'',
 'x_state': u'Nevada',
 'x_tax': u'0.00',
 'x_tax_exempt': u'FALSE',
 'x_test_request': u'true',
 'x_trans_id': u'0',
 'x_type': u'auth_capture',
 'x_zip': u'89074'}


class SomethingCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(SomethingCase, self).setUp(*args, **kwargs)

        # TODO Replace this for something useful or delete this method
        self.do_something_before_all_tests()

        return result

    def tearDown(self, *args, **kwargs):
        # TODO Replace this for something useful or delete this method
        self.do_something_after_all_tests()

        return super(SomethingCase, self).tearDown(*args, **kwargs)

    def test_something(self):
        """First line of docstring appears in test logs.
        Other lines do not.
        Any method starting with ``test_`` will be tested.
        """
        pass
