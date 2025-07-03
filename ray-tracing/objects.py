class Esfera:
    def __init__(self, raio, centro, cor):
        self.raio = raio
        self.centro = centro
        self.cor = cor

    def intersect(self, posCamera, vetorDiretor):
        condicao = True
        origemToCentro = posCamera - self.centro
        a = vetorDiretor.produto_escalar(vetorDiretor)
        b = 2 * origemToCentro.produto_escalar(vetorDiretor)
        c = origemToCentro.produto_escalar(origemToCentro) - self.raio ** 2
        delta = b ** 2 - 4 * a * c
        if delta < 0:
            condicao = False
            return (condicao, None, None, None, self.cor)
        t1 = (-b - delta ** 0.5) / (2 * a)
        t2 = (-b + delta ** 0.5) / (2 * a)
        
        if t1 >= 0 and t2 >= 0:
            pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(min(t1, t2)))
            return (condicao, min(t1, t2), None, pontoInterseccao, self.cor)
        elif t1 >= 0:
            pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(t1))
            return (condicao, t1, None, pontoInterseccao, self.cor)
        elif t2 >= 0:
            pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(t2))
            return (condicao, t2, None, pontoInterseccao, self.cor)
        
        return (condicao, None, None, None, self.cor)

class Plano:
    def __init__(self, ponto, vetorNormal, cor):
        self.ponto = ponto
        self.vetorNormal = vetorNormal
        self.cor = cor

    def intersect(self, posCamera, vetorDiretor):
        condicao = True
        temp = vetorDiretor.produto_escalar(self.vetorNormal)
        if temp == 0:
            condicao = False
            return (condicao, None, None, None, self.cor)
        origemToCentro = posCamera - self.ponto
        t = origemToCentro.produto_escalar(self.vetorNormal) / temp
        if t < 0:
            condicao = False
            return (condicao, None, None, None, self.cor)

        pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(t))
        return (condicao, t, self.vetorNormal, pontoInterseccao, self.cor)

class Triangulo:
    def __init__(self, v1, v2, v3, cor):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.normal = (v2.__sub__(v1)).produto_vetorial(v3.__sub__(v1)).normalizar()
        self.cor = cor

    def intersect(self, posCamera, vetorDiretor):
        # Cria o plano do triangulo e verifica se o raio intersecta
        condicao = True
        planoTriangulo = Plano(self.v1, self.normal, self.cor)
        resultado_plano = planoTriangulo.intersect(posCamera, vetorDiretor)
        # Verifica se intersecta e se o t eh valido
        if resultado_plano is None or resultado_plano[0] == False:
            condicao = False
            return (condicao, None, None, None, self.cor)       
            
        t = resultado_plano[1]

        if t <= 1e-10:
            condicao = False
            return (condicao, None, None, None, self.cor)

        # Calcula o ponto de interseccao e verifica se esta dentro do triangulo
        pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(t))
        return self.ponto_interno(t, pontoInterseccao, self.cor)

    def ponto_interno(self, t, ponto, cor):
        vetorV1V2 = self.v2 - self.v1
        vetorV1V3 = self.v3 - self.v1
        vetorPV1 = ponto - self.v1  
        # Produtos escalares do sistema
        d00 = vetorV1V2.produto_escalar(vetorV1V2)   
        d01 = vetorV1V2.produto_escalar(vetorV1V3)     
        d11 = vetorV1V3.produto_escalar(vetorV1V3)      
        d20 = vetorPV1.produto_escalar(vetorV1V2)       
        d21 = vetorPV1.produto_escalar(vetorV1V3)       
        # Determinante 
        denom = d00 * d11 - d01 * d01
        if abs(denom) <= 1e-10:
            condicao = False
            return (condicao, None, None, None, self.cor)
        # Coordenadas baricentricas
        alfa = (d11 * d20 - d01 * d21) / denom
        beta = (d00 * d21 - d01 * d20) / denom
        gama = 1.0 - alfa - beta
        
        # Verifica se o ponto esta dentro do triangulo
        if alfa >= 1e-10 and beta >= 1e-10 and gama >= 1e-10:
            return (True, t, self.normal, ponto, cor)
        else:
            return (False, None, None, None, self.cor)

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
        # Para cada vertice, verifica em que triangulos esta e soma as normais desses triangulos
        for vertice in (self.vertices):
            soma_normal = None
            for triangulo in (self.triangulos):
                # Se o vertice faz parte do triangulo
                if (triangulo.v1 == vertice or triangulo.v2 == vertice or triangulo.v3 == vertice):
                    if soma_normal is None:
                        soma_normal = triangulo.normal
                    else:
                        soma_normal = soma_normal.soma(triangulo.normal)
            if soma_normal is not None:
                self.normaisVertices.append(soma_normal.normalizar())

    def intersect(self, posCamera, vetorDiretor):
        menor_t = float('inf')
        menor_resultado = None
        # Para cada triangulo, verifica se o raio intersecta
        for triangulo in self.triangulos:
            resultado = triangulo.intersect(posCamera, vetorDiretor)
            # Se existe intersecao
            if resultado is not None and resultado[0] == True:
                _, t, normal, ponto, cor = resultado
                # Se o t eh valido e menor que o atual, vira o menor
                if t is not None and t < menor_t and t > 1e-10:
                    menor_t = t
                    menor_resultado = (True, t, normal, ponto, cor)

        if menor_resultado is None:
            from vector import Vetor
            return (False, None, None, None, Vetor(0, 0, 0)) 
         
        return menor_resultado

