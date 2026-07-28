import unittest
from math_ops import subtract

class TestMathOps(unittest.TestCase):
    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)

if __name__ == '__main__':
    unittest.main()
