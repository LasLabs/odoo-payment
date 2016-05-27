# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'
    journal_id = fields.Many2one(
        string='Pay To Account',
        comodel_name='account.journal',
        domain=[('type', 'in', ['bank', ])],
        default=lambda s: s._default_journal_id(),
    )

    def _default_journal_id(self, ):
        try:
            return self.company_id.bank_journal_ids[0]
        except AttributeError:
            return self.env['account.journal'].search([
                ('company_id', '=', self.company_id.id),
                ('type', 'in', ['bank', ])
            ],
                limit=1,)
