# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api

from authorizenet import apicontractsv1


class PaymentApiAuthorize(models.TransientModel):
    _name = 'payment.api.authorize'
    _description = 'Authorize Payment Api'
    acquirer_id = fields.Many2one(
        string='Acquirer',
        comodel_name='payment.acquirer',
    )
    acquirer_api = fields.Binary(
        compute='_compute_acquirer_api',
    )

    @api.multi
    def _compute_acquirer_api(self):
        for rec_id in self:
            api = apicontractsv1.merchantAuthenticationType()
            api.name = rec_id.authorize_login
            api.transactionKey = authorize_transaction_key
            rec_id.acquirer_api = api
