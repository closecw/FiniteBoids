import math

class Vec:
    """
    Class for representing 2D vectors.
    """
    def __init__(self, x, y):
        """
        Constructor for a 2D vector.
        :param x: X (horizontal) component of the vector.
        :param y: Y (vertical) component of the vector.
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __truediv__(self, value):
        if value != 0:
            return Vec(self.x / value, self.y / value)
        else:
            return Vec(0, 0)

    def __mul__(self, value):
        return Vec(self.x * value, self.y * value)

    __rmul__ = __mul__      # Scalar * Vector logic

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            self.x /= mag
            self.y /= mag
        return self

    def limit(self, limit):
        mag = self.magnitude()
        if mag > limit:
            self.x *= limit / mag
            self.y *= limit / mag
        return self

    def bottom_limit(self, limit):
        mag = self.magnitude()
        if mag < limit and mag != 0:
            self.x *= (limit / mag)
            self.y *= (limit / mag)
        return self

    def linear_interpolate(self, other, t):
        return Vec(self.x * (1 - t) + other.x * t, self.y * (1 - t) + other.y * t)

    @staticmethod
    def distance(v1, v2):
        return math.hypot(v1.x - v2.x, v1.y - v2.y)

    @staticmethod
    def angleBetween(v1, v2):
        mag1 = v1.magnitude()
        mag2 = v2.magnitude()
        if mag1 == 0 or mag2 == 0:
            return math.pi
        dot = v1.dot(v2) / (mag1 * mag2)
        dot = max(min(dot, 1), -1)
        return math.acos(dot)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)