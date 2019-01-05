# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


class Experience(models.Model):
    _inherit = 'hr.employee'

    is_bonus_eligible = fields.Boolean(string="Eligible for Bonus")
    startdate = fields.Date(string='Start Date')

    experience = fields.Integer(string="Experience(years)", stored=True)

    @api.onchange('startdate')
    def _set_experience( self ):
        """Updates experience field when Start date is changed"""

        if self.startdate:
            d1 = datetime.strptime(str(self.startdate), "%Y-%m-%d").date()
            d2 = date.today()
            self.experience = relativedelta(d2, d1).years


class PayrollBonus(models.Model):
    _name = 'bonus_calculation'
    _description = 'Bonus Calculation'
    name = fields.Char(string="Bonus")
    bonus_amount = fields.Float(string="Bonus Amount")
    bonus_date = fields.Date(string="Bonus Date")


class Evaluation(models.Model):
    _name = 'employee_evaluation'
    _description = 'Employees evaluation for bonus calculation'

    name = fields.Char(string="Employee Evaluation", required=True)
    bonus = fields.Many2one('bonus_calculation', string="Bonus")
    bonus_amount = fields.Float(related="bonus.bonus_amount", string="Bonus Amount", readonly=True)
    evaluation_lines = fields.One2many('employee_evaluation.line', 'evaluation_id', string="Employees Evaluation")
    total_kpi = fields.Float(string="Total KPI", compute="_get_total_kpi")

    @api.depends('evaluation_lines')
    def _get_total_kpi( self ):
        for obj in self:
            sum = 0.0
            for unit in self.evaluation_lines:
                sum += unit.kpi_score
                obj.update({'total_kpi': sum})

    total_experience = fields.Integer(string="Total Experience", compute="_get_total_experience")

    @api.depends('evaluation_lines')
    def _get_total_experience( self ):
        for obj in self:
            sum = 0.0
            for unit in self.evaluation_lines:
                sum += unit.experience
                obj.update({'total_experience': sum})


class EvaluationLine(models.Model):
    _name = 'employee_evaluation.line'
    _description = 'Evaluation Lines'

    evaluation_id = fields.Many2one('employee_evaluation', string="Evaluation")
    employee_id = fields.Many2one('hr.employee', domain="[('is_bonus_eligible', '=', True)]")
    organization_skill = fields.Selection([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"]])
    operational_excellence = fields.Selection([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"]])
    kpi_score = fields.Float(string="KPI Score", readonly=True, stored=True, compute='_get_avarage')
    experience = fields.Integer(related='employee_id.experience', string="Experience(years)", readonly=True)

    @api.onchange('organization_skill', 'operational_excellence')
    def _get_avarage( self ):
        for record in self:
            if record.organization_skill and record.operational_excellence:
                record['kpi_score'] = (int(record['organization_skill']) + int(record['operational_excellence'])) / 2


class HRPayslipEval(models.Model):
    _inherit = 'hr.payslip'

    evaluation_id = fields.Many2one('employee_evaluation', string="Evaluation")
    evaluation_lines = fields.One2many(related='evaluation_id.evaluation_lines', string="Employee Evaluations",
                                       compute="_get_employees_evaluations")
    bonus_amount = fields.Float(string="Bonus Amount", related='evaluation_id.bonus_amount')
    total_kpi = fields.Float(string="Total KPI score", related='evaluation_id.total_kpi')
    total_experience = fields.Integer(related='evaluation_id.total_experience', string="Total Experience")

    @api.multi
    @api.depends('evaluation_id')
    def _get_employees_evaluations( self ):
        lines = self.env["employee_evaluation.line"].search([])
        self.evaluation_lines = lines