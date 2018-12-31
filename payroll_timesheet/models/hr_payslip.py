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

    api_timesheet_hours = fields.One2many('account.analytic.line', string="API total hours",
                                          compute="_timesheets_hours_sum")
    vizam_timesheet_hours = fields.One2many('account.analytic.line', string="VIZAM total hours",
                                            compute="_timesheets_hours_sum")
    backpack_timesheet_hours = fields.One2many('account.analytic.line', string="BackPack total hours",
                                               compute="_timesheets_hours_sum")

    @api.depends('timesheet_ids.unit_amount')
    def _timesheets_hours_sum(self):
        api_timesheets_ids = self.timesheet_ids.search([('account_id', '=', "API")])
        vizam_timesheets_ids = self.timesheet_ids.search([('account_id', '=', "Vizam")])
        backpack_timesheets_ids = self.timesheet_ids.search([('account_id', '=', "BackPack")])
        for obj in self:
            sum = 0.0
            for unit in api_timesheets_ids:
                sum += unit.unit_amount
                obj.update({'api_timesheet_hours': sum})