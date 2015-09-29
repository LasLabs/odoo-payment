[![Build Status](https://travis-ci.org/laslabs/odoo-payment_authorize_auto_reconcile.svg?branch=master)](https://travis-ci.org/laslabs/odoo-payment_authorize_auto_reconcile)
 
# Auto Authorize.Net Reconciliation

### Automatically reconcile Authorize.net payments against appropriate Invoice

Authorize.net payments do not automatically generate transactions.

This plugin automates the process by creating a transaction and reconciling it against the appropriate invoice.

Do note that chargebacks will still need to be handled manually.

Example of the error that this solves:
```
2015-09-29 05:05:17,979 24363 INFO laslabs werkzeug: 127.0.0.1 - - [29/Sep/2015 05:05:17] "POST /payment/authorize/return/ HTTP/1.0" 500 -
2015-09-29 05:05:17,989 24363 ERROR laslabs werkzeug: Error on request:
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/dist-packages/werkzeug/serving.py", line 180, in run_wsgi
    execute(self.server.app)
  File "/usr/local/lib/python2.7/dist-packages/werkzeug/serving.py", line 168, in execute
    application_iter = app(environ, start_response)
  File "/usr/lib/python2.7/dist-packages/openerp/service/server.py", line 290, in app
    return self.app(e, s)
  File "/usr/lib/python2.7/dist-packages/openerp/service/wsgi_server.py", line 216, in application
    return application_unproxied(environ, start_response)
  File "/usr/lib/python2.7/dist-packages/openerp/service/wsgi_server.py", line 202, in application_unproxied
    result = handler(environ, start_response)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 1290, in __call__
    return self.dispatch(environ, start_response)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 1264, in __call__
    return self.app(environ, start_wrapped)
  File "/usr/local/lib/python2.7/dist-packages/werkzeug/wsgi.py", line 591, in __call__
    return self.app(environ, start_response)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 1264, in __call__
    return self.app(environ, start_wrapped)
  File "/usr/local/lib/python2.7/dist-packages/werkzeug/wsgi.py", line 591, in __call__
    return self.app(environ, start_response)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 1435, in dispatch
    result = ir_http._dispatch()
  File "/usr/lib/python2.7/dist-packages/openerp/addons/crm/ir_http.py", line 13, in _dispatch
    response = super(ir_http, self)._dispatch()
  File "/usr/lib/python2.7/dist-packages/openerp/addons/website/models/ir_http.py", line 148, in _dispatch
    resp = super(ir_http, self)._dispatch()
  File "/usr/lib/python2.7/dist-packages/openerp/addons/base/ir/ir_http.py", line 177, in _dispatch
    return self._handle_exception(e)
  File "/usr/lib/python2.7/dist-packages/openerp/addons/website/models/ir_http.py", line 196, in _handle_exception
    return super(ir_http, self)._handle_exception(exception)
  File "/usr/lib/python2.7/dist-packages/openerp/addons/base/ir/ir_http.py", line 147, in _handle_exception
    return request._handle_exception(exception)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 666, in _handle_exception
    return super(HttpRequest, self)._handle_exception(exception)
  File "/usr/lib/python2.7/dist-packages/openerp/addons/base/ir/ir_http.py", line 173, in _dispatch
    result = request.dispatch()
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 684, in dispatch
    r = self._call_function(**self.params)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 310, in _call_function
    return checked_call(self.db, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/openerp/service/model.py", line 113, in wrapper
    return f(dbname, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 307, in checked_call
    return self.endpoint(*a, **kw)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 803, in __call__
    return self.method(*args, **kw)
  File "/usr/lib/python2.7/dist-packages/openerp/http.py", line 403, in response_wrap
    response = f(*args, **kw)
  File "/usr/lib/python2.7/dist-packages/openerp/addons/payment_authorize/controllers/main.py", line 24, in authorize_form_feedback
    request.env['payment.transaction'].sudo().form_feedback(post, 'authorize')
  File "/usr/lib/python2.7/dist-packages/openerp/api.py", line 239, in wrapper
    return new_api(self, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/openerp/api.py", line 463, in new_api
    result = method(self._model, cr, uid, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/openerp/addons/payment/models/payment_acquirer.py", line 440, in form_feedback
    tx = getattr(self, tx_find_method_name)(cr, uid, data, context=context)
  File "/usr/lib/python2.7/dist-packages/openerp/api.py", line 241, in wrapper
    return old_api(self, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/openerp/api.py", line 336, in old_api
    result = method(recs, *args, **kwargs)
  File "/usr/lib/python2.7/dist-packages/openerp/addons/payment_authorize/models/authorize.py", line 115, in _authorize_form_get_tx_from_data
    raise ValidationError(error_msg)
ValidationError: Authorize: received data for reference SALE/2015/1234; no order found
```

# Contributers

Copyright © LasLabs, Inc. [https://laslabs.com]
License AGPL-3


* Written by Dave Lasley <dave@laslabs.com>