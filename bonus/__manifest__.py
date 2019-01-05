# -*- coding: utf-8 -*-
{
    'name': "bonus_calculation",

    'summary': """
        Bonus calculation module
    """,

    'description': """
        Bonus calculation module enables to calculate bonuses through evaluation metrics
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
