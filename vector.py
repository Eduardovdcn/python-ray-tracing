import math

class Vetor:
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
        return Vetor(self.x + outro.x, self.y + outro.y, self.z + outro.z)

    def sub(self, outro):
        return Vetor(self.x - outro.x, self.y - outro.y, self.z - outro.z)

    def dist(self, outro):
        return math.sqrt((self.x - outro.x) ** 2 + (self.y - outro.y) ** 2 + (self.z - outro.z) ** 2)

    def multEscalar(self, escalar: float):
        return Vetor(self.x * escalar, self.y * escalar, self.z * escalar)

    def produtoEscalar(self, outro):
        return self.x * outro.x + self.y * outro.y + self.z * outro.z

    def produtoVetorial(self, outro):
        return Vetor(
            self.y * outro.z - self.z * outro.y,
            self.z * outro.x - self.x * outro.z,
            self.x * outro.y - self.y * outro.x
        )

    def normalizar(self):
        n = self.norma()
        if n == 0:
            raise ValueError("Não é possível normalizar o vetor nulo.")
        return Vetor(self.x / n, self.y / n, self.z / n)
