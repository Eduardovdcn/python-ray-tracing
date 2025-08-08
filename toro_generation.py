import math
from obj_reader import Ponto
from obj_reader import Face

def criar_toro(raio_maior, raio_menor, num_segmentos_maior, num_segmentos_menor):
    """
    Gera os vértices e as faces de um toro (donut) como uma malha de triângulos.
    """
    vertices = []
    faces = []

    # 1. Gera os Vértices
    for i in range(num_segmentos_maior):
        phi = (i / num_segmentos_maior) * 2 * math.pi
        for j in range(num_segmentos_menor):
            theta = (j / num_segmentos_menor) * 2 * math.pi
            x = (raio_maior + raio_menor * math.cos(theta)) * math.cos(phi)
            y = (raio_maior + raio_menor * math.cos(theta)) * math.sin(phi)
            z = raio_menor * math.sin(theta)
            vertices.append(Ponto(x, y, z))

    # 2. Conecta os Vértices para Criar as Faces
    for i in range(num_segmentos_maior):
        for j in range(num_segmentos_menor):
            v1_idx = i * num_segmentos_menor + j
            v2_idx = ((i + 1) % num_segmentos_maior) * num_segmentos_menor + j
            v3_idx = ((i + 1) % num_segmentos_maior) * num_segmentos_menor + ((j + 1) % num_segmentos_menor)
            v4_idx = i * num_segmentos_menor + ((j + 1) % num_segmentos_menor)

            face1 = Face()
            face1.vertice_indices = [v1_idx, v4_idx, v2_idx]
            
            face2 = Face()
            face2.vertice_indices = [v2_idx, v4_idx, v3_idx]
            
            faces.append(face1)
            faces.append(face2)
            
    return vertices, faces