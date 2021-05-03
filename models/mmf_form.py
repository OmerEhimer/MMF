from odoo import api, fields, models ,tools
from odoo.tools.translate import _
from odoo.exceptions import ValidationError,Warning
from datetime import date, datetime
from logging import warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.fields import Date
from num2words import num2words

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    mmf_form_id = fields.Many2one('mmf.form', string='Form')



class MmfForm(models.Model):
    _name = 'mmf.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='name_seq'
    _description = 'Convert Form'
    _order = "name_seq desc"

    name_seq = fields.Char(string='Convert Form ID', copy=False, readonly=True, index=True, default=lambda self: _('New'))
    name_ar = fields.Char(string='Name',track_visibility="always",)
    price_word = fields.Char(string='Price in word',track_visibility="always",compute='_compute_price')
    # first_name = fields.Char(string='First Name', required=True,track_visibility='always')
    # middle_name = fields.Char(string='Middle Name',required=True,track_visibility='always')
    # last_name = fields.Char(string='Last Name', required=True, track_visibility='always')
    # fourth_name = fields.Char(string='Fourth Name',required=True,track_visibility='always')   
    department_id = fields.Many2one('mmf.department',string="Department",track_visibility="always")
    initial_diagnosis = fields.Text(string='Initial Diagnosis',track_visibility='always') 
    end_diagnosis = fields.Text(string='End Diagnosis',track_visibility='always') 
    # doctor_report = fields.Text(string='Doctor Report',track_visibility='always') 

    form_date = fields.Datetime(string='form Date')
    category = fields.Selection([
        ('1', 'ضابط'),
        ('2', 'ضابط صف/جندي'),
        ('3', 'مكفول'),
        
    ], string="Category" , track_visibility="always" )    
    officer = fields.Selection([
        ('1', 'فريق اول'),
        ('2', 'فريق'),
        ('3', 'لواء'),
        ('4', 'عميد'),
        ('5', 'عقيد'),
        ('6', 'مقدم'),
        ('7', 'رائد'),
        ('8', 'نقيب'),
        ('9', 'م.أول'),
        ('10', 'ملازم'),
    ], string="Officer" , track_visibility="always",)
    
    warrant_officer = fields.Selection([
        ('1', 'مساعد'),
        ('2', 'ر.أول'),
        ('3', 'رقيب'),
        ('4', 'عريف'),
        ('5', 'و.عريف'),
        ('6', 'جندي'),
        ('7', 'متعاقد'),
    ], string="Warrant Officer" , track_visibility="always",)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),        
    ], string="Gender" , track_visibility="always") 
    convert_type = fields.Selection([
        ('new', 'New Convert'),
        ('follow_up', 'Follow up'),
        ('convert', 'Converted'),
        ('emergency', 'Emergency '),

    ], string="Convert Type" , track_visibility="always",default='new' ) 
    relation_type = fields.Selection([
        ('1', 'Father'),
        ('2', 'Mother'),
        ('3', 'Husband/Wife'),
        ('4', 'Son/Daughter'),
    ], string="Relation Type" , track_visibility="always", )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('wait_manager', ' Wait Manager Approve'),
        ('request_processed', 'Request Processed'),
        ('confirm', 'Confirm'),
        ('close', 'Close'),

    ],string='State',  readonly=True, default='draft',) 

    card_no = fields.Char(string='Card NO', track_visibility="always")
    Age = fields.Integer(string='Age',track_visibility="always")
    phone = fields.Char(string='Phone', track_visibility="always")
    location = fields.Char(string='Location', track_visibility="always")
    user_id = fields.Many2one('res.users',string="Resposible",readonly="1",default=lambda self:self.env.user)
    company_id = fields.Many2one(string='company', comodel_name='res.company',readonly="1", default=lambda self: self.env.user.company_id)
    hospital_id = fields.Many2one('res.partner',string="Hospital", readonly="1",required=True, default=lambda self:self.env.user.hospital_id.id)

    month = fields.Integer(string='Month', track_visibility="always")
    year = fields.Integer(string='Year', track_visibility="always")
    # need_approve  = fields.Boolean(string="Need Approve",track_visibility="always",)

    service_line = fields.One2many(comodel_name="mmf.service.lines", inverse_name="form_id",string="Service ID")
    service_wait_line = fields.One2many(comodel_name="mmf.service.wait.lines", inverse_name="form_id",string="Service Wait ID")
     
    convertFormDate  = fields.Date(string='Convert Form Date',track_visibility="always",required=True,store=True,)
    currency_id = fields.Many2one("res.currency",  string="Currency", readonly=True,)
    price_total = fields.Monetary(string='Total',   compute='_amount_all', track_visibility='always',)
    # tmp_service_id = fields.Many2one('mmf.service',string="Service", required=True,track_visibility="always")
    # tmp_service_type_id = fields.Many2one('mmf.service.type',string="Service Type", required=True,track_visibility="always")
    related_invoice_ids = fields.One2many('account.invoice', 'mmf_form_id', string='Related Invoice')
    count_invoice_line = fields.Integer(compute='get_count_invoice_line' , string="Count Service")  


    @api.multi
    def count_service_line(self):
        return {
            'name': _('Service'),
            'domain': [('form_id','=', self.ids)],
            'view_type': 'form',
            'res_model': 'mmf.service.lines',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    @api.multi
    def get_count_invoice_line(self): 
        for rec in self:   
            count_invoice = rec.env['mmf.service.lines'].search_count([('form_id','=', self.ids)])
            self.count_invoice_line=count_invoice
    
    def action_invoiced(self):
        return {
            'name' : _('Create Invoice'),
            'view_type': 'form',
            'res_model': 'mmf.inv.wiz',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'context' : {'default_form_id' : self.id, 'default_date' : date.today()},
            'target' : 'new',
        }


    def create_invoice(self, inv_date):
        invoice_lines = []
        for line in self.service_line:
            if line.state == 'done' :
                line.state = 'invoiced'
                product_id = line.service_id.get_product()
                vals = {
                    'product_id' : product_id.id,
                    'quantity' : line.quantity,
                    'price_unit' : line.discount > 0 and line.service_price * line.discount / 100.0 or line.service_price,
                    'name' : line.service_id.name,
                    'account_id' : product_id.property_account_expense_id.id
                }
            # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>' , line.total)
                invoice_lines.append((0,0,vals))
        if invoice_lines : 
            invoice_vals = {
                'partner_id' : self.hospital_id.id,
                'date_invoice' :inv_date,
                'invoice_line_ids' : invoice_lines,
                'type' : 'in_invoice',
                'mmf_form_id' : self.id ,
            }
            invoice_obj = self.env.get('account.invoice').create(invoice_vals)
            invoice_obj.action_invoice_open()
        #self.state = 'invoiced'

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
                vals['name_seq'] = self.env['ir.sequence'].next_by_code('mmf.form.sequence') or _('New')
        result = super(MmfForm, self).create(vals)
        result.year = result.convertFormDate.year
        result.month = result.convertFormDate.month
        return result
    
    @api.depends('price_total')
    def _compute_price(self):
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])

        for record in self:
            x=25000
            obj=num2words(record.price_total,lang=lang.iso_code)
            record.price_word=str(obj)+' جنيه سوداني لا غير ' 
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",obj)
            # record.price+_word=a
    
    @api.depends('service_line')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            price_total = 0.0
            for line in order.service_line:
                price_total += line.total
            order.update({
                'price_total': price_total
            })    
   
    
    @api.multi
    @api.constrains("convertFormDate")
    def _check_field(self):
        for s in self:
            if s.convertFormDate < Date.today():
                raise ValidationError(_("Invalid Convert Form Date"))

    # @api.onchange('convertFormDate')              
    # def _compute_convertFormDate(self):
    #     for record in self:
    #         if record.convertFormDate:
    #             record.year = record.convertFormDate.year
    #             record.month= record.convertFormDate.month
              
    @api.multi
    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone and len(rec.phone) != 10:
                raise ValidationError(_("Invalid Phone Number..."))

        return True    
    def action_draft(self):
        self.state='draft'

       
    def action_confirm(self):
        self.state='confirm'
        # print(">>>>>>>>>SERVICES>>>>>>>>>>",self.tmp_service_id.name)
        # print(">>>>>>>>>SERVICES TYPE>>>>>>>>>>",self.tmp_service_id.name)
        
    def action_close(self):
        if self.price_total != 0:
            for line in self.service_line :
                if line.state != 'invoiced':
                    raise ValidationError(_("You Must Done and Invoice all Servieces Before Closing"))
            self.state='close'
        else:        
            raise ValidationError(_("You Must be Select One Service..."))

    def action_manager_approve(self):

        # for rec in self.service_line:
        #     if rec.service_type_id.need_approve and not rec.approved_by:
        #         # print(">>>>>>>>>>>>>>>>>>>>>>>>> ",rec.service_id.name)
        #         rec.approved_by=self.env.user

        for rec in self.service_wait_line:
            if rec.state=='wait':
                # print(">>>>>>>>>>>>>>>>>",rec.service_price)
                vals={
                'service_type_id':rec.service_type_id.id,
                'service_id':rec.service_id.id,
                'service_price':rec.service_price,
                'quantity' : rec.quantity,
                'approved_by':self.env.user.id,
                'created_by':rec.created_by.id,
                'attachment':rec.attachment,
                'form_id':self.id,
            }
                                
                self.env['mmf.service.lines'].create(vals)
                rec.state='approved'
                self.state='request_processed'
        # self.state='request_processed'
    def action_manager_reject(self):
        for rec in self.service_wait_line:
            if rec.state=='wait':
                rec.state='reject'
            self.state='request_processed'   
        
    def action_approve(self):
        if self.message_main_attachment_id.id is False:
            raise Warning(_("Please attach document for Convert"))
           
        else:
            self.state='approve'


