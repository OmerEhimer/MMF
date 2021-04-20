# -*- coding: utf-8 -*-
{
    'name' : 'Mutual Medical Fund Module',
    'version' : '1.0.0',
    'summary': 'Mutual Medical Fund',
    'sequence': 1,

    'author': 'RSF Developer',
    'category': 'Medical',
    'website': 'https://www.rsf.gov.sd/',
    'depends' : [
        'mail',
        'contacts',
        'base',
        'account',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',

        'wizards/request_service.xml',
        'wizards/convert_service.xml',
        'views/mmf_form.xml',
        'wizards/create_first_wizard.xml',
        'wizards/monthly_total_for_hospital.xml',
        'wizards/Frequency_report_wizard.xml',
        'wizards/services_request_wizard.xml',
        
        'views/mmf_service_type.xml',
        'views/mmf_service.xml',
        'views/mmf_invoice.xml',
        'views/mmf_department.xml',
        'views/mmf_dashboard.xml',
        'views/inhert_company.xml',
        'views/style_css.xml',   
        'views/mmf_add_hospital.xml',   


        #'reports/report.xml',

        'reports/style_css.xml',      
        # 'reports/appointments.xml',
        'reports/report.xml',
        'reports/report_monthly_total.xml',
        'reports/Frequency_report_hospital.xml',
        'reports/report_Services_request_hospital.xml',
        'reports/approve_request_report.xml',
        'reports/request_report.xml',

    ],
    # 'images': [''],
    'installable': True,
    'application': True,
    'auto_install': False,

}
