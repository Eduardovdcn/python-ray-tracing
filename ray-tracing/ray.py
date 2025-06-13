from point import Ponto
from vector import Vetor

class Ray:
    """Um raio de luz. Possui um ponto de origem e um vetor que indica sua direção."""

    def __init__(self, origem: Ponto, direcao: Vetor):
        self.origem = origem
        self.direcao = direcao.normalizar()

    def get_origem(self) -> Ponto:
        return self.origem

    def get_direcao(self) -> Vetor:
        return self.direcao
