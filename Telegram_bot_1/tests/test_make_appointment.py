import unittest
from datetime import time


class TestAppointmentTime(unittest.TestCase):

    def test_appointment_tme(self):
        constant_breaks = [time(12), time(13)]
        main_schedule = {3: [[time(9), time(16)]]}
        res = {3: [[time(9), time(12)], [time(13), time(16)]]}
        self.assertEqual(merge_main_and_schedule_break(main_schedule, constant_breaks), res)


if __name__ == '__main__':
    unittest.main()
