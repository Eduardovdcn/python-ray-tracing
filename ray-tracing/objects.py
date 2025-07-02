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

class Triangulo:
    def __init__(self, v1, v2, v3, cor):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.normal = (v2.__sub__(v1)).produto_vetorial(v3.__sub__(v1)).normalizar()
        self.cor = cor

    def intersect(self, posCamera, vetorDiretor):
        # Implementar a interseção com o triângulo
        pass


class MalhaT:
    def __init__(self, faces, vertices):
        self.vertices = vertices
        self.faces = faces
        self.numVertices = len(vertices)
        self.numFaces = len(faces)
        self.triangulos = []
        self.numTriangulos = 0
        self.normaisTriangulos = []
        self.normaisVertices = []

    def calcular_normais_vertices(self):
        # Para cada vértice, verifica em que triangulos esta e soma as normais desses triangulos
        for vertice in (self.vertices):
            soma_normal = None
            for triangulo in (self.triangulos):
                # Se o vértice faz parte do triângulo
                if (triangulo.v1 == vertice or triangulo.v2 == vertice or triangulo.v3 == vertice):
                    if soma_normal is None:
                        soma_normal = triangulo.normal
                    else:
                        soma_normal = soma_normal.soma(triangulo.normal)
            if soma_normal is not None:
                self.normaisVertices.append(soma_normal.normalizar())


    def intersect(self, posCamera, vetorDiretor):
        # Implementar a interseção com a malha
        pass
