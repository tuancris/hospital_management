# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Management',
    'version': '0.0.1',
    'category': 'hospital',
    'author': 'tuấn',
    'sequence': -100,
    'summary': 'hospital management system',
    'description': """ hospital management system """,
    'depends': ["mail", "report_xlsx"],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/appointment_wizard_view.xml',
        'views/patient_view.xml',
        'views/doctors_view.xml',
        'views/female_patient_view.xml',
        'views/male_patient_view.xml',
        'views/appointment_view.xml',
        'views/partner.xml',
        'report/report.xml',
        'report/patient_card.xml',
        'report/appointment_details.xml',
        'views/appointment_report_wizard_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
