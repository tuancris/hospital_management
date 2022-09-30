from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _description = "hospital_appointment"

    appointment_time = fields.Datetime(string='time', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor = fields.Many2one("hospital.doctors", string="doctor", required=True)

    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentWizard, self).default_get(fields)
        act_id = self._context.get('active_id')
        if act_id:
            res['patient_id'] = act_id
        return res
    def make_an_appointment(self):
        vals = {
            "patient_id": self.patient_id.id,
            "appointment_time": self.appointment_time,
            "doctor": self.doctor.id
        }
        return self.env['hospital.appointment'].create(vals)
    def view_appointments(self):
        action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    @api.constrains('appointment_time')
    def check_appointment_time(self):
        for rec in self:
            if rec.appointment_time.date() < date.today():
                raise ValidationError('appointment time cannot be before today\'s date')