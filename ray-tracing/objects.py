class Esfera:
    def __init__(self, raio, centro, cor):
        self.raio = raio
        self.centro = centro
        self.cor = cor

    def intersect(self, posCamera, vetorDiretor):
        origemToCentro = posCamera - self.centro
        a = vetorDiretor.produto_escalar(vetorDiretor)
        b = 2 * origemToCentro.produto_escalar(vetorDiretor)
        c = origemToCentro.produto_escalar(origemToCentro) - self.raio ** 2
        delta = b ** 2 - 4 * a * c
        if delta < 0:
            return None
        t1 = (-b - delta ** 0.5) / (2 * a)
        t2 = (-b + delta ** 0.5) / (2 * a)
        if t1 >= 0 and t2 >= 0:
            return min(t1, t2)
        elif t1 >= 0:
            return t1
        elif t2 >= 0:
            return t2
        else:
            return None

class Plano:
    def __init__(self, ponto, vetorNormal, cor):
        self.ponto = ponto
        self.vetorNormal = vetorNormal
        self.cor = cor

    def intersect(self, posCamera, vetorDiretor):
        temp = vetorDiretor.produto_escalar(self.vetorNormal)
        if temp == 0:
            return None
        origemToCentro = posCamera - self.ponto
        t = origemToCentro.produto_escalar(self.vetorNormal) / temp
        if t < 0:
            return None
        return t
