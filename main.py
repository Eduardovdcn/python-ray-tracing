from point import Ponto
from vector import Vetor
from camera import Camera
from objects import Esfera, Plano, Triangulo, MalhaT
from obj_reader import ObjReader
from affine_transformation import TransformacaoAfim
from illumination import phong, Luz
from ray import Ray
import numpy as np

def cor_para_ppm(cor):
    # Garante que os valores estejam entre 0 e 255 e converte para int
    return f"{int(max(0, min(255, cor.x)))} {int(max(0, min(255, cor.y)))} {int(max(0, min(255, cor.z)))}"


def renderizar_cena(camera, objetos, luzes, filename):
    # Cria imagem
    imagem = np.zeros((camera.Vres, camera.Hres, 3), dtype=np.uint8)
    for i in range(camera.Vres):
        for j in range(camera.Hres):
            ray = camera.get_ray(j, i)
            cor_pixel = Vetor(0, 0, 0)  # Cor de fundo padrão
            menor_t = float('inf')
            depth = 0
            for obj in objetos:
                resultado = obj.intersect(ray.origem, ray.direcao)
                if resultado is not None and resultado[0] == True:
                    t = resultado[1]
                    if t is not None:
                        if t < menor_t:
                            menor_t = t
                            cor_pixel = phong(luzes, resultado[4], ray, resultado[2], resultado[3], objetos, depth) # material = resultado[4], normal = resultado[2], pontoIntersecao = resultado[3]
                            if cor_pixel.x < 10 or cor_pixel.y < 10 or cor_pixel.z < 10:
                                print(f"Cor do pixel ({i}, {j}): {cor_pixel.x}, {cor_pixel.y}, {cor_pixel.z}")

            imagem[i, j] = [cor_pixel.x, cor_pixel.y, cor_pixel.z]

    with open(filename, "w") as f:
        f.write(f"P3\n{camera.Hres} {camera.Vres}\n255\n")
        for i in range(camera.Vres):
            for j in range(camera.Hres):
                f.write(f"{imagem[i, j, 0]} {imagem[i, j, 1]} {imagem[i, j, 2]} ")
            f.write("\n")
    print(f"Imagem renderizada e salva como '{filename}'")

    return imagem

def main():
    reader = ObjReader("C:/Users/phjc/Documents/python-ray-tracing-entrega_3/inputs/icosahedron.obj")
    luzes = [Luz(posicao=Ponto(-5, 5, 5), intensidade=Vetor(255, 255, 255)),
             Luz(posicao=Ponto(5, -5, -5), intensidade=Vetor(255, 255, 255))
             ]

    # Cria objetos
    esfera = Esfera(raio=2, 
                    centro=Ponto(5, 5, 0), 
                    cor=Vetor(150, 0, 150), 
                    n=20, 
                    kd=Vetor(0.85, 0.85, 0.85), 
                    ks=Vetor(0.5, 0.5, 0.5), 
                    ka=Vetor(0.4, 0.3, 0.3),
                    ns= 0.3,
                    ni= 0
                    )
    
    plano = Plano(ponto=Ponto(0, -1.5, 5), 
                  vetorNormal=Vetor(0, 1, 0), 
                  cor=Vetor(0, 0, 200), 
                  n=2, 
                  kd=Vetor(1, 1, 1), 
                  ks=Vetor(0.5, 0.5, 0.5), 
                  ka=Vetor(1, 1, 1),
                  ns= 0,
                  ni= 0.3
                  )

    plano2 = Plano(ponto=Ponto(0, 5, 5),
                   vetorNormal=Vetor(0,1,0),
                   cor=Vetor(0,0,200),
                   n=2,
                   kd=Vetor(1,1,1),
                   ks=Vetor(0.5,0.5,0.5),
                   ka=Vetor(1,1,1),
                   ns=0,
                   ni= 0.3
                   )

    # Cria a malha
    faces = reader.get_faces()
    vertices = reader.get_vertices()
    malha = MalhaT(faces=faces, vertices=vertices)

    # Configura a câmera
    camera = Camera(
        C=Ponto(-7, 0, 0),      # Posição da camera 
        M=malha.centro,      # Mira (olhando para origem)
        Vup=Vetor(0, 1, 0),
        d=2,                     # Campo de visao 
        Vres=300,
        Hres=300
    )

    objetos = [malha, esfera, plano, plano2] 
    renderizar_cena(camera, objetos, luzes, "output_original.ppm")

    #Transformacao afim
    #transformador = TransformacaoAfim()
    #malhaTransformada = transformador.rotacaoX(90, malha)

    #objetos = [malhaTransformada]
    #renderizar_cena(camera, objetos, luzes, "output_transformado.ppm")

if __name__ == "__main__":
    main()
