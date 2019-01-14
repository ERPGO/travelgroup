from odoo import models, api, fields, _


class hr_payslip_projects(models.Model):
    _name = 'hr.payslip.projects'
    _description = 'to see total hours per project on hr.payslip module'

    name = fields.Char(string="Description")
    project_id = fields.Many2one('project.project')
    project_hours = fields.Float(string="Total hours")
    overtime_hours = fields.Float(string="Overtime hours")
    project_split = fields.Float(string="Project split")
    slip_id = fields.Many2one('hr.payslip')


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    timesheet_ids = fields.One2many('account.analytic.line', compute="_get_timesheets")

    @api.one
    def _get_timesheets(self):
        timesheets = self.env["account.analytic.line"].search(
            [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
             ('validated', '=', True)])
        self.timesheet_ids = timesheets

    total_project_hours = fields.Float(string="Total project hours", compute="_total_timesheets_sum")

    @api.depends('timesheet_ids')
    def _total_timesheets_sum(self):
        for obj in self:
            sum = 0.0
            for unit in self.timesheet_ids:
                sum += unit.unit_amount
            obj.update({'total_project_hours': sum})

    total_num_projects = fields.Integer(string="Total Project numbers", compute="_def_num_projects")

    @api.multi
    def _def_num_projects(self):
        self.total_num_projects = len(self.timesheet_ids.mapped('project_id'))

    all_project_hours = fields.One2many('hr.payslip.projects', 'slip_id', "Project Hours")

    @api.onchange('employee_id')
    def _calculate_project_hours(self):
        all_project_hours = []
        value = {}
        projects = self.env['project.project'].search([])
        for project in projects:
            domain = [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from),
                      ('date', '<=', self.date_to),
                      ('validated', '=', True), ('is_bonus_eligible', '=', True), ('project_id', '=', project.name)]
            domain_ot = [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to),
                         ('validated', '=', True), ('is_bonus_eligible', '=', True), ('project_id', '=', project.name),
                         ('task_id', '=', 'Overtime')]
            all_timesheets = self.env["account.analytic.line"].search(domain)
            ot_timesheets = self.env["account.analytic.line"].search(domain_ot)
            sum_all = 0.0
            sum_ot = 0.0
            split = 0.0
            for unit in all_timesheets:
                sum_all += unit.unit_amount
            for ot in ot_timesheets:
                sum_ot += ot.unit_amount
            if self.total_project_hours > float(0):
                split = sum_all / self.total_project_hours * 100
            all_project_hours.append(
                (0, 0, {'project_id': project.id, 'project_hours': sum_all, 'overtime_hours': sum_ot, 'project_split': split}))
        value.update(all_project_hours=all_project_hours)
        return {'value': value}
    
    @api.multi
    def _get_project_split(self, project):
        for line in self.all_project_hours:
            if line.project_id.name == project:
                project_split = line.project_split
        return project_split
    
    @api.multi
    def _get_sample_split(self):
        return 1200

    api_project_hours = fields.Float(string="API project hours", compute="_api_timesheet_sum")

    @api.depends('timesheet_ids')
    def _api_timesheet_sum(self):
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
    def _vizam_timesheet_sum(self):
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
    def _backpack_timesheet_sum(self):
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
    def _project_percentage(self):
        if self.total_project_hours > float(0):
            api_split = self.api_project_hours / self.total_project_hours * 100
            self.api_percentage = api_split
            vizam_split = self.vizam_project_hours / self.total_project_hours * 100
            self.vizam_percentage = vizam_split
            backpack_split = self.backpack_project_hours / self.total_project_hours * 100
            self.backpack_percentage = backpack_split

    ot_hours = fields.Float(string="OT hours", compute="_get_ot_hours")

    @api.multi
    def _get_ot_hours(self):
        for obj in self:
            domain = [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from),
                      ('date', '<=', self.date_to),
                      ('validated', '=', True), ('task_id', '=', 'Overtime')]
            ot_timesheets_ids = self.env["account.analytic.line"].search(domain)
            sum = 0.0
            for unit in ot_timesheets_ids:
                sum += unit.unit_amount
            obj.update({'ot_hours': sum})

    total_ot_hours = fields.Float(string="Total OT hours", compute="_get_total_ot_hours")

    @api.multi
    def _get_total_ot_hours(self):
        for obj in self:
            domain = [('date', '>=', self.date_from),
                      ('date', '<=', self.date_to),
                      ('validated', '=', True), ('task_id', '=', 'Overtime'), ('is_bonus_eligible', '=', True)]
            ot_timesheets_ids = self.env["account.analytic.line"].search(domain)
            sum = 0.0
            for unit in ot_timesheets_ids:
                sum += unit.unit_amount
            obj.update({'total_ot_hours': sum})
