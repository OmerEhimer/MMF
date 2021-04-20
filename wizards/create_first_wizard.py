# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CreateFirstWizard(models.TransientModel):
   _name = 'create.first.wizard'

   gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),        
    ], string="Gender" ,required=True, ) 

   date_start = fields.Date(string="Date Start")
   end_date = fields.Date(string="End Date")

   def print_report(self):
      data={
         'model':'create.first.wizard',
         'form':self.read()[0]
      }

      selected_states = data['form']['gender'][0]
      test_states_list = self.env['mmf.form'].search([('gender','=', self.gender)
      ,('convertFormDate','>=', self.date_start),('convertFormDate','<=', self.end_date)])

      states_list =[]
      for fetch_value in test_states_list:
         vals = {
            'name_ar':fetch_value.name_ar,
            'middle_name':fetch_value.middle_name,
            'gender':fetch_value.gender
         } 
      
         states_list.append(vals)
      data['test_states_list'] = states_list
      return self.env.ref('mmf.send_to_report_type').report_action(self, data=data)



   