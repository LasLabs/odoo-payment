# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Payment Auto-Reconcile Base",
    'license': 'AGPL-3',
    'author': "LasLabs",
    'website': "https://laslabs.com",
    'category': 'Hidden',
    'version': '9.0.1.0.0',
    'depends': [
        'payment',
        'account_voucher',
    ],
    'data': [
        'views/payment_acquirer_view.xml',
    ],
    'installable': True,
    'application': False,
}