class mmfServiceLines(models.Model):
    _name='mmf.service.lines'
    _description=' Services Lines'
    
    service_id = fields.Many2one('mmf.service',string="Service", required=True,track_visibility="always")
    service_type_id = fields.Many2one('mmf.service.type',string="Service Type", required=True,track_visibility="always")
    serviceDate  = fields.Date(string='Service Date',default=fields.Date.today(),required=True, )
    service_price = fields.Integer('Service Price',required=True,readonly=1,store=True)
    discount = fields.Integer('Discount',required=True,related='service_type_id.discount')
    total = fields.Integer('Sub Total',required=True,compute='compute_total_line',)
    patient_amount=fields.Float(string="Patient Amount" , compute="_get_patient_amount")
    need_approve  = fields.Boolean(string="Need Approve",track_visibility="always",related='service_type_id.need_approve')
    attachment = fields.Binary(string='Attachment',required=True,)
    # doctor_report = fields.Text(string='Doctor Report',track_visibility='always') 
    created_by = fields.Many2one('res.users',string="Resposible",readonly="1")
    approved_by = fields.Many2one('res.users',string="Approved By",readonly="1")
    quantity = fields.Integer(string="Quantity" ,default=1,)
    date_done  = fields.Date(string="Date Done")


    form_id = fields.Many2one('mmf.form',string="Form", required=True,track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('invoiced', 'Invoiced')
       
    ], string="State" , track_visibility="always",required=True,default='draft', ) 
     
    def action_done(self):
        for rec in self:
            rec.date_done = Date.today()
            rec.state='done'

    def action_delete(self):
        for rec in self:
            rec.unlink()

    @api.depends('discount','service_price','service_type_id','quantity')
    def compute_total_line(self):
        total=0
        for order in self:
            if order.discount != 0:
                order.total= (order.quantity * order.service_price * order.discount / 100)
            else:
                 order.total = (order.quantity * order.service_price)

    @api.depends('service_price','total','quantity')             
    def _get_patient_amount(self):
        for rec in self:
            rec.patient_amount=(rec.quantity * rec.service_price-rec.total) 

