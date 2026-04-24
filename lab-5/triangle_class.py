class IncorrectTriangleSides(Exception):
    """Исключение для некорректных сторон треугольника."""


class Triangle:
    def __init__(self, a, b, c):
        """Инициализация треугольника."""
        self.a = a
        self.b = b
        self.c = c

        if not self._is_valid():
            raise IncorrectTriangleSides("Некорректные стороны треугольника")

    def _is_valid(self):
        """Проверяет корректность сторон треугольника."""
        sides = (self.a, self.b, self.c)

        if not all(isinstance(side, (int, float)) for side in sides):
            return False

        if not all(side > 0 for side in sides):
            return False

        return (
            self.a + self.b > self.c
            and self.a + self.c > self.b
            and self.b + self.c > self.a
        )

    def triangle_type(self):
        """Возвращает тип треугольника."""
        if self.a == self.b == self.c:
            return "equilateral"

        if self.a == self.b or self.a == self.c or self.b == self.c:
            return "isosceles"

        return "nonequilateral"

    def perimeter(self):
        """Возвращает периметр треугольника."""
        return self.a + self.b + self.c