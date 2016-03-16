# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
import mock


class TestPaymentAcquirerPartialWizard(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestPaymentTransaction, self).setUp(*args, **kwargs)

        self.invoice_id = self.env['account.invoice'].search([], limit=1)
        self.model_obj = self.env['payment.acquirer.partial.wizard']

    def _new_record(self, ):
        return self.model_obj.with_context({'active_id': self.invoice_id.id})

    def test_default_invoice_id(self, ):
        res = self._new_record()
        expect = self.invoice_id
        got = res.invoice_id
        self.assertEqual(
            expect, got,
            'Default invoice not set, Expect %s Got %s' % (
                expect, got,
            )
        )

    def test_default_pay_amount(self, ):
        res = self._new_record()
        expect = self.invoice_id.residual
        got = res.pay_amount
        self.assertEqual(
            expect, got,
            'Default invoice not set, Expect %s Got %s' % (
                expect, got,
            )
        )

    def test_default_payment_block(self, ):
        with mock.patch.object(
            self.model_obj, '_default_payment_acquirer'
        ) as mk:
            res = self._new_record()
            mk().render.assert_called_once_with(
                reference=self.invoice_id.number,
                currency_id=self.invoice_id.currency_id.id,
                amount=self.invoice_id.residual,
                partner_id=self.invoice_id.partner_id.id,
            )
