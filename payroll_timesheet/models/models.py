from odoo import models, api, fields


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many('account.analytic.line', 'payslip', 'Timesheets')

class hr_payroll(models.Model):
    _inherit = 'account.analytic.line'

    payslip = fields.Many2one('hr.payslip', string="Payslip", ondelete='cascade')
    