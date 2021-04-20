# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FrequencyReportWizard(models.TransientModel):
   _name = 'frequency.report.wizard'

   company_id = fields.Many2one(string='Hospital', comodel_name='res.company',  default=lambda self: self.env.user.company_id)
   card_no = fields.Char(string='Card NO',track_visibility="always")
   report_by = fields.Selection([
        ('hospital', 'Hospital'),
        ('patient', 'Patient'),        
    ], string="Report By" ,required=True, ) 
   date_start = fields.Date(string="Date Start")
   end_date = fields.Date(string="End Date")

   def get_report(self):
      data={
         'model':'frequency.report.wizard',
         'form':self.read()[0]
      }
     
      if self.report_by=='hospital':
         selected = data['form']['company_id'][0]
         if self.date_start and self.end_date:
            filter_data = self.env['mmf.form'].search([('company_id','=', self.company_id.id)
            ,('convertFormDate','>=', self.date_start),('convertFormDate','<=', self.end_date)])
         elif self.date_start:
            filter_data = self.env['mmf.form'].search([('company_id','=', self.company_id.id)
            ,('convertFormDate','>=', self.date_start),])
         elif self.end_date:
                filter_data = self.env['mmf.form'].search([('company_id','=', self.company_id.id)
            ,('convertFormDate','<=', self.end_date),])
         else:
            filter_data = self.env['mmf.form'].search([('company_id','=', self.company_id.id)])
      elif  self.report_by=='patient':
         selected = data['form']['card_no']
         if self.date_start and self.end_date:
                filter_data = self.env['mmf.form'].search([('card_no','=', self.card_no)
            ,('convertFormDate','>=', self.date_start),('convertFormDate','<=', self.end_date)])
         elif self.date_start:
            filter_data = self.env['mmf.form'].search([('card_no','=', self.card_no)
            ,('convertFormDate','>=', self.date_start),])
         elif self.end_date:
                filter_data = self.env['mmf.form'].search([('card_no','=', self.card_no)
            ,('convertFormDate','<=', self.end_date),])
         else:
            filter_data = self.env['mmf.form'].search([('card_no','=', self.card_no)])
      
      frequency_list =[]
      for fetch_v in filter_data:
         state=""
         if fetch_v.state=='draft':
            state='مبدئي'
         elif fetch_v.state=='approve':
                state='تم الموافقة'
         elif fetch_v.state=='wait_manager':
                state='في إنتظار اﻹدارة'
         elif fetch_v.state=='request_processed':
                state='تمت معالجة الطلب'
         elif fetch_v.state=='confirm':
                state='تم التأكيد'
         elif fetch_v.state=='close':
                state='تم اﻹغلاق '
         valus = {
            'company_id':fetch_v.company_id.name,
            'name_seq':fetch_v.name_seq,
            'convertFormDate':fetch_v.convertFormDate,
            'price_total':fetch_v.price_total,
            'name_ar':fetch_v.name_ar,
            'state':state,
            'department_id':fetch_v.department_id.name,
         } 
         
         frequency_list.append(valus)
      data['filter_data'] = frequency_list
      # print("?????????????????????????",frequency_list)
      return self.env.ref('mmf.frequency_reports').report_action(self, data=data)


class FrequencyAbstract(models.AbstractModel):
    
   _name = 'report.mmf.frequency_report_hospital' 
   
   @api.model
   def _get_report_values(self, docids, data=None):

      date_start =''
      end_date =''   
      company_id=''

      date_start = data['form']['date_start']
      end_date = data['form']['end_date']

      docs = []
      docs.append({
            'date_start': date_start,
            'end_date': end_date,
      })

      return{
            'docs_id':'docs_id',
            'doc_model':'mmf.invoice',
            'date_start': date_start,
            'date_end': end_date,
            'docs': docs,
      }
