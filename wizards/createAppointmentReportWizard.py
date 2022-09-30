from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CreateAppointmentReportWizard(models.TransientModel):
    _name = "create.appointment.report.wizard"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _description = "hospital_appointment_report"

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')

    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentReportWizard, self).default_get(fields)
        act_id = self._context.get('active_id')
        if act_id:
            res['patient_id'] = act_id
        return res
    def make_appointment_report(self):
        domain = [('patient_id', '=', self.patient_id.id)]
        if self.date_from:
            domain.append(("appointment_time", '>=', self.date_from))
        if self.date_to:
            domain.append(("appointment_time", '<=', self.date_to))
        appointments = self.env['hospital.appointment'].search_read(domain)
        vals = {
            'form': self.read()[0],
            'appointments': appointments,
        }
        return self.env.ref('om_hospital.action_report_appointment').report_action(self, data=vals)
        # self.env['hospital.appointment'].create(vals)
    # def view_appointments(self):
    #     action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
    #     action['domain'] = [('patient_id', '=', self.patient_id.id)]
    #     return action
    @api.constrains('date_from')
    def check_date_from_and_date_to(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise ValidationError('\'date from\' cannot be after \'date to\'')