import math
import numpy as np
from point import Ponto
from vector import Vetor

class Matrix:
    """
    Classe para representar e manipular matrizes 4x4, usadas para transformações afins.
    """
    def __init__(self, initial_matrix=None):
        if initial_matrix is None:
            # Inicializa como uma matriz identidade se nenhuma for fornecida
            self.m = np.identity(4)
        else:
            self.m = np.array(initial_matrix)

    @staticmethod
    def make_translation(x, y, z):
        """Cria uma matriz de translação."""
        return Matrix([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def make_scale(x, y, z):
        """Cria uma matriz de escala."""
        return Matrix([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def make_rotation_x(angle_degrees):
        """Cria uma matriz de rotação em torno do eixo X."""
        angle_rad = math.radians(angle_degrees)
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def make_rotation_y(angle_degrees):
        """Cria uma matriz de rotação em torno do eixo Y."""
        angle_rad = math.radians(angle_degrees)
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def make_rotation_z(angle_degrees):
        """Cria uma matriz de rotação em torno do eixo Z."""
        angle_rad = math.radians(angle_degrees)
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def __mul__(self, other):
        """Multiplica duas matrizes."""
        if isinstance(other, Matrix):
            return Matrix(np.dot(self.m, other.m))
        return NotImplemented

    def apply_to_point(self, point: Ponto) -> Ponto:
        """Aplica a matriz de transformação a um ponto."""
        # Converte o ponto para coordenadas homogêneas (x, y, z, 1)
        p_homogeneous = np.array([point.x, point.y, point.z, 1])
        # Aplica a transformação
        p_transformed = np.dot(self.m, p_homogeneous)
        # Converte de volta para coordenadas 3D
        return Ponto(p_transformed[0], p_transformed[1], p_transformed[2])

    def apply_to_vector(self, vector: Vetor) -> Vetor:
        """Aplica a matriz de transformação a um vetor."""
        # Converte o vetor para coordenadas homogêneas (x, y, z, 0)
        v_homogeneous = np.array([vector.x, vector.y, vector.z, 0])
        # Aplica a transformação
        v_transformed = np.dot(self.m, v_homogeneous)
        # Converte de volta para coordenadas 3D
        return Vetor(v_transformed[0], v_transformed[1], v_transformed[2])

