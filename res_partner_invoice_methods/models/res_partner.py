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


class ResPartner(models.Model):
    _inherit = 'res.partner'
    invoice_preference = fields.Selection([
        ('online', 'Online'),
        ('mail', 'Physical Mail'),
        ('fax', 'Fax'),
    ], default='online')
    invoice_grouping = fields.Selection(
        [
            ('grouped', 'Group All Orders On Same Invoice'),
            ('separate', 'Each Order On Separate Invoice'),
        ],
        default='grouped',
        string='Invoice Grouping Preference'
    )
    invoice_cc_ids = fields.Many2many(
        comodel_name = 'res.partner',
        relation = 'rel_res_partner_invoice_cc_res_partner',
        inverse_name = 'invoice_ccd_on_ids',
        column1 = 'rel_invoice_cc_ids',
        column2 = 'rel_invoice_ccd_on_ids',
        string = 'Invoice CCs',
        help = 'CC These Users When Invoicing',
    )
    invoice_ccd_on_ids = fields.Many2many(
        comodel_name = 'res.partner',
        relation = 'rel_res_partner_invoice_cc_res_partner',
        inverse_name = 'invoice_cc_ids',
        column1 = 'rel_invoice_ccd_on_ids',
        column2 = 'rel_invoice_cc_ids',
        string = 'CCd By',
        help = 'CCd On Invoices By These Users',
    )

    @api.model
    def _fix_invoice_group_names(self, ):
        for i in self.search([('invoice_grouping', '=', 'all')]):
            i.invoice_grouping = 'grouped'
        
    