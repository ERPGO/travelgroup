from odoo import models, api, fields, _


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many('account.analytic.line', compute="_get_timesheets")

    @api.one
    def _get_timesheets( self ):
        timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True)])
        self.timesheet_ids = timesheets

    api_timesheet_hours = fields.One2many('account.analytic.line', compute="_api_timesheets")

    @api.multi
    def _api_timesheets( self ):
        all_timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True)])
        api_timesheets = all_timesheets.search([('account_id', '=', "API")])
        self.api_timesheet_hours = api_timesheets

    api_total_hours = fields.Float(string="total hours", compute="_sum_all")

    @api.multi
    def _sum_all( self, cr, uid, ids, unit_amount, arg, context=None ):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            sum = 0
            for c in obj.timesheet_ids:
                sum += c.unit_amount
            res[obj.id] = {'sum_all': sum}
        return res
