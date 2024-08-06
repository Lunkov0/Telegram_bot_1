import unittest
from datetime import time
from handlers.make_appointment import merge_time


class TestMergeTime(unittest.TestCase):
    def test_inside(self):
        main = [[time(9), time(18)]]
        changes = [time(13), time(14)]
        res = [[time(9), time(13)], [time(14), time(18)]]
        self.assertEqual(merge_time(main, changes), res)

    def test_outside(self):
        main = [[time(13), time(14)]]
        changes = [time(9), time(18)]
        res = []
        self.assertEqual(merge_time(main, changes), res)


if __name__ == '__main__':
    unittest.main()
