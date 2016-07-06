# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) LasLabs, Inc [https://laslabs.com]. All Rights Reserved
#
##############################################################################
#
#    Collaborators of this module:
#       Written By: Dave Lasley <dave@laslabs.com>
#
##############################################################################
#
#    This project is mantained by Medical Team:
#    https://repo.laslabs.com/projects/ODOO/repos/payment
#
##############################################################################

{
    'name': "payment_authorize_auto_reconcile",
    'description': 'Reconcile invoices from Authorize.net payments',
    'license': 'AGPL-3',
    'author': "LasLabs",
    'website': "https://laslabs.com",
    'category': 'Hidden',
    'version': '9.0.1.0.0',
    'depends': [
        'payment_authorize',
        'account_voucher',
    ],
    'data': [
        'views/payment_acquirer_view.xml',
    ],
    'installable': True,
    'application': False,
}
