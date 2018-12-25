# -*- coding: utf-8 -*-
{
    'name': "employee_experience",

    'summary': """
        Adds Employee's start date and shows its experience in years in experience""",

    'description': """
        Adds Employee's start date and shows its experience in years in experience
    """,

    'author': "ERGPO",
    'website': "http://www.erpgo.az",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/crm2invoice.xml',
        #'views/automation.xml',
        'views/avarage_rate.xml',
        'views/experience.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'Application': False,
}
