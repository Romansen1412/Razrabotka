import pytest

from triangle_class import IncorrectTriangleSides, Triangle


def test_create_equilateral_triangle():
    triangle = Triangle(5, 5, 5)
    assert triangle.triangle_type() == "equilateral"
    assert triangle.perimeter() == 15


def test_create_isosceles_triangle():
    triangle = Triangle(5, 5, 3)
    assert triangle.triangle_type() == "isosceles"
    assert triangle.perimeter() == 13


def test_create_nonequilateral_triangle():
    triangle = Triangle(3, 4, 5)
    assert triangle.triangle_type() == "nonequilateral"
    assert triangle.perimeter() == 12


def test_zero_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 4, 5)


def test_negative_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-3, 4, 5)


def test_impossible_triangle():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 2, 3)


def test_string_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle("3", 4, 5)