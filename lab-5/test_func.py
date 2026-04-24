import unittest

from triangle_func import IncorrectTriangleSides, get_triangle_type


class TestTriangleFunction(unittest.TestCase):

    def test_equilateral_triangle(self):
        self.assertEqual(get_triangle_type(5, 5, 5), "equilateral")

    def test_isosceles_triangle(self):
        self.assertEqual(get_triangle_type(5, 5, 3), "isosceles")

    def test_nonequilateral_triangle(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")

    def test_zero_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 4, 5)

    def test_negative_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-3, 4, 5)

    def test_impossible_triangle(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 2, 3)

    def test_string_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type("3", 4, 5)


if __name__ == "__main__":
    unittest.main()