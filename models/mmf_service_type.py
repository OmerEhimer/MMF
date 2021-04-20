from odoo import api, fields, models
from odoo.tools.translate import _


class MmfServiceType(models.Model):
    _name = 'mmf.service.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Convert Service Type'

    name = fields.Char(string='Name',required=True,track_visibility="always")
    user_id = fields.Many2one('res.users',string="Resposible",readonly="1",default=lambda self:self.env.user)
    need_approve  = fields.Boolean(string="Need Approve",track_visibility="always")
    update_price  = fields.Boolean(string="Update Price",track_visibility="always")
    discount = fields.Integer(string='Discount %')

    _sql_constraints = [
        (
            'constraint_uniq_name',
            'unique(name)',
            'This Name Is Existed'
        ),
    ]