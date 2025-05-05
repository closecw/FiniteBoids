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

    def heading(self):
        return math.atan2(self.y, self.x)

    @staticmethod
    def sub_vector(v1, v2):
        return Vec(v1.x - v2.x, v1.y - v2.y)

    @staticmethod
    def distance(v1, v2):
        return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)

    @staticmethod
    def angleBetween(v1, v2):
        return math.acos(v1.dot(v2) / (v1.magnitude() * v2.magnitude()))

    def __str__(self):
        return "({}, {})".format(self.x, self.y)