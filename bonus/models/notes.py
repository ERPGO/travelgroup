@api.onchange('employee_id')
def _calculate_project_hours(self):
    project_hours = []
    value = {}
    projects = self.env['project.project'].search([])
    for project in projects:
        domain = [('employee_id', '=', self.employee_id.name), ('date', '>=', self.date_from),
                  ('date', '<=', self.date_to),
                  ('validated', '=', True), ('project_id', '=', project.name)]
        timesheets = self.env["account.analytic.line"].search(domain)
        sum = 0.0
        for unit in timesheets:
            sum += unit.unit_amount
        project_hours.append((0, 0, {'project_id': project.id, 'total_project_hours': sum}))
    value.update(project_hours=project_hours)
    return {'value': value}

@api.multi
def _get_project_split(project):
