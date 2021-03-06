# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FrequencyReportWizard(models.TransientModel):
   _name = 'frequency.report.wizard'

   hospital_id = fields.Many2one(string='Hospital', comodel_name='res.partner', required=True, default=lambda self: self.env.user.hospital_id)

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
         selected = data['form']['hospital_id'][0]
         if self.date_start and self.end_date:
            filter_data = self.env['mmf.form'].search([('hospital_id','=', self.hospital_id.id)
            ,('convertFormDate','>=', self.date_start),('convertFormDate','<=', self.end_date)])

         elif self.date_start:
            filter_data = self.env['mmf.form'].search([('hospital_id','=', self.hospital_id.id)
            ,('convertFormDate','>=', self.date_start),])

         elif self.end_date:
                filter_data = self.env['mmf.form'].search([('hospital_id','=', self.hospital_id.id)
            ,('convertFormDate','<=', self.end_date),])

         else:
            filter_data = self.env['mmf.form'].search([('hospital_id','=', self.hospital_id.id)])
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
            state='??????????'
         elif fetch_v.state=='approve':
                state='???? ????????????????'
         elif fetch_v.state=='wait_manager':
                state='???? ???????????? ?????????????'
         elif fetch_v.state=='request_processed':
                state='?????? ???????????? ??????????'
         elif fetch_v.state=='confirm':
                state='???? ??????????????'
         elif fetch_v.state=='close':
                state='???? ????????????? '
         valus = {
            'hospital_id':fetch_v.hospital_id.name,
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
      hospital_id=''

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
