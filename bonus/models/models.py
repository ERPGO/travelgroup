# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


class Experience(models.Model):
    _inherit = 'hr.employee'

    startdate = fields.Date(string='Start Date')

    experience = fields.Integer(string="Experience(years)")

    @api.onchange('startdate')
    def _set_experience( self ):
        """Updates experience field when Start date is changed"""

        if self.startdate:
            d1 = datetime.strptime(str(self.startdate), "%Y-%m-%d").date()
            d2 = date.today()
            self.experience = relativedelta(d2, d1).years


class Evaluation(models.Model):
    _name = 'payroll_timesheet.bonus'
    _description = 'Bonus for Timesheet app'
    organization_skill = fields.Selection([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"]])
    operational_excellence = fields.Selection([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"]])
    kpi_score = fields.Float(string="KPI Score", readonly=True, stored=True, compute='_get_avarage')

    employee_id = fields.Many2one('hr.employee', string="Employee")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip")
    experience = fields.Float(related='employee_id.experience', string="Experience(years)", readonly=True)



    @api.multi
    @api.onchange('organization_skill', 'operational_excellence')
    def _get_avarage(self):
        for record in self:
            if record.organization_skill and record.operational_excellence:
                record['avarage_rate'] = (int(record['organization_skill']) + int(record['operational_excellence'])) / 2
