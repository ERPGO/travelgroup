from odoo import models, api, fields


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many('account.analytic.line', compute="_get_timesheets")

    @api.one
    def _get_timesheets(self):
        timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True)])
        self.timesheet_ids = timesheets

    account_ids = fields.One2Many('account.analytic.account', compute="_sum_timesheets")
    @api.one
    def _sum_timesheets(self):
        all_account_ids = self.env["account.analytic.account"].search([])
        self.account_ids = all_account_ids

#    employee_ids = fields.One2many('hr.employee', compute="_get_employees")

#    @api.one
#    def _get_employees(self):
#        employee_recordset = self.env["hr.employee"].search([('name', '=', self.employee_id.name)])
#        self.employee_ids = employee_recordset
