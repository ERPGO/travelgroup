# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from datetime import date


class Experience(models.Model):
    _inherit = 'hr.employee'

    startdate = fields.Date(string='Start Date')

    experience = fields.Integer(string="Experience")

    @api.onchange('startdate')
    def _set_experience( self ):
        """Updates age field when birth_date is changed"""

        if self.startdate:
            d1 = datetime.strptime(self.startdate, "%Y-%m-%d").date()

            d2 = date.today()

            self.experience = relativedelta(d2, d1).years