class HospitalDasboard(models.Model):
    _name = 'mmf.hospital.dashboard'    
    
    count_draft= fields.Integer(compute='get_draft_action' , string="Draft")  
    count_approve= fields.Integer(compute='get_approve_action' , string="Approve")  
    count_wait= fields.Integer(compute='get_wait_action' , string="Wait")  
    count_close= fields.Integer(compute='get_close_action' , string="Close")  
    month_price= fields.Integer(compute='get_price_month' , string="This Month")  
    day_price= fields.Integer(compute='get_price_day' , string="This Day")  
    color = fields.Integer()
    hospital_id = fields.Many2one('res.partner',string="Hospital")

    @api.multi
    def get_draft_action(self): 
        for rec in self:
               
            count_action_draft = rec.env['mmf.form'].search_count([('hospital_id','=', rec.hospital_id.id),('state','=', 'draft')])
            rec.count_draft=count_action_draft

    @api.multi
    def get_approve_action(self): 
        for approve in self:   
            count_action_approve = approve.env['mmf.form'].search_count([('hospital_id','=', approve.hospital_id.id),('state','=', 'approve')])
            approve.count_approve=count_action_approve


    @api.multi
    def get_wait_action(self): 
        for wait in self:   
            count_action_wait = wait.env['mmf.form'].search_count([('hospital_id','=', wait.hospital_id.id),('state','=', 'wait_manager')])
            wait.count_wait=count_action_wait

    @api.multi
    def get_close_action(self): 
        for close in self:   
            count_action_close = close.env['mmf.form'].search_count([('hospital_id','=', close.hospital_id.id),('state','=', 'close')])
            close.count_close=count_action_close

    
    @api.multi
    def get_price_day(self): 
        for price in self:   
            today = date.today()
            day_total_price=0
            company_ids = price.env['mmf.form'].search([('hospital_id','=', price.hospital_id.id),('convertFormDate','=',Date.today())])
            # print("************************************",company_ids)
            if company_ids:
                day_total_price = sum(company['price_total'] for company in company_ids)
                
            price.day_price=day_total_price

    @api.multi
    def get_price_month(self): 
        for price in self:   
            today = datetime.today()
            month=today.month
            year=today.year
            total_price=0
            company_ids = price.env['mmf.form'].search([('hospital_id','=', price.hospital_id.id),('month','=',month ),('year','=',year )])
            if company_ids:
                total_price = sum(company['price_total'] for company in company_ids)

            price.month_price=total_price

