from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.fields import Date


class MmfInvoice(models.Model):
    _name = 'mmf.invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Invoices'
    _rec_name='name_seq'
    _order = "name_seq desc"
    
    name_seq = fields.Char(string='Invoice ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_name=fields.Char(string="Patient Name",required=True,track_visibility="always" )   
    form_id=fields.Many2one('mmf.form',string="Form ID",required=True,track_visibility="always" )   
    convertFormDate  = fields.Date(string='Convert Form Date',required=True, track_visibility="always",) #default=fields.Date.today()
    convert_type = fields.Selection([
        ('new', 'New Convert'),
        ('follow_up', 'Follow up'), 
        ('convert', 'Converted'),       
    ], string="Convert Type" , track_visibility="always",required=True, ) 
    price = fields.Integer(string='Price', required=True,track_visibility='always')
    user_id = fields.Many2one('res.users',string="Resposible",readonly="1",default=lambda self:self.env.user)
    hospital_id = fields.Many2one('res.partner',string="Hospital", readonly="1",required=True, default=lambda self:self.env.user.hospital_id.id)
    month = fields.Integer(string='Month', required=True,track_visibility="always",readonly=1)
    year = fields.Integer(string='Year', required=True,track_visibility="always")
    

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
                vals['name_seq'] = self.env['ir.sequence'].next_by_code('mmf.invoice.sequence') or _('New')
        result = super(MmfInvoice, self).create(vals)
        return result