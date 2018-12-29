from odoo import models, api, fields


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many('account.analytic.line', compute="_get_timesheets")

    @api.one
    def _get_timesheets( self ):
        timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True)])
        self.timesheet_ids = timesheets

    account_ids = fields.One2many('account.analytic.line', string="Sum of Timesheet hours",
                                  description="Sum of Timesheet hours",
                                  compute="_sum_account_ids")

    @api.one
    def _sum_account_ids( self ):
        all_account_recordset = self.env["account.analytic.line"].search([('account_id', '!=', None)])
        self.account_ids = all_account_recordset.mapped('account_id')

    sum_timesheet_ids = fields.One2many('account.analytic.line', compute="_total_timesheets")

    @api.multi
    def _total_timesheets( self ):
        if acc in ('API', 'Vizam'):
            all_timesheets = self.env["account.analytic.line"].search([('account_id.name', '=', acc)])
        return all_timesheets
        self.sum_timesheet_ids = all_timesheets

