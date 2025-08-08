import math
from point import Ponto
from vector import Vetor
from camera import Camera
from objects import Esfera, Plano, Triangulo, MalhaT, Material
from obj_reader import ObjReader, Face
from affine_transformation import TransformacaoAfim
from illumination import phong, Luz
import numpy as np

def cor_para_ppm(cor):
    # Garante que os valores estejam entre 0 e 255 e converte para int
    return f"{int(max(0, min(255, cor.x)))} {int(max(0, min(255, cor.y)))} {int(max(0, min(255, cor.z)))}"

def renderizar_cena(camera, objetos, luzes, filename):
    imagem = np.zeros((camera.Vres, camera.Hres, 3), dtype=np.uint8)
    from illumination import intersect  # Importa aqui para evitar import circular
    for i in range(camera.Vres):
        for j in range(camera.Hres):
            ray = camera.get_ray(j, i)
            # Descobre o objeto mais próximo atingido pelo raio
            resultado = intersect(ray.origem, ray.direcao, objetos)
            if resultado is not None and resultado[0]:
                _, t, normal, ponto, material = resultado
                cor_pixel = phong(luzes, material, ray, normal, ponto, objetos, 0)
            else:
                cor_pixel = Vetor(0, 0, 0)  # Cor de fundo
            imagem[i, j] = [
                int(max(0, min(255, cor_pixel.x))),
                int(max(0, min(255, cor_pixel.y))),
                int(max(0, min(255, cor_pixel.z)))
            ]

    with open(filename, "w") as f:
        f.write(f"P3\n{camera.Hres} {camera.Vres}\n255\n")
        for i in range(camera.Vres):
            for j in range(camera.Hres):
                f.write(cor_para_ppm(Vetor(*imagem[i, j])) + " ")
            f.write("\n")
    print(f"Imagem renderizada e salva como '{filename}'")

    return imagem

def criar_toro(raio_maior, raio_menor, num_segmentos_maior, num_segmentos_menor):
    """
    Gera os vértices e as faces de um toro (donut) como uma malha de triângulos.
    """
    vertices = []
    faces = []

    # 1. Gerar os Vértices
    for i in range(num_segmentos_maior):
        phi = (i / num_segmentos_maior) * 2 * math.pi
        for j in range(num_segmentos_menor):
            theta = (j / num_segmentos_menor) * 2 * math.pi
            x = (raio_maior + raio_menor * math.cos(theta)) * math.cos(phi)
            y = (raio_maior + raio_menor * math.cos(theta)) * math.sin(phi)
            z = raio_menor * math.sin(theta)
            vertices.append(Ponto(x, y, z))

    # 2. Conectar os Vértices para Criar as Faces
    for i in range(num_segmentos_maior):
        for j in range(num_segmentos_menor):
            v1_idx = i * num_segmentos_menor + j
            v2_idx = ((i + 1) % num_segmentos_maior) * num_segmentos_menor + j
            v3_idx = ((i + 1) % num_segmentos_maior) * num_segmentos_menor + ((j + 1) % num_segmentos_menor)
            v4_idx = i * num_segmentos_menor + ((j + 1) % num_segmentos_menor)

            # CORREÇÃO DA ORDEM DOS VÉRTICES PARA A NORMAL APONTAR PARA FORA
            face1 = Face()
            face1.vertice_indices = [v1_idx, v4_idx, v2_idx]
            
            face2 = Face()
            face2.vertice_indices = [v2_idx, v4_idx, v3_idx]
            
            faces.append(face1)
            faces.append(face2)
            
    return vertices, faces

def main():
    reader = ObjReader("inputs/icosahedron.obj")
    luzes = [Luz(posicao=Ponto(0, 5, 5), intensidade=Vetor(255, 255, 255))]

    # Cria objetos
    esfera = Esfera(raio=1, 
                    centro=Ponto(0, 0, 0), 
                    cor=Vetor(255, 0, 0), 
                    n=20, 
                    ka=Vetor(0.5, 0.5, 0.5),
                    kd=Vetor(1, 0, 0),
                    ks=Vetor(0.5, 0.5, 0.5), 
                    kr=Vetor(0.1, 0.1, 0.1),
                    kt=0
                    )
    
    plano = Plano(ponto=Ponto(0, -4, 0), 
                  vetorNormal=Vetor(0, 1, 0), 
                  cor=Vetor(200, 200, 200), 
                  n=1000, 
                  kd=Vetor(0.7, 0.7, 0.7), 
                  ks=Vetor(0.8, 0.8, 0.8), 
                  ka=Vetor(0.3, 0.3, 0.3),
                  kr=Vetor(0.6, 0.6, 0.6),
                  kt=0
                  )

    # --- INÍCIO DA CRIAÇÃO DO TORO ---
    vertices_toro, faces_toro = criar_toro(raio_maior=3, raio_menor=1, num_segmentos_maior=12, num_segmentos_menor=8)
    
    material_toro = Material(
        cor=Vetor(255, 215, 0),
        n=50,
        kd=Vetor(0.7, 0.5, 0.1),
        ks=Vetor(0.9, 0.9, 0.9),
        ka=Vetor(0.2, 0.2, 0.2),
        kr=Vetor(0.3, 0.3, 0.3),
        kt=0
    )
    
    # Atribui o material a cada face do toro
    for face in faces_toro:
        face.cor = material_toro.cor
        face.ka = material_toro.ka
        face.kd = material_toro.kd
        face.ks = material_toro.ks
        face.ns = material_toro.coeficienteRugosidade
        face.kr = material_toro.kr
        face.kt = material_toro.kt
        
    toro = MalhaT(faces=faces_toro, vertices=vertices_toro)
    
    transformador = TransformacaoAfim()
    #toro = transformador.rotacaoY(45, toro)  # Gira 45 graus em torno do eixo Y
    #toro = transformador.translacao(0, 0, 5, toro)          # Depois translada
    # --- FIM DA CRIAÇÃO DO TORO ---


    # Cria a malha do icosaedro
    faces_icosaedro = reader.get_faces()
    vertices_icosaedro = reader.get_vertices()
    malha = MalhaT(faces=faces_icosaedro, vertices=vertices_icosaedro)
    
    # Aplica uma transformação para mover o icosaedro
    malha_transformada = transformador.translacao(5, 0, 5, malha)


    # Configura a câmera
    camera = Camera(
        C=Ponto(-5, 5, -15),      # Posição da camera 
        M=Ponto(0, 0, 0),      # Mira (olhando para origem)
        Vup=Vetor(0, 1, 0),
        d=2,                     # Campo de visao 
        Vres=100,
        Hres=100
    )

    objetos = [esfera, plano, toro] 
    renderizar_cena(camera, objetos, luzes, "output.ppm")

if __name__ == "__main__":
    main()
