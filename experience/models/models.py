# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


class Experience(models.Model):
    _inherit = 'hr.employee'

    startdate = fields.Date(string='Start Date')

    experience = fields.Integer(string="Experience")

    @api.onchange('startdate')
    def _set_experience( self ):
        """Updates experience field when Start date is changed"""

        if self.startdate:
            d1 = datetime.strptime(str(self.startdate), "%Y-%m-%d").date()
            d2 = date.today()
            self.experience = relativedelta(d2, d1).years


class Evaluation(models.Model):
    _inherit = 'hr.payslip'

    organization_skill = fields.Selection([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"]])
    operational_excellence = fields.Selection([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"]])
    avarage_rate = fields.Float(string="Avarage rate", readonly=True, compute='_get_avarage')

    @api.multi
    def _get_avarage(self):
        for record in self:
            record.average_rate = int(record.organization_skill) + int(record.operational_excellence) / 2
