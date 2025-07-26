class Material:
    def __init__(self, cor, n, kd, ks, ka, ns, ni):
        self.cor = cor  # Cor do material
        self.coeficienteRugosidade = n  # Coeficiente de rugosidade
        self.kd = kd  # Coeficiente de difusão
        self.ks = ks  # Coeficiente especular
        self.ka = ka  # Coeficiente de ambiente
        self.ns = ns  # Coeficiente de reflexão
        self.ni = ni  # Indice de refração

class Esfera:
    def __init__(self, raio, centro, cor, n, kd, ks, ka, ns, ni):
        self.raio = raio
        self.centro = centro
        self.cor = cor
        self.material = Material(cor, n, kd, ks, ka, ns, ni)

    def intersect(self, posCamera, vetorDiretor):
        condicao = True
        origemToCentro = posCamera - self.centro
        a = vetorDiretor.produto_escalar(vetorDiretor)
        b = 2 * origemToCentro.produto_escalar(vetorDiretor)
        c = origemToCentro.produto_escalar(origemToCentro) - self.raio ** 2
        delta = b ** 2 - 4 * a * c
        if delta < 0:
            condicao = False
            return (condicao, None, None, None, self.material)
        t1 = (-b - delta ** 0.5) / (2 * a)
        t2 = (-b + delta ** 0.5) / (2 * a)
        
        if t1 >= 0 and t2 >= 0:
            pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(min(t1, t2)))
            normal = (pontoInterseccao - self.centro).normalizar()
            return (condicao, min(t1, t2), normal, pontoInterseccao, self.material)
        elif t1 >= 0:
            pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(t1))
            normal = (pontoInterseccao - self.centro).normalizar()
            return (condicao, t1, normal, pontoInterseccao, self.material)
        elif t2 >= 0:
            pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(t2))
            normal = (pontoInterseccao - self.centro).normalizar()
            return (condicao, t2, normal, pontoInterseccao, self.material)

        return (condicao, None, None, None, self.material)

class Plano:
    def __init__(self, ponto, vetorNormal, cor, n, kd, ks, ka, ns, ni):
        self.ponto = ponto
        self.vetorNormal = vetorNormal.normalizar()
        self.material = Material(cor, n, kd, ks, ka, ns, ni)

    def intersect(self, posCamera, vetorDiretor):
        condicao = True
        temp = vetorDiretor.produto_escalar(self.vetorNormal)
        if temp == 0:
            condicao = False
            return (condicao, None, None, None, self.material)
        origemToCentro = self.ponto - posCamera
        t = origemToCentro.produto_escalar(self.vetorNormal) / temp
        if t < 0:
            condicao = False
            return (condicao, None, None, None, self.material)

        pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(t))
        return (condicao, t, self.vetorNormal, pontoInterseccao, self.material)

class Triangulo:
    def __init__(self, v1, v2, v3, cor, kd, ks, ka, ns, ni, n):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.normal = (v2.__sub__(v1)).produto_vetorial(v3.__sub__(v1)).normalizar()
        self.material = Material(cor, n, kd, ks, ka, ns, ni)

    def intersect(self, posCamera, vetorDiretor):
        # Cria o plano do triangulo e verifica se o raio intersecta
        condicao = True
        planoTriangulo = Plano(self.v1, self.normal, self.material.cor, self.material.coeficienteRugosidade, self.material.kd, self.material.ks, self.material.ka, self.material.ns, self.material.ni)
        resultado_plano = planoTriangulo.intersect(posCamera, vetorDiretor)
        # Verifica se intersecta e se o t eh valido
        if resultado_plano is None or resultado_plano[0] == False:
            condicao = False
            return (condicao, None, None, None, self.material)
            
        t = resultado_plano[1]

        if t <= 1e-10:
            condicao = False
            return (condicao, None, None, None, self.material)

        # Calcula o ponto de interseccao e verifica se esta dentro do triangulo
        pontoInterseccao = posCamera.__soma__(vetorDiretor.mult_escalar(t))
        return self.ponto_interno(t, pontoInterseccao, self.material)

    def ponto_interno(self, t, ponto, material):
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
            return (condicao, None, None, None, self.material)
        # Coordenadas baricentricas
        alfa = (d11 * d20 - d01 * d21) / denom
        beta = (d00 * d21 - d01 * d20) / denom
        gama = 1.0 - alfa - beta
        # Verifica se o ponto esta dentro do triangulo
        if alfa >= 1e-10 and beta >= 1e-10 and gama >= 1e-10:
            return (True, t, self.normal, ponto, self.material)
        else:
            return (False, None, None, None, self.material)

class MalhaT:
    def __init__(self, faces, vertices):
        self.vertices = vertices
        self.numVertices = len(vertices)
        self.faces = faces
        self.numFaces = len(faces)
        self.triangulos = []
        self.numTriangulos = 0
        self.normaisTriangulos = []
        self.normaisVertices = []
        self._build_triangles()
        self.calcular_normais_vertices()
        self.centro = self.calcular_centro()

    def _build_triangles(self):
        for face in self.faces:
            idx1, idx2, idx3 = face.vertice_indices
            v1 = self.vertices[idx1]
            v2 = self.vertices[idx2]
            v3 = self.vertices[idx3]
            cor = face.kd.mult_escalar(255)  # Multiplica por 255 para converter de [0, 1] para [0, 255] 
            triangulo = Triangulo(v1, v2, v3, cor, face.kd, face.ks, face.ka, face.ns, face.ni, n=2)
            self.triangulos.append(triangulo)
            self.normaisTriangulos.append(triangulo.normal)
            self.numTriangulos += 1

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
                _, t, normal, ponto, material = resultado
                # Se o t eh valido e menor que o atual, vira o menor
                if t is not None and t < menor_t and t > 1e-10:
                    menor_t = t
                    menor_resultado = (True, t, normal, ponto, material)

        if menor_resultado is None:
            from vector import Vetor
            return (False, None, None, None, Vetor(0, 0, 0)) 
         
        return menor_resultado
    
    def calcular_centro(self):
        from point import Ponto
        centro_x = sum(v.x for v in self.vertices) / self.numVertices
        centro_y = sum(v.y for v in self.vertices) / self.numVertices
        centro_z = sum(v.z for v in self.vertices) / self.numVertices
        return Ponto(centro_x, centro_y, centro_z)
    

