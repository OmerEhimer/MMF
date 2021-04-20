
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words
class ReprotServicesRequestWizard(models.TransientModel):
	_name = 'reprot.services.request'
	company_id = fields.Many2one(string='Choose Hospital', comodel_name='res.company', required=True, default=lambda self: self.env.user.company_id)
	
	def year_selection(self):
		year = 2020 # replace 2000 with your a start year
		year_list = []
		while year != 2051: # replace 2030 with your end year
			year_list.append((str(year), str(year)))
			year += 1
		return year_list

	year = fields.Selection(
		year_selection,
		string="Choose Year",
		default="2021", # as a default value it would be 2019
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
		], string="Chooes Month")  

	def get_service_types(self, form_id):
		types = []
		res = []
		for line in form_id.service_line:
			if line.service_type_id.id not in types : 
				types.append(line.service_type_id.id)
				res.append({
					'id' : line.service_type_id.id ,
					'name' : line.service_type_id.name,
					})
		return res
	

	def get_services(self, form_id):
		res = []
		for line in form_id.service_line :
			vals = {
				'service_id':line.service_id.name,
				'form_id':line.form_id,
				'service_price':line.service_price,
				'service_type_id':line.service_type_id.id,
			} 
			res.append(vals)
		return res

	def get_report(self):
		data={
			'model':'reprot.services.request',
			'form':self.read()[0]
			}
			 
		company_id = data['form']['company_id'][0]
		month = data['form']['month']
		year = data['form']['year']
			 
		filter_data_request = self.env['mmf.form'].search([('company_id','=', self.company_id.id)
		,('year','=', year),('month','=', month)])
		filter_service_type_request = self.env['mmf.service.type'].search([])
			 
		request_data_list = []
		for fetch_req in filter_data_request:
			valus = {
				'id':fetch_req,
				'company_id':fetch_req.company_id.name,
				'month':fetch_req.month,
				'year':fetch_req.year,
				'name_seq':fetch_req.name_seq,
				'name_ar':fetch_req.name_ar,
				'convert_type':fetch_req.convert_type,
				'service_line':fetch_req.service_line,
				'user_id':fetch_req.user_id.name,
				'convertFormDate':fetch_req.convertFormDate,
				'Age':fetch_req.Age,
				'gender':fetch_req.gender,
				'end_diagnosis':fetch_req.end_diagnosis,
				'initial_diagnosis':fetch_req.initial_diagnosis,
				'service_types' : self.get_service_types(fetch_req),
				'services' : self.get_services(fetch_req),
					} 
			request_data_list.append(valus)

			data['filter_data_request'] = request_data_list
			
		return self.env.ref('mmf.services_request_wizard').report_action(self, data=data)


