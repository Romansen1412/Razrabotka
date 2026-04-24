class IncorrectTriangleSides(Exception):
    """Исключение для некорректных сторон треугольника."""


def get_triangle_type(a, b, c):
    """Возвращает тип треугольника по длинам его сторон."""
    sides = (a, b, c)

    if not all(isinstance(side, (int, float)) for side in sides):
        raise IncorrectTriangleSides("Стороны должны быть числами")

    if not all(side > 0 for side in sides):
        raise IncorrectTriangleSides("Стороны должны быть положительными")

    if a + b <= c or a + c <= b or b + c <= a:
        raise IncorrectTriangleSides("Треугольник с такими сторонами невозможен")

    if a == b == c:
        return "equilateral"

    if a == b or a == c or b == c:
        return "isosceles"

    return "nonequilateral"