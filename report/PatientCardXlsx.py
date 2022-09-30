
from odoo import models
class PatientCardXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('PatientIdCards')
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})

        sheet.set_column('A:B', 13)

        col = 0
        row = 0

        for obj in partners:
            sheet.merge_range(row, col, row, col + 1, 'ID Card')
            sheet.write(row, col, 'ID Card', format_1)

            row += 1

            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col+1, obj.name)

            row += 1

            sheet.write(row, col, 'Age', bold)
            sheet.write(row, col + 1, obj.age)

            row += 1

            sheet.write(row, col, 'Reference', bold)
            if obj.ref:
                sheet.write(row, col + 1, obj.ref.name)

            row += 2
