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
from openerp.exceptions import Warning, ValidationError
from collections import defaultdict
import logging


_logger = logging.getLogger(__name__)


class SaleMakeInvoice(models.TransientModel):
    _inherit = 'sale.make.invoice'
    grouped = fields.Selection(
        [
            ('partner_preference', 'Grouped By Partner Preference'),
            ('grouped', 'Orders Grouped On One Invoice Per Customer'),
            ('separate', 'Orders Invoiced Individually'),
        ],
        required = True,
        default = 'partner_preference',
        help = 'Select the invoice grouping method for these orders',
    )

    def active_ids(self, ):
        return self.env['sale.order'].browse(self._context.get('active_ids'))

    @api.multi
    def make_invoices(self, ):

        sale_mdl = self.env['sale.order']
        new_invoices = []
        
        _logger.debug('Working on orders %s', self.active_ids())
        for sale_order in self.active_ids():
            if sale_order.state != 'manual':
                raise ValidationError(
                    "You shouldn't manually invoice the following order %s" % (
                        sale_order.name
                    )
                )
        
        
        if self.grouped == 'partner_preference':
            
            invoice_groups = defaultdict(list)
            ungrouped = []

            for order in self.active_ids():

                if order.partner_invoice_id.invoice_grouping == 'grouped':
                    _logger.debug(
                        '%s chose grouped invoicing, adding to invoice_groups',
                        order.partner_invoice_id
                    )
                    invoice_groups[order.partner_invoice_id.id].append(order.id)
                else:
                    _logger.debug(
                        '%s chose sep invoicing, adding to ungrouped',
                        order.partner_invoice_id
                    )
                    ungrouped.append(order.id)

            if len(ungrouped):
                _logger.debug('Creating ungrouped invoices for %s', ungrouped)
                sale_mdl.browse(ungrouped).action_invoice_create(
                    grouped = False,
                    date_invoice = self.invoice_date
                )
            
            for orders in invoice_groups.values():
                _logger.debug('Creating ungrouped invoices for %s', orders)
                sale_mdl.browse(orders).action_invoice_create(
                    grouped = True,
                    date_invoice = self.invoice_date
                )
            
                
        else:
            _logger.debug('Not invoicing by partner preference')
            self.active_ids.action_invoice_create(
                grouped = (self.grouped == 'grouped'),
                date_invoice = self.invoice_date,
            )
        
        for sale_order in self.active_ids():
            for invoice in sale_order.invoice_ids:
                new_invoices.append(invoice.id)

        _logger.debug('Created invoices: %s', new_invoices)
        
        # Dummy call to workflow, will not create another invoice but bind the new invoice to the subflow
        manual_orders = [
            o.id for o in self.active_ids() if o.order_policy == 'manual'
        ]
        sale_mdl.browse(manual_orders).signal_workflow('manual_invoice')
        result = self.env['ir.model.data'].get_object_reference(
            'account', 'action_invoice_tree1',
        )
        id = result and result[1] or False
        result = self.env['ir.actions.act_window'].browse(id).read()[0]
        result['domain'] = "[('id','in', [" + ','.join(map(str, new_invoices)) + "])]"

        _logger.debug('Invoice domain %s', result['domain'])
        return result

