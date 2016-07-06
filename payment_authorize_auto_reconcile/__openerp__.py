# -*- coding: utf-8 -*-
# © 2015-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': "Payment Authorize - Auto Reconcile",
    'description': 'Reconcile invoices from Authorize.net payments',
    'license': 'AGPL-3',
    'author': "LasLabs",
    'website': "https://laslabs.com",
    'category': 'Hidden',
    'version': '9.0.1.0.0',
    'depends': [
        'payment_authorize',
        'payment_base_auto_reconcile',
    ],
    'installable': True,
    'application': False,
}
