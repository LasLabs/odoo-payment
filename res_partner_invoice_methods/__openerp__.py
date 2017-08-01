# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Dave Lasley <dave@laslabs.com>
#    Copyright: 2015 LasLabs, Inc [https://laslabs.com]
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
{
    'name': 'Partner Invoice Methods & CCs',
    'version': '8.0.0.1',
    'category': '',
    'author': "LasLabs",
    'license': 'AGPL-3',
    'website': 'https://laslabs.com',
    'depends': [
        'account',
        'sale',
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'application': False,
}
