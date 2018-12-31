from odoo import models, api, fields, _


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many('account.analytic.line', compute="_get_timesheets")

    @api.one
    def _get_timesheets(self):
        timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True)])
        self.timesheet_ids = timesheets

    total_project_hours = fields.Float(string="Total project hours", compute="_total_timesheets_sum")

    @api.depends('timesheet_ids')
    def _total_timesheets_sum(self):
        for obj in self:
            sum = 0.0
            for unit in self.timesheet_ids:
                sum += unit.unit_amount
            obj.update({'total_project_hours': sum})
