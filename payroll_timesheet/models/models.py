from odoo import models, api, fields


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    test_field = fields.Char(string="Test field")
    timesheet_ids = fields.One2many('account.analytic.line', compute="_get_timesheets")
    account_ids = fields.One2many('account.analytic.line', string="Analytic Account", description="Analytic Accounts",
                                  compute="_sum_timesheets")

    @api.one
    def _get_timesheets(self):
        timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True)])
        self.timesheet_ids = timesheets

    @api.one
    def _sum_timesheets(self):
        all_account_recordset = self.env["account.analytic.line"].search([('account_id', '!=', None)])
        self.account_ids = all_account_recordset