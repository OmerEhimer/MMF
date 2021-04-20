from odoo import api, fields, models
from odoo.tools.translate import _


class MmfDepartment(models.Model):
    _name = 'mmf.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Department'

    name = fields.Char(string='Name',required=True,track_visibility="always")
    user_id = fields.Many2one('res.users',string="Resposible",readonly="1",default=lambda self:self.env.user)    

    _sql_constraints = [
        (
            'constraint_uniq_name',
            'unique(name)',
            'This Name Is Existed'
        ),
    ]  