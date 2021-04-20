from odoo import api, fields, models
from odoo.tools.translate import _


class MmfService(models.Model):
    _name = 'mmf.service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Convert Service'

    name = fields.Char(string='Name',required=True,track_visibility="always")
    service_type_id=fields.Many2one('mmf.service.type',string="Service Type",required=True,track_visibility="always" )   
    price = fields.Integer(string='Price', required=True,track_visibility='always')
    user_id = fields.Many2one('res.users',string="Resposible",readonly="1",default=lambda self:self.env.user)    
    company_id = fields.Many2one(string='Company', comodel_name='res.company', required=True, default=lambda self: self.env.user.company_id)
    hospital_id = fields.Many2one('res.partner',string="Hospital", required=True, default=lambda self:self.env.user.hospital_id.id)


    #************************************************************************************/

    product_id = fields.Many2one('product.product', string='Product Name')

    def get_product(self):
        if self.product_id :
            return self.product_id
        product = self.env.get('product.product').create({'name' : self.name , 'standard_price' : self.price})
        self.product_id = product
        return product

    
    @api.model
    def create(self, vals):
        obj = super(MmfService, self).create(vals)
        obj.get_product()
        return obj


    @api.multi
    @api.depends('name', 'company_id')
    def name_get(self):
        result = []
        for record in self:
            if record.company_id.name:
                name = '[' + record.company_id.name + '] ' + record.name
            else:
                name = record.name
            result.append((record.id, name))
        return result

    _sql_constraints = [
        (
            'constraint_uniq_name',
            'Check(1=1)',
            'This Name Is Existed'
        ),
    ]    