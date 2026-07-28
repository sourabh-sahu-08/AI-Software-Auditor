import unittest
from calculator import add

class TestCalculator(unittest.TestCase):
    def test_add(self):
        # This will fail because the add function has a bug
        self.assertEqual(add(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
