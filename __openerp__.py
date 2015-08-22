# -*- coding: utf-8 -*-
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

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Hidden',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['payment_authorize', ],

    # always loaded
    'data': [
        
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}