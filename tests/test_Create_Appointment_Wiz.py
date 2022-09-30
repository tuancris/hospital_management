from odoo.tests import common
from odoo.exceptions import ValidationError
import datetime
class TestModelB(common.TransactionCase):
    doc = ''
    record = ''

    def test_some_action(self):
        red = '\033[91m'
        green = '\033[92m'
        normal = '\033[92m'
        doc = self.env['hospital.doctors'].create({'name': 'doc003', 'date_of_birth': datetime.datetime(1950, 12, 12)})
        record = self.env['hospital.patient'].create({'patient_name': 'fg003', 'ref': doc.id, 'date_of_birth': datetime.datetime(2000, 12, 12)})

        print('   ================== normal creation test ==================')
        appointment = self.env['create.appointment.wizard'].create({'patient_id': record.id, 'doctor': doc.id, 'appointment_time': datetime.datetime(datetime.datetime.today().year+1, 12, 12)})
        print(f'{green}================== normal creation test finished ==================')

        print('   ================== date constraint test ==================')
        with self.assertRaises(ValidationError):
            self.env['create.appointment.wizard'].create({'patient_id': record.id, 'doctor': doc.id, 'appointment_time': datetime.datetime(2050, 12, 12)})
            print(f'{red}================== date constraint test failed ==================')
        print(f'{green}================== date constraint test finished ==================')

        print('   ================== making an appointment test ==================')
        appointment.make_an_appointment()
        print(f'{green}================== making an appointment test finished ==================')

        print('   ================== view appointments test ==================')
        appointment.view_appointments()
        print(f'{green}================== view appointments test finished ==================')
