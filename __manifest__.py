# -*- coding: utf-8 -*-
{
    'name': 'HR Attendances Inherit',
    'summary' : 'Overtime Calculation, Check In/ Check Out',
    'author': 'IT Teams',
    'license': 'LGPL-3',
    'category': 'Attendances',
    'depends': [
        'hr',
        'barcodes',
        'hr_attendance',
        ],
    'data' : [
        'views/hr_attendance.xml',
        'views/hr_leave_type_views.xml',
        'security/ir.model.access.csv',
        'wizard/attendance_import_wizard.xml',
    ],
    'version': '17.0.1.0.0',
    'installable': True,
}