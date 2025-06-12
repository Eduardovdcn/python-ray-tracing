import math

class Ponto:
    """
    Representa um ponto em um espaço tridimensional.

    Atributos:
        x (float): Coordenada X do ponto.
        y (float): Coordenada Y do ponto.
        z (float): Coordenada Z do ponto.
    """

    def __init__(self, x: float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
        return f"Ponto({self.x}, {self.y}, {self.z})"

    @staticmethod
    def somaBaricentrica(p1, w1, p2, w2, p3, w3):
        """Retorna a combinação baricêntrica de três pontos."""
        x = p1.x * w1 + p2.x * w2 + p3.x * w3
        y = p1.y * w1 + p2.y * w2 + p3.y * w3
        z = p1.z * w1 + p2.z * w2 + p3.z * w3
        return Ponto(x, y, z)

    def dist(self, outro):
        return math.sqrt((self.x - outro.x) ** 2 + (self.y - outro.y) ** 2 + (self.z - outro.z) ** 2)

    def multEscalar(self, escalar: float):
        return Ponto(self.x * escalar, self.y * escalar, self.z * escalar)