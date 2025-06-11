import math

class Point:
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
        return f"Point({self.x}, {self.y}, {self.z})"

    def soma_pontos(self, outro):
        return Point(self.x + outro.x, self.y + outro.y, self.z + outro.z)

    def subtrai_pontos(self, outro):
        return Point(self.x - outro.x, self.y - outro.y, self.z - outro.z)

    def distancia(self, outro):
        return math.sqrt((self.x - outro.x) ** 2 + (self.y - outro.y) ** 2 + (self.z - outro.z) ** 2)

    def produto_escalar(self, escalar: float):
        return Point(self.x * escalar, self.y * escalar, self.z * escalar)