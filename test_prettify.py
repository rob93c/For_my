import unittest
from For_my import Tools


class TestPrettify(unittest.TestCase):
    # Test prettify
    def test_prettify_long(self):
        num = 14.020021142151241
        res = Tools.prettify(num)
        self.assertEqual(res, "14.02")

    def test_prettify_short(self):
        num = 1
        res = Tools.prettify(num)
        self.assertEqual(res, "1.00")


if __name__ == '__main__':
    unittest.main()
