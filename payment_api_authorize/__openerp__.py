# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Payment Authorize API Base",
    "summary": "Provides a base for API communication with Authorize.net",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://laslabs.com/",
    "author": "LasLabs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [
            'authorizenet',
        ],
    },
    "depends": [
        "payment_authorize",
    ],
}
