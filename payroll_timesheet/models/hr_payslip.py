from odoo import models, api, fields, _


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many('account.analytic.line', compute="_get_timesheets")

    @api.one
    def _get_timesheets(self):
        timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True), ('|', '|', ('account_id', '=', 'Vizam'), ('account_id', '=', 'API'))])
        self.timesheet_ids = timesheets

    api_timesheet_hours = fields.Float(string="API total hours", compute="_api_timesheets_sum")

    @api.depends('timesheet_ids')
    def _api_timesheets_sum(self):
        api_timesheets_ids = self.timesheet_ids.search([('account_id', '=', "API")])
        for obj in self:
            sum = 0.0
            for unit in api_timesheets_ids:
                sum += unit.unit_amount
            obj.update({'api_timesheet_hours': sum})

    vizam_timesheet_hours = fields.Float(string="Vizam total hours", compute="_vizam_timesheets_sum")

    @api.depends('timesheet_ids')
    def _vizam_timesheets_sum(self):
        vizam_timesheets_ids = self.timesheet_ids.search([('account_id', '=', "Vizam")])
        for obj in self:
            sum = 0.0
            for unit in vizam_timesheets_ids:
                sum += unit.unit_amount
            obj.update({'vizam_timesheet_hours': sum})

    backpack_timesheet_hours = fields.Float(string="BackPack total hours", compute="_backpack_timesheets_sum")

    @api.depends('timesheet_ids')
    def _backpack_timesheets_sum(self):
        backpack_timesheets_ids = self.timesheet_ids.search([('account_id', '=', "BackPack")])
        for obj in self:
            sum = 0.0
            for unit in backpack_timesheets_ids:
                sum += unit.unit_amount
            obj.update({'backpack_timesheet_hours': sum})
