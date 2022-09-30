from odoo import api, fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _description = "hospital_appointment"
    _order = "appointment_time asc"
    _rec_name = "patient_id"

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor = fields.Many2one("hospital.doctors", string="doctor", required=True)


    gender = fields.Selection(related='patient_id.gender')
    age = fields.Integer(related='patient_id.age')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)

    prescription = fields.Text(string="prescription")
    description = fields.Text(string="description")
    prescription_line_ids = fields.One2many('appointment.prescription.line', 'appointment_id', string='Prescription Lines')

class appointmentPrescriptionLine(models.Model):
    _name = "appointment.prescription.line"
    _description = "Appointment Prescription Line"

    medicine = fields.Char(string="Medicine", required=True)

    qty = fields.Char(string="Quantity", default=1, required=True)

    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")