# from odoo import models

# # How To Create Excel/XLS Report in Odoo
# class PatientCardXls(models.AbstractModel):
#     _name = 'report.om_hospital.report_patient_xls'
#     _inherit = 'report.report_xlsx.abstract'

#     def generate_xlsx_report(self, workbook, data, lines):
#         format1 = workbook.add_format({'font_size':14, 'align':'center','bold':True}) 
#         format2 = workbook.add_format({'font_size':12, 'align':'left'}) 
#         sheet= workbook.add_worksheet('Patient Card')
#         sheet.write(2,2, 'Name' ,format1)
#         sheet.write(2,3, lines.patient_name ,format2)
#         sheet.write(3,2, 'Age' ,format1)
#         sheet.write(3,3, lines.patient_age ,format2)
#         sheet.write(4,2, 'Gender' ,format1)
#         sheet.write(4,3, lines.gander ,format2)
#         sheet.write(5,2, 'E.mail' ,format1)
#         sheet.write(5,3, lines.email_id ,format2)
        