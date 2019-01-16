# -*- coding: utf-8 -*-
{
    'name': "payroll_timesheet",

    'summary': """
        Payslip according to employee's timesheet
    """,

    'description': """
        Payslip according to employee's timesheet by Nurlan
    """,

    'author': "ERGPO",
    'website': "http://www.erpgo.az",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'timesheet_grid', 'hr_payroll', 'hr_payroll_account', 'account_accountant'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/payroll_timesheet.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'Application': False,
}
