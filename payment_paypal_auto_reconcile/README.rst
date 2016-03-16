.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
PayPal Auto Reconciliation
==========================

Automatically reconcile PayPal payments against appropriate Invoice

PayPal payments do not automatically generate transactions.

This plugin automates the process by creating a transaction and reconciling it against the appropriate invoice.

Example of the error that this solves:
2016-03-15 20:06:35,098 24796 INFO smdrugstore openerp.addons.payment_paypal.models.paypal: Paypal: received data with missing reference () or txn_id (47T022049E9822917)
2016-03-15 20:06:35,099 24796 INFO smdrugstore werkzeug: 127.0.0.1 - - [15/Mar/2016 20:06:35] "POST /payment/paypal/ipn/ HTTP/1.0" 500 -
2016-03-15 20:06:35,110 24796 ERROR smdrugstore werkzeug: Error on request:
Traceback (most recent call last):
  File "/media/enc-data-01/odoo/_venv/lib/python2.7/site-packages/werkzeug/serving.py", line 177, in run_wsgi
    execute(self.server.app)
  File "/media/enc-data-01/odoo/_venv/lib/python2.7/site-packages/werkzeug/serving.py", line 165, in execute
    application_iter = app(environ, start_response)
  File "/media/enc-data-01/odoo/openerp/service/server.py", line 245, in app
    return self.app(e, s)
  File "/media/enc-data-01/odoo/openerp/service/wsgi_server.py", line 184, in application
    return application_unproxied(environ, start_response)
  File "/media/enc-data-01/odoo/openerp/service/wsgi_server.py", line 170, in application_unproxied
    result = handler(environ, start_response)
  File "/media/enc-data-01/odoo/openerp/http.py", line 1488, in __call__
    return self.dispatch(environ, start_response)
  File "/media/enc-data-01/odoo/openerp/http.py", line 1462, in __call__
    return self.app(environ, start_wrapped)
  File "/media/enc-data-01/odoo/_venv/lib/python2.7/site-packages/werkzeug/wsgi.py", line 588, in __call__
    return self.app(environ, start_response)
  File "/media/enc-data-01/odoo/openerp/http.py", line 1652, in dispatch
    result = ir_http._dispatch()
  File "/media/enc-data-01/odoo/addons/website_sale/models/ir_http.py", line 12, in _dispatch
    return super(IrHttp, self)._dispatch()
  File "/media/enc-data-01/odoo/addons/utm/models/ir_http.py", line 13, in _dispatch
    response = super(ir_http, self)._dispatch()
  File "/media/enc-data-01/odoo/addons/website/models/ir_http.py", line 190, in _dispatch
    resp = super(ir_http, self)._dispatch()
  File "/media/enc-data-01/odoo/addons/web_editor/models/ir_http.py", line 16, in _dispatch
    return super(ir_http, self)._dispatch()
  File "/media/enc-data-01/odoo/openerp/addons/base/ir/ir_http.py", line 186, in _dispatch
    return self._handle_exception(e)
  File "/media/enc-data-01/odoo/addons/website/models/ir_http.py", line 239, in _handle_exception
    return super(ir_http, self)._handle_exception(exception)
  File "/media/enc-data-01/odoo/openerp/addons/base/ir/ir_http.py", line 157, in _handle_exception
    return request._handle_exception(exception)
  File "/media/enc-data-01/odoo/openerp/http.py", line 781, in _handle_exception
    return super(HttpRequest, self)._handle_exception(exception)
  File "/media/enc-data-01/odoo/openerp/addons/base/ir/ir_http.py", line 182, in _dispatch
    result = request.dispatch()
  File "/media/enc-data-01/odoo/openerp/http.py", line 840, in dispatch
    r = self._call_function(**self.params)
  File "/media/enc-data-01/odoo/openerp/http.py", line 316, in _call_function
    return checked_call(self.db, *args, **kwargs)
  File "/media/enc-data-01/odoo/openerp/service/model.py", line 118, in wrapper
    return f(dbname, *args, **kwargs)
  File "/media/enc-data-01/odoo/openerp/http.py", line 309, in checked_call
    result = self.endpoint(*a, **kw)
  File "/media/enc-data-01/odoo/openerp/http.py", line 959, in __call__
    return self.method(*args, **kw)
  File "/media/enc-data-01/odoo/openerp/http.py", line 509, in response_wrap
    response = f(*args, **kw)
  File "/media/enc-data-01/odoo/addons/payment_paypal/controllers/main.py", line 65, in paypal_ipn
    self.paypal_validate_data(**post)
  File "/media/enc-data-01/odoo/addons/payment_paypal/controllers/main.py", line 54, in paypal_validate_data
    res = request.registry['payment.transaction'].form_feedback(cr, SUPERUSER_ID, post, 'paypal', context=context)
  File "/media/enc-data-01/odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/media/enc-data-01/odoo/addons/website_sale/models/payment.py", line 19, in form_feedback
    res = super(PaymentTransaction, self).form_feedback(cr, uid, data, acquirer_name, context=context)
  File "/media/enc-data-01/odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/media/enc-data-01/odoo/addons/payment/models/payment_acquirer.py", line 518, in form_feedback
    tx = getattr(self, tx_find_method_name)(cr, uid, data, context=context)
  File "/media/enc-data-01/odoo/openerp/api.py", line 250, in wrapper
    return old_api(self, *args, **kwargs)
  File "/media/enc-data-01/odoo/addons/payment_paypal/models/paypal.py", line 185, in _paypal_form_get_tx_from_data
    raise ValidationError(error_msg)
ValidationError: Paypal: received data with missing reference () or txn_id (47T022049E9822917)
``

Configuration
=============

Update the `Pay To Account` field in the Payment Acquirer form to the
journal to create vouchers for

Credits
=======

Images
------

* LasLabs: `Icon <https://repo.laslabs.com/projects/TEM/repos/odoo-module_template/browse/module_name/static/description/icon.svg?raw>`_.

Contributors
------------

* Dave Lasley <dave@laslabs.com>

Maintainer
----------

.. image:: https://laslabs.com/logo.png
   :alt: LasLabs Inc.
   :target: https://laslabs.com

This module is maintained by LasLabs Inc.
