# -*- coding: utf-8 -*-
# © 2015-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Partial Invoice Payments in Portal",
    'license': 'AGPL-3',
    'author': "LasLabs",
    'website': "https://laslabs.com",
    'category': 'Payment',
    'version': '9.0.1.0.0',
    'depends': [
        'payment',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'wizards/payment_acquirer_partial_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
}
