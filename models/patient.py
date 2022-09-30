from datetime import date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "hospital_patient"

    image = fields.Binary(string="Patient image")

    patient_name = fields.Char(string='Name', required=True, translate=True, tracking=True)
    ref = fields.Many2one("hospital.doctors", string="reference", required=True)
    date_of_birth = fields.Date(string='Date of birth')

    age = fields.Integer(string='Age', compute='_compute_age', tracking=True, store=True)
    gender = fields.Selection([('male','Male'), ('female','Female')],string= 'Gender', tracking=True)
    active = fields.Boolean(string='active', default=True)

    state = fields.Selection([('draft', 'draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancel')],
                             default='draft', string='Status', tracking=True)

    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")

    ## functions ##

    ## state functions ##
    def action_confirm(self):
        # if self.state == "draft":
        self.state = 'confirm'
        # else:
        #     raise ValidationError(f"{self.patient_name} is not in draft state")
    def action_done(self):
        # if self.state == "confirm":
        self.state = 'done'
        # else:
            # raise ValidationError(f"{self.patient_name} is not in confirmed state")

    def action_draft(self):
        # if self.state == "cancel":
        self.state = 'draft'
        # else:
        #     raise ValidationError(f"{self.patient_name} is not in confirmed state")

    def action_cancel(self):
        self.state = 'cancel'
    ## end of state functions ##

    ## action functions ##
    ## end action functions ##
    def setDOB(self,date):
        self.date_of_birth = date
        print(self.age)

    ## dependant functions ##
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth.year < date.today().year:
                record.age = date.today().year - record.date_of_birth.year
            else:
                record.age = 0
    ## end dependant functions ##

    ## get functions ##
    def name_get(self):
        res = []
        for rec in self:
            name = "[" + str(rec.id) + "] " + rec.patient_name
            res.append((rec.id, name))
        return res
    ## end get functions ##

    ## overrides ##
    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(f"you cannot delete use {rec.patient_name} as it is in Done state")
            for appointment in rec.appointment_ids:
                appointment.unlink()
            super(HospitalPatient, rec).unlink()

    def copy(self, default={}):
        if not default.get('patient_name'):
            default['patient_name'] = f"{self.patient_name} (COPY)"
        return super(HospitalPatient, self).copy(default)
    ## end overrides ##

    ## constrains ##

    @api.constrains('patient_name')
    def check_name(self):
        patient = self.env['hospital.patient']
        for rec in self:
            search = patient.search([('patient_name', '=', rec.patient_name), ('id', '!=', rec.id)])
            if search:
                raise ValidationError(f'the name {rec.patient_name} already exists')

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError('age cannot be 0')
    ## end constrains ##

    ## end functions ##
