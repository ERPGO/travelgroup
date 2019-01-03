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
        lines = [(0, 0, line) for line in self._get_payslip_lines(contract_ids, payslip.id)]
        payslip.write({'line_ids': lines, 'number': number})

        for line in self.line_ids:
            if line.name == 'API':
                line.write({'rate': self.api_percentage})
            if line.name == 'BackPack':
                line.write({'rate': self.backpack_percentage})
            if line.name == 'Vizam':
                line.write({'rate': self.vizam_percentage})
        return True
