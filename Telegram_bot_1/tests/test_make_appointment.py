import unittest
from handlers.make_appointment import tme
from datetime import time


class TestAppointmentTime(unittest.TestCase):

    def test_appointment_tme(self):
        constant_breaks = [9, time(12), time(13)]
        main_schedule = {3: [[time(9), time(16)]]}
        res = {3: [[time(9), time(12)], [time(13), time(16)]]}
        self.assertEqual(tme(constant_breaks, main_schedule), res)


if __name__ == '__main__':
    unittest.main()
