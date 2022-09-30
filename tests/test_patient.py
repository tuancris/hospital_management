from odoo.tests import common
from odoo.exceptions import ValidationError
import datetime
class TestModelA(common.TransactionCase):
    def test_some_action(self):
        doc = self.env['hospital.doctors'].create({'name': 'doc004', 'date_of_birth': datetime.datetime(1950, 12, 12)})
        record = self.env['hospital.patient'].create({'patient_name': 'fg001', 'ref': doc.id, 'date_of_birth': datetime.datetime(2000,12,12)})

        print('\n\n\n\n\n\n\n\n', record, '\n\n\n\n\n\n\n\n')

        self.assertEqual(
            record.age,
            datetime.date.today().year-datetime.datetime(2000, 12, 12).year)
        self.assertGreaterEqual(record.age, 1)

        record.action_confirm()
        self.assertEqual(
            record.state,
            'confirm')
        record.action_done()
        self.assertEqual(
            record.state,
            'done')
        newRec = record.copy()
        self.assertEqual(
            newRec.patient_name,
            f"{record.patient_name} (COPY)")
        ## check if name constraint is not working
        with self.assertRaises(ValidationError):
            self.env['hospital.patient'].create({'patient_name': 'fg002', 'ref': doc.id, 'date_of_birth': datetime.datetime(2022,12,12)})
        ## check if age constraint is not working
        with self.assertRaises(ValidationError):
            record.setDOB(datetime.datetime.today())
        ## check for unlink error
        with self.assertRaises(ValidationError):
            record.unlink()


        record.action_cancel()