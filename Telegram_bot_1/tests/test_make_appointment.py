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
        changes = [time(8), time(23)]
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
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(15), time(16)]
        res = [[time(9), time(14)], [time(15), time(16)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working2(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(6), time(7)]
        res = [[time(6), time(7)], [time(9), time(14)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working3(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(6), time(10)]
        res = [[time(6), time(14)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working4(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(6), time(9)]
        res = [[time(6), time(14)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working5(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(6), time(14)]
        res = [[time(6), time(14)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working6(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(6), time(15)]
        res = [[time(6), time(15)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working7(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(6), time(17)]
        res = [[time(6), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working8(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(6), time(21)]
        res = [[time(6), time(21)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working9(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(10), time(11)]
        res = [[time(9), time(14)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working10(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(10), time(14)]
        res = [[time(9), time(14)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working11(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(10), time(15)]
        res = [[time(9), time(15)], [time(17), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)

    def test_working12(self):
        main = [[time(9), time(14)], [time(17), time(20)]]
        changes = [time(10), time(17)]
        res = [[time(9), time(20)]]
        self.assertEqual(merge_time(main, changes, 1), res)


if __name__ == '__main__':
    unittest.main()
