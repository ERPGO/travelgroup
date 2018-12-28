from odoo import models, api, fields


class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    for_payslip = fields.Boolean(string="For payslip?")

    percentage_split = fields.Integer(string="Multiplier")

    @api.multi
    def _check_qty(self):
        min = 0
        max = 100
        if not min < self.percentage_split < max:
            return False
        return True

        _constraints = [(_check_qty, 'Please inter other qty !', ['qty'])]
