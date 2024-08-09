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

    def test_many(self):
        main = [[time(9), time(15)], [time(16), time(20)]]
        changes = [time(13), time(14)]
        res = [[time(9), time(13)], [time(14), time(15)], [time(16), time(20)]]
        self.assertEqual(merge_time(main, changes, 0), res)

    def test_many2(self):
        main = [[time(9), time(15)], [time(16), time(20)]]
        changes = [time(15), time(16)]
        res = [[time(9), time(15)], [time(16), time(20)]]
        self.assertEqual(merge_time(main, changes), res)

    def test_many3(self):
        main = [[time(9), time(15)], [time(16), time(20)]]
        changes = [time(8), time(24)]
        res = []
        self.assertEqual(merge_time(main, changes), res)

    def test_many4(self):
        main = [[time(9), time(15)], [time(16), time(20)]]
        changes = [time(8), time(17)]
        res = [[time(17), time(20)]]
        self.assertEqual(merge_time(main, changes), res)

    def test_empty(self):
        main = []
        changes = [time(8), time(17)]
        res = []
        self.assertEqual(merge_time(main, changes), res)

    def test_empty2(self):
        main = [[time(9), time(15)], [time(16), time(20)]]
        changes = []
        res = [[time(9), time(15)], [time(16), time(20)]]
        self.assertEqual(merge_time(main, changes), res)

    def test_working(self):
        main = [[time(9), time(15)], [time(16), time(20)]]
        changes = [time(15), time(16)]
        res = [[time(9), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)


if __name__ == '__main__':
    unittest.main()
