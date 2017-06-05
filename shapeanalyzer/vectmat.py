import math

class Vector2:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Vector2 (%.2lf, %.2lf)" % (self.x, self.y)

    def __add__(self, v):
        return Vector2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        return self

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def cross(self, v):
        return self.x * v.y - self.y * v.x

    def normalize(self):
        length = math.hypot(self.x , self.y)
        if length == 0:
            return self
        self.x = self.x / length
        self.y = self.y / length
        return self

    def length(self):
        return math.hypot(self.x, self.y)
