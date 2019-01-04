# -*- coding: utf-8 -*-
{
    'name': "payroll_timesheet_bonus",

    'summary': """
        Bonus calculation addon to payroll_timesheet module
    """,

    'description': """
        Bonus calculation addon to payroll_timesheet module
    """,

    'author': "ERGPO",
    'website': "http://www.erpgo.az",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'payroll_timesheet'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/bonus_calculation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'Application': False,
}
