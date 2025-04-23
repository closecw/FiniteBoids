import math

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __div__(self, value):
        if value != 0:
            return Vec(self.x / value, self.y / value)

    def __mul__(self, value):
        return Vec(self.x * value, self.y * value)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            self.x /= mag
            self.y /= mag

    def limit(self, limit):
        mag = self.magnitude()
        if mag > limit:
            self.x *= limit / mag
            self.y *= limit / mag

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

def main():
    print("done")

if __name__ == "__main__":
    main()