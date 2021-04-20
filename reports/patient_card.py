# from odoo import models, api, _


# class PatientCardReport(models.AbstractModel):
#     _name = 'report.om_hospital.report_patient'
#     _description ='Patient Card Report'
    
#     @api.model
#     def _get_report_values(self, docids, data=None):   
#         print("Print Here AnyThing")
#         model = self.env.context.get('active_model')
#         docs = self.env['hospital.patient'].browse(docids[0])
#         appointment = self.env['hospital.appointment'].search([('patient_id','=', docids[0])])
#         appointment_list = []
#         for app in self:
#             vals = {
#                 'Age': app.patient_age,
#                 'Notes': app.notes,
#                 'Appointment date': app.appointment_date
#             }
#             appointment_list.append(vals)
#         return {
#             'doc_model': 'hospital.patient',
#             'data': data,
#             'docs': docs,
#             'appointment_list': appointment_list,
#         }