class SaleOrderInherit(models.Model):
    _inherit = 'res.partner'    

    count_draft= fields.Integer(compute='get_draft_action' , string="Draft")  
    count_approve= fields.Integer(compute='get_approve_action' , string="Approve")  
    count_wait= fields.Integer(compute='get_wait_action' , string="Wait")  
    count_close= fields.Integer(compute='get_close_action' , string="Close")  
    month_price= fields.Integer(compute='get_price_month' , string="This Month")  
    day_price= fields.Integer(compute='get_price_day' , string="This Day")  
    color = fields.Integer()
    is_hospital = fields.Boolean(string="Is Hospital")

    @api.model
    def create(self, vals):
        obj = super(SaleOrderInherit, self).create(vals)
        self.env.get('mmf.hospital.dashboard'). create({
            'hospital_id' : obj.id
        })
        return obj

    def unlink(self):
        for obj in self:
            self.env.get('mmf.hospital.dashboard').search([('hospital_id','=', obj.id)]).unlink()
        return super(SaleOrderInherit, self).unlink()

    def write(self, vals):
        res = super(SaleOrderInherit, self).write(vals)
        if 'is_hospital' in vals :
            for obj in self :
                if obj.is_hospital :
                    self.env.get('mmf.hospital.dashboard'). create({
                            'hospital_id' : obj.id
                        })
                else :
                    self.env.get('mmf.hospital.dashboard').search([('hospital_id','=', obj.id)]).unlink()
        return res


    @api.multi
    def get_draft_action(self): 
        for rec in self:   
            count_action_draft = rec.env['mmf.form'].search_count([('hospital_id','=', rec.id),('state','=', 'draft')])
            rec.count_draft=count_action_draft

    @api.multi
    def get_approve_action(self): 
        for approve in self:   
            count_action_approve = approve.env['mmf.form'].search_count([('hospital_id','=', approve.id),('state','=', 'approve')])
            approve.count_approve=count_action_approve


    @api.multi
    def get_wait_action(self): 
        for wait in self:   
            count_action_wait = wait.env['mmf.form'].search_count([('hospital_id','=', wait.id),('state','=', 'wait_manager')])
            wait.count_wait=count_action_wait

    @api.multi
    def get_close_action(self): 
        for close in self:   
            count_action_close = close.env['mmf.form'].search_count([('hospital_id','=', close.id),('state','=', 'close')])
            close.count_close=count_action_close

    
    @api.multi
    def get_price_day(self): 
        for price in self:   
            today = date.today()
            day_total_price=0
            company_ids = price.env['mmf.form'].search([('hospital_id','=', price.id),('convertFormDate','=',Date.today())])
            # print("************************************",company_ids)
            if company_ids:
                day_total_price = sum(company['price_total'] for company in company_ids)
                
            price.day_price=day_total_price
    @api.multi
    def get_price_month(self): 
        for price in self:   
            today = datetime.today()
            month=today.month
            year=today.year
            total_price=0
            company_ids = price.env['mmf.form'].search([('hospital_id','=', price.id),('month','=',month ),('year','=',year )])
            if company_ids:
                total_price = sum(company['price_total'] for company in company_ids)

            price.month_price=total_price
    
class mmfServiceWaitLines(models.Model):
    _name='mmf.service.wait.lines'
    _description=' Services Lines'
    
    service_id = fields.Many2one('mmf.service',string="Service", required=True,track_visibility="always")
    service_type_id = fields.Many2one('mmf.service.type',string="Service Type", required=True,track_visibility="always")
    service_price = fields.Float('Service Price',required=True,readonly=1,store=True)
    created_by = fields.Many2one('res.users',string="Resposible",readonly="1")
    attachment = fields.Binary(string='Attachment',required=True, )
    form_id = fields.Many2one('mmf.form',string="Form", required=True,track_visibility='onchange')
    state = fields.Selection([
        ('wait', 'Wait'),
        ('approved', 'Approved'),
        ('reject', 'Rejected'),
        ('converted', 'Converted'),
    ], string="State" , track_visibility="always",required=True, ) 
    quantity = fields.Integer(string="Quantity" ,default=1,)


    def action_delete(self):
        for rec in self:
            rec.unlink()

class UsersInhert(models.Model):
    _inherit = 'res.users'

    hospital_id = fields.Many2one('res.partner',string="Hospital", default=lambda self:self.env.user.hospital_id.id)
