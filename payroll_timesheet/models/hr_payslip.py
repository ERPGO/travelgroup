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

    total_project_hours = fields.Float(string="Total project hours", compute="_total_timesheets_sum")

    @api.depends('timesheet_ids')
    def _total_timesheets_sum( self ):
        for obj in self:
            sum = 0.0
            for unit in self.timesheet_ids:
                sum += unit.unit_amount
            obj.update({'total_project_hours': sum})

    total_num_projects = fields.Integer(string="Total Project numbers", compute="_def_num_projects")

    @api.multi
    def _def_num_projects( self ):
        self.total_num_projects = len(self.timesheet_ids.mapped('project_id'))

    api_project_hours = fields.Float(string="API project hours", compute="_api_timesheet_sum")

    @api.depends('timesheet_ids')
    def _api_timesheet_sum( self ):
        api_timesheet_ids = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True), ('account_id', '=', 'API')])
        for obj in self:
            sum = 0.0
            for unit in api_timesheet_ids:
                sum += unit.unit_amount
            obj.update({'api_project_hours': sum})

    vizam_project_hours = fields.Float(string="Vizam project hours", compute="_vizam_timesheet_sum")

    @api.depends('timesheet_ids')
    def _vizam_timesheet_sum( self ):
        vizam_timesheet_ids = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True), ('account_id', '=', 'Vizam')])
        for obj in self:
            sum = 0.0
            for unit in vizam_timesheet_ids:
                sum += unit.unit_amount
            obj.update({'vizam_project_hours': sum})

    backpack_project_hours = fields.Float(string="BackPack project hours", compute="_backpack_timesheet_sum")

    @api.depends('timesheet_ids')
    def _backpack_timesheet_sum( self ):
        backpack_timesheet_ids = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True), ('account_id', '=', 'BackPack')])
        for obj in self:
            sum = 0.0
            for unit in backpack_timesheet_ids:
                sum += unit.unit_amount
            obj.update({'backpack_project_hours': sum})

    api_percentage = fields.Float(string="API split", compute="_project_percentage")
    vizam_percentage = fields.Float(string="Vizam split", compute="_project_percentage")
    backpack_percentage = fields.Float(string="BackPack split", compute="_project_percentage")

    @api.depends('total_project_hours')
    def _project_percentage( self ):
        if self.total_project_hours > float(0):
            api_split = self.api_project_hours / self.total_project_hours * 100
            self.api_percentage = api_split
            vizam_split = self.vizam_project_hours / self.total_project_hours * 100
            self.vizam_percentage = vizam_split
            backpack_split = self.backpack_project_hours / self.total_project_hours * 100
            self.backpack_percentage = backpack_split



    @api.multi
    def compute_sheet(self):
        for payslip in self:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            # delete old payslip lines
            payslip.line_ids.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or \
                self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
#            lines = [(0, 0, line) for line in self._get_payslip_lines(contract_ids, payslip.id)]
            input_ids = (0, 0, {'name': "API", 'rate': self.api_percentage})

            payslip.write({'line_ids[0]': input_ids, 'number': number})
        return True

