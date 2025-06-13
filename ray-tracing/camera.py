from point import Ponto
from vector import Vetor
from ray import Ray

class Camera:

    def __init__(self, C: Ponto, M: Ponto, Vup: Vetor, d, Vres, Hres):
        self.C = C
        self.M = M
        self.Vup = Vup
        self.d = d
        self.Vres = Vres
        self.Hres = Hres
        self.vetores_ortonormais()

    def vetores_ortonormais(self):
        self.W = -((self.C - self.M).normalizar())
        self.U = self.Vup.produto_vetorial(self.W).normalizar()
        self.V = self.W.produto_vetorial(self.U).normalizar()

    def novo_local(self, novoC: Ponto):
        self.C = novoC
        self.vetores_ortonormais()

    def nova_mira(self, novoM: Ponto):
        self.M = novoM
        self.vetores_ortonormais()

    def get_ray(self, i: int, j: int) -> Ray:
        """Retorna um ray saindo da camera até o pixel (i, j)"""
        centro_tela = (self.W.mult_escalar(self.d)).soma(self.C)

        i_normalizado = 2*(i - self.Hres / 2) / self.Hres
        j_normalizado = 2*(j - self.Vres / 2) / self.Vres

        vetor_i_offset = self.U.mult_escalar(i_normalizado)
        vetor_j_offset = self.V.mult_escalar(j_normalizado)

        ponto = centro_tela.soma(vetor_i_offset).soma(vetor_j_offset)
        direcao = ponto - self.C.to_vetor()
        return Ray(self.C, direcao)
        
    def to_vetor(self):
        from vector import Vetor
        return Vetor(self.x, self.y, self.z)

    def __sub__(self, other):
        # Permite Vetor - Vetor ou Vetor - Ponto
        return Vetor(self.x - other.x, self.y - other.y, self.z - other.z)
