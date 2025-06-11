import math

class Vector:
    """
    Representa um vetor em um espaço tridimensional.

    Atributos:
        x (float): Componente do vetor na direção X.
        y (float): Componente do vetor na direção Y.
        z (float): Componente do vetor na direção Z.
    """
    def __init__(self, x: float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
        return f"Vetor({self.x}, {self.y}, {self.z})"
    
    def norma(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def soma(self, outro):
        return Vector(self.x + outro.x, self.y + outro.y, self.z + outro.z)

    def sub(self, outro):
        return Vector(self.x - outro.x, self.y - outro.y, self.z - outro.z)

    def dist(self, outro):
        return math.sqrt((self.x - outro.x) ** 2 + (self.y - outro.y) ** 2 + (self.z - outro.z) ** 2)

    def mult_escalar(self, escalar: float):
        return Vector(self.x * escalar, self.y * escalar, self.z * escalar)

    def produto_escalar(self, outro):
        return self.x * outro.x + self.y * outro.y + self.z * outro.z

    def produto_vetorial(self, outro):
        return Vector(
            self.y * outro.z - self.z * outro.y,
            self.z * outro.x - self.x * outro.z,
            self.x * outro.y - self.y * outro.x
        )

    def normalizar(self):
        n = self.norma()
        if n == 0:
            raise ValueError("Não é possível normalizar o vetor nulo.")
        return Vector(self.x / n, self.y / n, self.z / n)
