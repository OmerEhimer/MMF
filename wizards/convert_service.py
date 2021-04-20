# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date, datetime



class mmfInvoicing(models.TransientModel):
    _name = 'mmf.inv.wiz'

    date = fields.Date('Date')
    form_id = fields.Many2one('mmf.form', 'Form', readonly=True,)

    def create_invoice(self):
        self.form_id.create_invoice(self.date)
    
class mmfServiceLines(models.TransientModel):
    _name='convert.service.line'
    _description=' Services Lines'
    
    service_id = fields.Many2one('mmf.service',string="Service", required=True,track_visibility="always")
    service_type_id = fields.Many2one('mmf.service.type',string="Service Type", required=True,track_visibility="always")
    convert_id = fields.Many2one('convert.service', string='Convert')
    service_price = fields.Integer(string="Service Price",related='service_id.price',)
    new_service_price = fields.Integer(string="New Service Price")
    update_price  = fields.Boolean(string="Update Price",related='service_type_id.update_price',track_visibility="always")
    quantity = fields.Integer(string="Quantity" ,default=1,)


class convertService(models.TransientModel):
    _name='convert.service'

    form_id = fields.Many2one('mmf.form',string="Form", required=True,track_visibility="always",readonly="1")
    patient_name = fields.Char(string="Patinet Name",related='form_id.name_ar',readonly="1" )
    service_type_id = fields.Many2one('mmf.service.type',string="Service Type", track_visibility="always")
    service_id = fields.Many2one('mmf.service',string="Service", track_visibility="always")
    user_id = fields.Many2one('res.users',string="Resposible",readonly="1",default=lambda self:self.env.user)
    service_price = fields.Integer(string="Service Price",related='service_id.price',)
    hospital_id = fields.Many2one('res.partner',string="Hospital", required=True,)
    attachment = fields.Binary(string='Attachment',required=True, )
    convertFormDate  = fields.Date(string='Convert Form Date',track_visibility="always",)
    service_line_ids = fields.One2many('convert.service.line', 'convert_id', string='Lines')

    # department_id = fields.Many2one('mmf.department',string="Department",related='form_id.department_id',required=True,track_visibility="always")
    
    
    @api.onchange('service_type_id')
    def onchange_field(self):
        self.service_id = ''

    @api.onchange('hospital_id')
    def onchange_field(self):
        self.service_type_id=''
        self.service_id = ''

    def convert_service(self):
        form_lines = []
        vals={
                'name_ar':self.patient_name,
                'convert_type':'convert',
                'hospital_id' : self.hospital_id.id,
                'user_id':self.env.user.id,
                'department_id':self.form_id.department_id.id,
                'gender':self.form_id.gender,
                'Age':self.form_id.Age,
                'phone':self.form_id.phone,
                'location':self.form_id.location,
                'card_no':self.form_id.card_no,
                'category':self.form_id.category,
                'officer':self.form_id.officer,
                'relation_type':self.form_id.relation_type,
                'warrant_officer':self.form_id.warrant_officer,
                'convertFormDate':date.today(),
                'initial_diagnosis':self.form_id.initial_diagnosis,

                # 'attachment':self.attachment,
                # 'form_id':self.form_id.id,
            }
        form_obj = self.env['mmf.form'].create(vals)
        form_id = form_obj.id

        for line in self.service_line_ids:
            vals1={
                'service_type_id':line.service_type_id.id,
                'service_id':line.service_id.id,
                'service_price':line.service_price,
                'quantity':line.quantity,
                'created_by':self.user_id.id,
                'attachment':self.attachment,
                'form_id':form_id,
            }
            self.env['mmf.service.lines'].create(vals1)

        for rec in self.form_id.service_wait_line:
            if rec.state=='wait':
                rec.state='converted'
            self.form_id.state='request_processed'
  