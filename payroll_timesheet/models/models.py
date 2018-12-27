from odoo import models, api, fields


class hr_payroll(models.Model):
    _inherit = 'account.analytic.line'

    payslip = fields.Many2one('hr.payslip', string="Payslip", ondelete='cascade')


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

<<<<<<< HEAD
    timesheet_ids = fields.One2many(compute="_compute_o2m_field", 'Timesheets')



@api.one
def _compute_o2m_field(self):
    ### get recordset of related object, for example with search (or whatever you like):
    related_recordset = self.env["the.relation.obj"].search([("some", "condition","here")])
    self.o2m_field = related_recordset
=======
    timesheet_ids = fields.One2many('account.analytic.line', compute="_get_timesheets")

    @api.one
    def _get_timesheets(self):
        timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
        self.timesheet_ids = timesheets

#    employee_ids = fields.One2many('hr.employee', compute="_get_employees")

#    @api.one
#    def _get_employees(self):
#        employee_recordset = self.env["hr.employee"].search([('name', '=', self.employee_id.name)])
#        self.employee_ids = employee_recordset
>>>>>>> e52689cd13e046ff0bd994133451effd6a4aa538
