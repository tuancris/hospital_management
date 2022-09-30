from datetime import date
from odoo import api, fields, models
from odoo.exceptions import ValidationError

import re

class HospitalDoctors(models.Model):
    _name = "hospital.doctors"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _description = "hospital_doctors"
    _rec_name = "name"

    image = fields.Binary(string="Doctors image")

    name = fields.Char(string='Name', required=True, translate=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)

    date_of_birth = fields.Date(string='Date of birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True, store=True)

    desc = fields.Text(string='Description', translate=True, tracking=True)
    # sub = {'AH': "Ahmed", 'JA': 'Jarir'}

    ## functions ##

    ## dependant functions ##

    #@api.onchange('desc')
    #def on_change_name(self):
    #    for i in self.sub.keys():
    #        reg = f'{i}\s'
    #        if bool(re.compile(reg).match(self.name)):
    #            self.name = re.sub(reg, self.sub[i], self.name)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth.year < date.today().year:
                #tempAge = date.today().year - record.date_of_birth.year
                record.age = date.today().year - record.date_of_birth.year
            else:
                record.age = 0
    ## end dependant functions ##

    ## overrides ##
    def copy(self, default={}):
        if not default.get('name'):
            default['name'] = f"{self.name} (COPY)"

        return super(HospitalDoctors, self).copy(default)
    ## end overrides ##
    ## constrains ##

    @api.constrains('name')
    def check_name(self):
        doc = self.env['hospital.doctors']
        for rec in self:
            search = doc.search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if search:
                raise ValidationError(f'the name {rec.name} already exists')

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError('the age cannot be 0')
    ## end constrains ##

    ## end functions ##
