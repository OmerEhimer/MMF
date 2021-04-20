# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class requestServicelines(models.TransientModel):
    _name = 'request.service.line'

    req_id = fields.Many2one('request.service', string='Request')
    service_type_id = fields.Many2one('mmf.service.type',string="Service Type", required=True,track_visibility="always")
    service_id = fields.Many2one('mmf.service',string="Service", required=True,track_visibility="always")
    service_price = fields.Integer(string="Service Price",related='service_id.price',)
    new_service_price = fields.Integer(string="New Service Price")
    update_price  = fields.Boolean(string="Update Price",related='service_type_id.update_price',track_visibility="always")
    quantity = fields.Integer(string="Quantity" ,default=1,)


class requestService(models.TransientModel):
    _name = 'request.service'

    form_id = fields.Many2one('mmf.form',string="Form", required=True,track_visibility="always",readonly="1")
    patient_name = fields.Char(string="Patinet Name",related='form_id.name_ar',readonly="1" )
    service_line_ids = fields.One2many('request.service.line', 'req_id', string='Lines')
    user_id = fields.Many2one('res.users',string="Resposible",readonly="1",default=lambda self:self.env.user)
    attachment = fields.Binary(string='Attachment',required=True,  attachment=True)
    
    
    @api.onchange('service_type_id')
    def onchange_field(self):
        self.service_id = ''
    
    def request_service(self):
        form_lines = []
        for line in self.service_line_ids:
            if line.update_price:
                vals={
                    'service_type_id':line.service_type_id.id,
                    'service_id':line.service_id.id,
                    'service_price':line.new_service_price,
                    'quantity':line.quantity,
                    'created_by':self.user_id.id,
                    'attachment':self.attachment,
                    'form_id':self.form_id.id,
                }
                if line.service_type_id.need_approve:
                    vals1={
                    'service_type_id':line.service_type_id.id,
                    'service_id':line.service_id.id,
                    'service_price':line.new_service_price,
                    'quantity':line.quantity,
                    'attachment':self.attachment,
                    'state':'wait',
                    'form_id':self.form_id.id,
                }
                                    
                    self.form_id.state='wait_manager'
                    self.env['mmf.service.wait.lines'].create(vals1)
                else:
                    self.env['mmf.service.lines'].create(vals)
            else:
                vals={
                    'service_type_id':line.service_type_id.id,
                    'service_id':line.service_id.id,
                    'service_price':line.service_price,
                    'quantity':line.quantity,
                    'created_by':self.env.user.id,
                    'attachment':self.attachment,
                    'form_id':self.form_id.id,
                }
                if line.service_type_id.need_approve:
                    vals1={
                    'service_type_id':line.service_type_id.id,
                    'service_id':line.service_id.id,
                    'service_price':line.service_price,
                    'quantity':line.quantity,
                    'created_by':self.env.user.id,
                    'attachment':self.attachment,
                    'state':'wait',
                    'form_id':self.form_id.id,
                }
                                    
                    self.form_id.state='wait_manager'
                    self.env['mmf.service.wait.lines'].create(vals1)
                else:
                    self.env['mmf.service.lines'].create(vals)
   
  