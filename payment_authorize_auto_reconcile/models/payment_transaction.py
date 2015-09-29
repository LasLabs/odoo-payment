# -*- coding: utf-8 -*-
from openerp import models, fields, api


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    
    @api.model
    def _send_thankyou_message(self, pay_amount, invoice):
        ''' Send a thankyou message to partners subscribed to the invoice  '''
        last_message = invoice.message_ids[-1]
        thread = self.env['mail.thread'].browse(last_message.res_id)
        
        thread.sudo().message_post(
            subject = 'Payment Received',
            body =  'Hi %s,<br /><br />Your payment of %s has been received for invoice %s.<br /><br />We appreciate your business!' % (
                invoice.partner_id.name, pay_amount, invoice.number
            ),
            partner_ids = [ invoice.partner_id.id ]
        )
    
    @api.model
    def _authorize_form_get_tx_from_data(self, data):
        """ Given a data dict coming from authorize, verify it and find the related
        transaction record. Create transaction record if one doesn't exist. """
        
        reference, trans_id, fingerprint = data.get('x_invoice_num'), data.get('x_trans_id'), data.get('x_MD5_Hash')
        
        if not reference or not trans_id or not fingerprint:
            error_msg = 'Authorize: received data with missing reference (%s) or trans_id (%s) or fingerprint (%s)' % (reference, trans_id, fingerprint)
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        
        tx = self.search([('reference', '=', reference)])
        
        if not tx:
            
            invoice = self.env['account.invoice'].search([
                ('internal_number', '=', reference)
            ], limit=1)
            acquirer = self.env['payment.acquirer'].search([
                ('provider', '=', 'authorize'),
                ('company_id', '=', invoice.company_id.id)
            ], limit=1)
            
            pay_amount = data.get('x_amount')
            
            tx = [ self.create( {
                'reference': reference,
                'acquirer_id': acquirer.id,
                'amount': pay_amount,
                'state': 'draft',
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_country_id': invoice.partner_id.country_id.id,
                'partner_state': data.get('x_state'),
                'partner_city': data.get('x_city'),
                'partner_street': data.get('x_address'),
            } ) ]
            
            invoice.pay_and_reconcile(
                pay_amount = pay_amount,
                pay_account_id = invoice.account_id.id,
                period_id = invoice.period_id.id,
                pay_journal_id = invoice.journal_id.id,
                writeoff_acc_id = invoice.account_id.id,
                writeoff_period_id = invoice.period_id.id,
                writeoff_journal_id = invoice.journal_id.id,
                name = 'Authorize.net Transaction ID %s' % data.get('x_trans_id', 0),
            )
            
            #self._send_thankyou_message(pay_amount, invoice)
        
        elif len(tx) > 1:
            error_msg = 'Authorize: received data for reference %s' % (reference)
            error_msg += '; multiple orders found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        
        return tx[0]
    