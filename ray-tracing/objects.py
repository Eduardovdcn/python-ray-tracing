import numpy as np
from point import Ponto
from vector import Vetor

class Esfera:
    def __init__(self, raio, centro, cor):
        self.raio = raio
        self.centro = centro
        self.cor = cor
        self.t = float('inf')

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
        
        if t1 > 0.001 and t1 < self.t:
            self.t = t1
            return t1
        if t2 > 0.001 and t2 < self.t:
            self.t = t2
            return t2
        return None


class Plano:
    def __init__(self, ponto, vetorNormal, cor):
        self.ponto = ponto
        self.vetorNormal = vetorNormal.normalizar()
        self.cor = cor
        self.t = float('inf')


    def intersect(self, posCamera, vetorDiretor):
        denominador = vetorDiretor.produto_escalar(self.vetorNormal)
        if abs(denominador) > 0.001: # Evita divisão por zero e raios paralelos ao plano
            numerador = (self.ponto - posCamera).produto_escalar(self.vetorNormal)
            t = numerador / denominador
            if t > 0.001 and t < self.t:
                self.t = t
                return t
        return None

class Triangulo:
    def __init__(self, v1, v2, v3, cor):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        # A normal é calculada e normalizada na inicialização
        edge1 = self.v2 - self.v1
        edge2 = self.v3 - self.v1
        self.normal = edge1.produto_vetorial(edge2).normalizar()
        self.cor = cor
        self.t = float('inf')

    def intersect(self, posCamera, vetorDiretor):
        """
        Implementa o algoritmo de interseção Möller-Trumbore.
        """
        EPSILON = 0.000001
        edge1 = self.v2 - self.v1
        edge2 = self.v3 - self.v1
        
        h = vetorDiretor.produto_vetorial(edge2)
        a = edge1.produto_escalar(h)

        if -EPSILON < a < EPSILON:
            return None  # O raio é paralelo ao triângulo.

        f = 1.0 / a
        s = posCamera - self.v1
        u = f * s.produto_escalar(h)

        if u < 0.0 or u > 1.0:
            return None

        q = s.produto_vetorial(edge1)
        v = f * vetorDiretor.produto_escalar(q)

        if v < 0.0 or u + v > 1.0:
            return None

        # Neste ponto, sabemos que há uma interseção.
        t = f * edge2.produto_escalar(q)

        if t > EPSILON:  # Interseção com o raio
            if t < self.t:
                self.t = t
                return t
        
        return None


class MalhaT:
    def __init__(self, faces, vertices, cor=Vetor(255, 255, 255)):
        self.vertices = vertices
        self.faces = faces
        self.cor = cor
        self.numVertices = len(vertices)
        self.numFaces = len(faces)
        self.triangulos = []
        self.numTriangulos = 0
        self.normaisTriangulos = []
        self.normaisVertices = []
        self.t = float('inf')
        self._build_triangles()
        self.calcular_normais_vertices()

    def _build_triangles(self):
        """Constrói a lista de triângulos a partir das faces e vértices."""
        self.triangulos = []
        self.normaisTriangulos = []
        for face in self.faces:
            idx1, idx2, idx3 = face.vertice_indices
            v1 = self.vertices[idx1]
            v2 = self.vertices[idx2]
            v3 = self.vertices[idx3]
            # Usa a cor da face se disponível, senão a cor da malha
            cor = face.kd if face.kd.norma() > 0 else self.cor
            triangulo = Triangulo(v1, v2, v3, cor)
            self.triangulos.append(triangulo)
            self.normaisTriangulos.append(triangulo.normal)
        self.numTriangulos = len(self.triangulos)


    def calcular_normais_vertices(self):
        """Para cada vértice, verifica em que triangulos esta e soma as normais desses triangulos"""
        self.normaisVertices = [Vetor(0, 0, 0)] * self.numVertices
        for i, vertice in enumerate(self.vertices):
            soma_normal = Vetor(0,0,0)
            count = 0
            for triangulo in self.triangulos:
                # Se o vértice faz parte do triângulo
                if (triangulo.v1.dist(vertice) < 0.001 or 
                    triangulo.v2.dist(vertice) < 0.001 or 
                    triangulo.v3.dist(vertice) < 0.001):
                    soma_normal = soma_normal.soma(triangulo.normal)
                    count += 1
            if count > 0:
                self.normaisVertices[i] = soma_normal.normalizar()


    def intersect(self, posCamera, vetorDiretor):
        """
        Verifica a interseção do raio com cada triângulo da malha
        e retorna a interseção mais próxima.
        """
        menor_t = float('inf')
        hit_obj = None

        for triangulo in self.triangulos:
            t = triangulo.intersect(posCamera, vetorDiretor)
            if t is not None and t < menor_t:
                menor_t = t
                hit_obj = triangulo
        
        if hit_obj:
            self.t = menor_t
            # A cor retornada é a do triângulo atingido
            self.cor = hit_obj.cor
            return menor_t
            
        return None

    def transform(self, matrix):
        """Aplica uma transformação a todos os vértices da malha."""
        transformed_vertices = []
        for v in self.vertices:
            transformed_vertices.append(v.transform(matrix))
        self.vertices = transformed_vertices
        # Reconstrói os triângulos com os novos vértices
        self._build_triangles()
        self.calcular_normais_vertices()

