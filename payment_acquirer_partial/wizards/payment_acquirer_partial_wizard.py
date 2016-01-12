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
import openerp.addons.decimal_precision as dp
import logging


_logger = logging.getLogger(__name__)


class PaymentAcquirerPartialWizard(models.TransientModel):
    _name = 'payment.acquirer.partial.wizard'
    _description = 'Wizard - choose amount of invoice payment for Authorize'

    def _compute_default_invoice_id(self, ):
        return self.env['account.invoice'].browse(
            self._context.get('active_id')
        )

    def _compute_default_pay_amount(self, ):
        return self._compute_default_invoice_id().residual

    invoice_id = fields.Many2one(
        string='Invoice',
        readonly=True,
        default=_compute_default_invoice_id,
    )
    pay_amount = fields.Float(
        string='Amount to Pay',
        digits=dp.get_precision('Account'),
        required=True,
        default=_compute_default_pay_amount,
    )
    acquirer_id = fields.Many2one(
        string='Payment Method',
        comodel_name='payment.acquirer',
        required=True,
    )

    @api.multi
    def generate_acquirer_display(self, ):
        return self.acquirer_id.render(
            reference=self.invoice_id.name,
            currency_id=self.invoice_id.currency_id,
            amount=self.pay_amount,
            partner_id=self.invoice_id.partner_id,
        )
