from odoo import models, api, fields


class hr_employee(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many('account.analytic.line', 'employee_id', 'Timesheets', domain="[('employee_id', '=', employee_id)]")


