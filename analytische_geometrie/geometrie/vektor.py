import math

class Vektor(tuple):
    """

    """
    def __new__(cls, x, y=None, z=None):
        if y is None and z is None:
            # Si le pasas una lista o tupla tipo Vector([1, 2, 3])
            return super().__new__(cls, (float(x[0]), float(x[1]), float(x[2])))
        return super().__new__(cls, (float(x), float(y), float(z)))

    @property
    def x(self): return self[0]
    @property
    def y(self): return self[1]
    @property
    def z(self): return self[2]

    # Operaciones básicas
    def __add__(self, other):
        return Vektor(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __sub__(self, other):
        return Vektor(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __mul__(self, scalar):
        return Vektor(self[0] * scalar, self[1] * scalar, self[2] * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vektor(self[0] / scalar, self[1] / scalar, self[2] / scalar)

    def __neg__(self):
        return Vektor(-self[0], -self[1], -self[2])
    
    def __abs__(self):
        return math.sqrt(self[0]**2 + self[1]**2 + self[2]**2)

    def dot(self, other):
        """Skalarprodukt (Dot Product)"""
        return self[0]*other[0] + self[1]*other[1] + self[2]*other[2]

    def cross(self, other):
        """Kreuzprodukt (Cross Product)"""
        return Vektor(
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0]
        )

    def mod(self):
        return abs(self)

