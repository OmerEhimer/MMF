# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from num2words import num2words
class MonthlyTotalForHospital(models.TransientModel):
      _name = 'monthly.total'

      company_id = fields.Many2one(string='Hospital', comodel_name='res.company', required=True, default=lambda self: self.env.user.company_id)
   
      def year_selection(self):
            year = 2020 # replace 2000 with your a start year
            year_list = []
            while year != 2051: # replace 2030 with your end year
                  year_list.append((str(year), str(year)))
                  year += 1
            return year_list

      year = fields.Selection(
            year_selection,
            string="Year",
              default="2021", required=True # as a default value it would be 2019
         ) 

      month = fields.Selection([
        ('1', 'يناير'),
        ('2', 'فبراير'),
        ('3', 'مارس'),
        ('4', 'ابريل'),
        ('5', 'مايو'),
        ('6', 'يونيو'),
        ('7', 'يوليو'),
        ('8', 'أغسطس'),
        ('9', 'سبتمبر'),
        ('10', 'أكتوبر'),
        ('11', 'نوفمبر'),
        ('12', 'ديسمبر'),
     ], string="Month" , required=True)  

      @api.multi
      def get_report(self):
            active_ids=self.env.context.get('active_ids',[]) 
            data={
            'ids':active_ids,
            'model':'mmf.invoice',
            'form':self.read()[0]
            }
            return self.env.ref('mmf.monthly_total_report').report_action(self, data=data)


class ReportMonthlyTotalAbstract(models.AbstractModel):

      _name = 'report.mmf.report_monthly'

      def get_price_word(self,ammount):
            lang_code = self.env.context.get('lang') or self.env.user.lang
            lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
            word=""
            obj=num2words(ammount,lang='ar')
            word=str(obj)
            # print("+++++++++++++++++++++++++++++",obj)

            return word 

      @api.model
      def _get_report_values(self, docids, data=None):

            if not data.get('form'):
                  raise UserError('Not Fount')

            company_id = ''
            month = ''
            year = ''
      
            if data['form']['company_id']:            
                  company_id = data['form']['company_id']

            if data['form']['month']:            
                  month = data['form']['month']    #[0]

            if data['form']['year']:            
                  year = data['form']['year']   

            total = 0

            if company_id and  month:
            
                  invoice_ids = self.env['mmf.invoice'].search([('company_id','=',company_id[0]),('month','=',month),('year','=',year)])
                  if invoice_ids:
                        total = sum(invoice['price'] for invoice in invoice_ids)

                  if month =='1' :
                        month='يناير'
                  elif month=='2':
                        month='فبراير' 
                  elif month=='3':
                        month='مارس' 
                  elif month=='4':
                        month='أبرايل' 
                  elif month=='5':
                        month='مايو' 
                  elif month=='6':
                        month='يونيو'            
                  elif month=='7':
                        month='يوليو' 
                  elif month=='8':
                        month='أغسطس' 
                  elif month=='9':
                        month='سبتمبر' 
                  elif month=='10':
                        month='أكتوبر'
                  elif month=='11':
                        month='نوفمبر'
                  elif month=='12':
                        month='ديسمبر'  
            
            docs = []
            docs.append({
                  'company_id': company_id[1],
                  'month': month,
                  'year':year,
                  'price': float(total),
                  'price_word' : self.get_price_word(total)
            })
            
            return{
                  'docs_id':'docs_id',
                  'doc_model':'mmf.invoice',
                  'docs':docs,
                  'data':data,
            }
