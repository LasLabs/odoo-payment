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
from openerp import models, fields, api
from collections import defaultdict
import logging


_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    invoice_preference = fields.Selection(
        related='partner_id.invoice_preference'
    )
    partner_cc_to_ids = fields.Many2many(
        comodel_name = 'res.partner',
        related = 'partner_id.invoice_cc_ids',
    )

    @api.multi
    def action_invoice_sent_prefs(self, ):
        
        assert len(self) == 1, \
               'This option should only be used for a single id at a time.'
        
        assert self.state not in ['draft', 'cancel',], \
               'Cannot send an invoice in %s state' % self.state
        
        invoice_partners = self.env['res.partner'].browse(
            [self.partner_id.id] + [i.id for i in self.partner_cc_to_ids]
        )
        _logger.debug('Got %s for invoice delivery', invoice_partners)
        
        deliveries = defaultdict(list)
        for partner in invoice_partners:
            invoice_pref = partner.invoice_preference
            deliveries[invoice_pref].append(partner.id)
            self.message_follower_ids = [(4, partner.id, 0)]
            
        printed = [p for p in deliveries.get('mail', [])]
        faxed = [p for p in deliveries.get('fax', [])]

        if self.partner_id.invoice_preference == 'online':
            return super(AccountInvoice, self).action_invoice_sent()
        else:
            return super(AccountInvoice, self).invoice_print()

        return

        raise NotImplementedError()
        
