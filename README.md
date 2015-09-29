[![Build Status](https://travis-ci.org/laslabs/odoo-payment_authorize_auto_reconcile.svg?branch=master)](https://travis-ci.org/laslabs/odoo-payment_authorize_auto_reconcile)
 
# Auto Authorize.Net Reconciliation

## Automatically reconcile Authorize.net payments against appropriate Invoice

Authorize.net payments do not automatically generate transactions.

This plugin automates the process by creating a transaction and reconciling it against the appropriate invoice.

Do note that chargebacks will still need to be handled manually.