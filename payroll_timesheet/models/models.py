from odoo import models, api, fields


class hr_payroll(models.Model):
    _inherit = 'account.analytic.line'

    payslip = fields.Many2one('hr.payslip', string="Payslip", ondelete='cascade')


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many(compute="_compute_o2m_field", 'Timesheets')



@api.one
def _compute_o2m_field(self):
    ### get recordset of related object, for example with search (or whatever you like):
    related_recordset = self.env["the.relation.obj"].search([("some", "condition","here")])
    self.o2m_field = related_recordset
