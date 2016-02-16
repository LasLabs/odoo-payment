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

    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        related='invoice_id.company_id',
    )
    invoice_id = fields.Many2one(
        string='Invoice',
        comodel_name='account.invoice',
        readonly=True,
        default=lambda s: s._default_invoice_id(),
    )
    pay_amount = fields.Float(
        string='Amount to Pay',
        digits=dp.get_precision('Account'),
        required=True,
        default=lambda s: s._default_pay_amount(),
    )
    static_pay_amount = fields.Float(
        string='Amount to Pay',
        digits=dp.get_precision('Account'),
        readonly=True,
        related='pay_amount',
    )
    acquirer_id = fields.Many2one(
        string='Payment Method',
        comodel_name='payment.acquirer',
        default=lambda s: s._default_payment_acquirer(),
        required=True,
    )
    payment_block = fields.Text(
        compute='_compute_payment_block',
        default=lambda s: s._default_payment_block(),
        readonly=True,
    )

    @api.model
    def _default_invoice_id(self, ):
        return self.env['account.invoice'].browse(
            self._context.get('active_id')
        )

    @api.model
    def _default_pay_amount(self, ):
        return self._default_invoice_id().residual

    @api.model
    def _default_payment_acquirer(self, ):
        invoice_id = self._default_invoice_id()
        return self.env['payment.acquirer'].search([
            ('company_id', '=', invoice_id.company_id.id),
            ('website_published', '=', True),
        ], limit=1)

    @api.model
    def _default_payment_block(self, ):
        invoice_id = self._default_invoice_id()
        return self._default_payment_acquirer().render(
            reference=invoice_id.number,
            currency_id=invoice_id.currency_id.id,
            amount=self._default_pay_amount(),
            partner_id=invoice_id.partner_id.id,
        )

    @api.multi
    def _compute_payment_block(self, ):
        for rec_id in self:
            rec_id.payment_block = rec_id.render(
                rec_id.invoice_id.number, rec_id.invoice_id.currency_id,
                rec_id.pay_amount, rec_id.invoice_id.partner_id,
            )

    @api.multi
    def reload(self, ):
        self.ensure_one()
        imd = self.env['ir.model.data']
        wizard_view_id = imd.xmlid_to_object(
            'payment_acquirer_partial.payment_acquirer_partial_wizard_view'
        )
        action_id = imd.xmlid_to_object(
            'payment_acquirer_partial.payment_acquirer_partial_wizard_action'
        )
        context = self._context.copy()
        context.update({
            'active_id': self.id,
        })
        return {
            'name': action_id.name,
            'help': action_id.help,
            'type': action_id.type,
            'views': [
                (wizard_view_id.id, 'form'),
            ],
            'target': 'new',
            'context': context,
            'res_id': self.id,
            'res_model': action_id.res_model,
        }

    @api.multi
    @api.onchange('invoice_id', 'acquirer_id', 'pay_amount')
    def _onchange_data(self, ):
        self.ensure_one()
        self.payment_block = self.render(
            self.invoice_id.number,
            self.invoice_id.currency_id,
            self.pay_amount,
            self.invoice_id.partner_id,
        )

    @api.multi
    def render(self, number, currency_id, pay_amount, partner_id):
        self.ensure_one()
        block = self.acquirer_id.render(
            reference=number,
            currency_id=currency_id.id,
            amount=pay_amount,
            partner_id=partner_id.id,
        )[0]
        _logger.debug('Got payment_block: %s', block)
        return block
