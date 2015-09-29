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
{
    'name': "payment_authorize_auto_reconcile",

    'summary': """
        Automatically reconcile Authorize.net payments against appropriate Invoice
    """,

    'description': """
        Authorize.net payments do not automatically generate transactions.
        This plugin automates the process by creating a transaction and
            reconciling it against the appropriate invoice.
        Do note that chargebacks will still need to be handled manually.
    """,

    'author': "LasLabs",
    'website': "https://laslabs.com",
    'category': 'Hidden',
    'version': '8.0.1.0',
    'depends': [
        'payment', 
        'payment_authorize',
    ],
}