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
            d1 = datetime.strptime(str(self.startdate), "%Y-%m-%d %H:%M:%S.%f").date()
            d2 = date.today()
            self.experience = relativedelta(d2, d1).years
