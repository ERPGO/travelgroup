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
    def _set_experience(self):
        """Updates experience field when Start date is changed"""

        if self.startdate:
            d1 = datetime.strptime(str(self.startdate), "%Y-%m-%d").date()
            d2 = date.today()
            self.experience = relativedelta(d2, d1).years


class PayrollBonus(models.Model):
    _name = 'payroll_timesheet.bonus'
    _description = 'Bonus for Timesheet app'
    name = fields.Char(string="Bonus")
    bonus_amount = fields.Float(string="Bonus Amount")
    bonus_date = fields.Date(string="Bonus Date")


class BonusLine(models.Model):
    _inherit = 'hr.payslip'

    bonus = fields.Many2one('payroll_timesheet.bonus', string="Bonus")
    bonus_amount = fields.Float(related="bonus.bonus_amount", string="Bonus Amount")

    organization_skill = fields.Selection([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"]])
    operational_excellence = fields.Selection([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"]])
    kpi_score = fields.Float(string="KPI Score", readonly=True, stored=True, compute='_get_avarage')
    experience = fields.Integer(related='employee_id.experience', string="Experience(years)", readonly=True)

    @api.onchange('organization_skill', 'operational_excellence')
    def _get_avarage(self):
        for record in self:
            if record.organization_skill and record.operational_excellence:
                record['kpi_score'] = (int(record['organization_skill']) + int(record['operational_excellence'])) / 2
