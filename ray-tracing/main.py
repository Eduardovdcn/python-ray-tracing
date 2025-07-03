from point import Ponto
from vector import Vetor
from camera import Camera
from objects import Esfera, Plano, Triangulo, MalhaT
from obj_reader import ObjReader
import numpy as np

def cor_para_ppm(cor):
    # Garante que os valores estejam entre 0 e 255 e converte para int
    return f"{int(max(0, min(255, cor.x)))} {int(max(0, min(255, cor.y)))} {int(max(0, min(255, cor.z)))}"

def main():
    reader = ObjReader("C:/Users/eduar/OneDrive/Documentos/GitHub/python-ray-tracing/inputs/icosahedron.obj")

    # Configura a câmera
    camera = Camera(
        C=Ponto(-10, 0, 0),      # Posição da camera 
        M=Ponto(0, 0, 0),      # Mira (olhando para origem)
        Vup=Vetor(0, 1, 0),
        d=0.5,                     # Campo de visao 
        Vres=200,
        Hres=200
    )

    # Cria objetos
    esfera = Esfera(raio=4, centro=Ponto(0, 1, 0), cor=Vetor(255, 0, 0))
    plano = Plano(ponto=Ponto(0, -1, 0), vetorNormal=Vetor(0, 1, 0), cor=Vetor(200, 200, 200))

    # Cria a malha
    faces = reader.get_faces()
    vertices = reader.get_vertices()
    malha = MalhaT(faces=faces, vertices=vertices)

    # Cada face da malha cria um triangulo
    for face in faces:
        idx1, idx2, idx3 = face.vertice_indices
        v1 = vertices[idx1]
        v2 = vertices[idx2]
        v3 = vertices[idx3]
        cor = face.kd
        triangulo = Triangulo(v1, v2, v3, cor)
        malha.triangulos.append(triangulo)
        malha.normaisTriangulos.append(triangulo.normal)
        malha.numTriangulos += 1

    malha.calcular_normais_vertices()

    triangulo_teste = Triangulo(Ponto(-2, -1, -1), Ponto(-2, 1, -1), Ponto(-2, 0, 1), Vetor(255, 255, 0))
    objetos = [plano, triangulo_teste] 
    # Cria imagem
    imagem = np.zeros((camera.Vres, camera.Hres, 3), dtype=np.uint8)

    for i in range(camera.Vres):
        for j in range(camera.Hres):
            ray = camera.get_ray(j, i)
            cor_pixel = Vetor(0, 0, 0)  # Cor de fundo padrão
            menor_t = float('inf')
            for obj in objetos:
                resultado = obj.intersect(ray.origem, ray.direcao)
                if resultado is not None and resultado[0] == True:
                    t = resultado[1]
                    if t is not None:
                        if t < menor_t:
                            menor_t = t
                            cor_pixel = resultado[4]

            imagem[i, j] = [cor_pixel.x, cor_pixel.y, cor_pixel.z]

    # Exporta para PPM
    with open("output.ppm", "w") as f:
        f.write(f"P3\n{camera.Hres} {camera.Vres}\n255\n")
        for i in range(camera.Vres):
            for j in range(camera.Hres):
                f.write(f"{imagem[i, j, 0]} {imagem[i, j, 1]} {imagem[i, j, 2]} ")
            f.write("\n")

if __name__ == "__main__":
    main()
