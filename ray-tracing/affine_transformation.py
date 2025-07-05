import numpy as np
import math
from vector import Vetor
from point import Ponto
from objects import MalhaT, Plano

class TransformacaoAfim:
    def rotacaoZ(self, angulo, objeto):
        # Rotacao no eixo Z anti-horario
        angulo = self.toRadiano(angulo)
        c = math.cos(angulo)
        s = math.sin(angulo)
        matriz = np.array([[c, -s, 0, 0],
                        [s, c, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        return self.transformar_objeto(matriz, objeto)


    def rotacaoY(self, angulo, objeto):
        # Rotacao no eixo Y anti-horario
        angulo = self.toRadiano(angulo)
        c = math.cos(angulo)
        s = math.sin(angulo)
        matriz = np.array([[c, 0, s, 0],
                        [0, 1, 0, 0],
                        [-s, 0, c, 0],
                        [0, 0, 0, 1]])
        return self.transformar_objeto(matriz, objeto)


    def rotacaoX(self, angulo, objeto):
        # Rotacao no eixo X anti-horario
        angulo = self.toRadiano(angulo)
        c = math.cos(angulo)
        s = math.sin(angulo)
        matriz = np.array([[1, 0, 0, 0],
                        [0, c, -s, 0],
                        [0, s, c, 0],
                        [0, 0, 0, 1]])
        return self.transformar_objeto(matriz, objeto)


    def translacao(self, dx, dy, dz, objeto):
        matriz = np.array([[1, 0, 0, dx],
                        [0, 1, 0, dy],
                        [0, 0, 1, dz],
                        [0, 0, 0, 1]])
        return self.transformar_objeto(matriz, objeto)


    def escala(self, sx, sy, sz, objeto):
        matriz = np.array([[sx, 0, 0, 0],
                        [0, sy, 0, 0],
                        [0, 0, sz, 0],
                        [0, 0, 0, 1]])
        return self.transformar_objeto(matriz, objeto)


    def transformar_objeto(self, matriz, objeto):
        matriz_composta = self.calcular_transformacao(matriz, objeto)
        if isinstance(objeto, MalhaT):
            vertices_transformados = []
        #Para cada vertice aplicar a transformacao
            for v in objeto.vertices:
                vertices_transformados.append(self.aplicar_transformacao(matriz= matriz_composta, objeto=v))

            novaMalha = MalhaT(faces=objeto.faces, vertices=vertices_transformados)
            novaMalha.calcular_normais_vertices()

            return novaMalha
        #Se for apenas um ponto ou vetor
        else:
            self.aplicar_transformacao(matriz_composta, objeto)


    def aplicar_transformacao(self, matriz, objeto):
        objetoHomogeneo = np.array([objeto.x, objeto.y, objeto.z, 1])
        novoObjeto = matriz @ objetoHomogeneo  # Retorna apenas x, y e z
        novoX, novoY, novoZ = novoObjeto[:3]
        if isinstance(objeto, Ponto):
            return Ponto(novoX, novoY, novoZ)
        elif isinstance(objeto, Vetor):
            return Vetor(novoX, novoY, novoZ)
        
    
    def calcular_transformacao(self, matriz, objeto):
        if isinstance(objeto, MalhaT):
            centro = objeto.centro
        else:
            centro = Ponto(objeto.x, objeto.y, objeto.z)

        matriz = (self.moveToPosicao(centro) @
                  matriz @
                  self.moveToOrigem(centro))

        return matriz


    def moveToOrigem(self, ponto):
        """Move o objeto para a origem (0, 0, 0)"""
        return np.array([
        [1, 0, 0, -ponto.x],
        [0, 1, 0, -ponto.y],
        [0, 0, 1, -ponto.z],
        [0, 0, 0, 1]
    ])


    def moveToPosicao(self, ponto):
        """Move o objeto para a posição (x, y, z)"""
        return np.array([
        [1, 0, 0, ponto.x],
        [0, 1, 0, ponto.y],
        [0, 0, 1, ponto.z],
        [0, 0, 0, 1]
    ])


    def toRadiano(self, angulo):
        return math.radians(angulo)
