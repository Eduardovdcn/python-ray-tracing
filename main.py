from point import Ponto
from vector import Vetor
from camera import Camera
from objects import Esfera, Plano, Triangulo, MalhaT
from obj_reader import ObjReader
from affine_transformation import TransformacaoAfim
from illumination import phong, Luz
from ray import Ray
import numpy as np
import math
from obj_reader import Face 
from objects import Material
from toro_generation import criar_toro



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
    reader = ObjReader("inputs/icosahedron.obj")
    luzes = [Luz(posicao=Ponto(-5, 5, 5), intensidade=Vetor(255, 255, 255)),
             #Luz(posicao=Ponto(5, -5, -5), intensidade=Vetor(255, 255, 255))
             ]


    # --- INÍCIO DA ADIÇÃO DO TORO ---

    # 1. Gera a geometria do Toro
    vertices_toro, faces_toro = criar_toro(raio_maior=3, raio_menor=1, num_segmentos_maior=12, num_segmentos_menor=6)

    # 2. Cria um Material para o Toro
    material_toro = Material(
        cor=Vetor(255, 215, 0),  # Cor dourada
        n=50,                     # Brilho focado
        kd=Vetor(0.8, 0.8, 0.8),  # Coeficiente Difuso
        ks=Vetor(0.9, 0.9, 0.9),  # Coeficiente Especular (brilho branco forte)
        ka=Vetor(0.2, 0.2, 0.2),  # Coeficiente Ambiente
        kr=Vetor(1, 1, 1),        # Reflexão (ajuste conforme desejado)
        kt=0.0                    # Transparência (0 = opaco)
    )

    # 3. Atribui o material a cada face gerada.
    for face in faces_toro:
        face.ka = material_toro.ka
        face.kd = material_toro.kd
        face.ks = material_toro.ks
        face.ns = material_toro.coeficienteRugosidade
        # Como não temos kr e kt, não os atribuímos aqui.

    # 4. Cria o objeto MalhaT com os vértices e faces do toro.
    toro = MalhaT(faces=faces_toro, vertices=vertices_toro)

    # --- FIM DA ADIÇÃO DO TORO ---


    # Cria objetos
    esfera = Esfera(raio=2, 
                    centro=Ponto(5, 2, -4), 
                    cor=Vetor(150, 0, 150), 
                    n=20, 
                    kd=Vetor(0.85, 0.85, 0.85), 
                    ks=Vetor(0.5, 0.5, 0.5), 
                    ka=Vetor(0.4, 0.3, 0.3),
                    kr= Vetor(1,1,1),
                    kt= 1
                    )
    
    esfera2 = Esfera(raio=2, 
                    centro=Ponto(7, 2, 4), 
                    cor=Vetor(0, 150, 0), 
                    n=20, 
                    kd=Vetor(0.85, 0.85, 0.85), 
                    ks=Vetor(0.5, 0.5, 0.5), 
                    ka=Vetor(0.4, 0.3, 0.3),
                    kr= Vetor(1,1,1),
                    kt= 0.7
                    )
    
    plano = Plano(ponto=Ponto(0, -1.5, 5), 
                  vetorNormal=Vetor(0, 1, 0), 
                  cor=Vetor(0, 0, 200), 
                  n=2, 
                  kd=Vetor(1, 1, 1), 
                  ks=Vetor(0.5, 0.5, 0.5), 
                  ka=Vetor(1, 1, 1),
                  kr= Vetor(1, 1, 1),
                  kt= 0.3
                  )

    plano2 = Plano(ponto=Ponto(0, 5, 5),
                   vetorNormal=Vetor(0,1,0),
                   cor=Vetor(0,0,200),
                   n=2,
                   kd=Vetor(1,1,1),
                   ks=Vetor(0.5,0.5,0.5),
                   ka=Vetor(1,1,1),
                   kr=Vetor(0.4, 0.4, 0.4),
                   kt= 0.3
                   )

    # Cria a malha
    faces = reader.get_faces()
    vertices = reader.get_vertices()
    malha = MalhaT(faces=faces, vertices=vertices)

     # Configuração da Câmera (sugiro afastar um pouco para ver todos os objetos)
    camera = Camera(
        C=Ponto(10, 3, 15),      # Posição da câmera (em frente ao toro, afastada no Z)
        M=Ponto(0, 0, 0),       # Mira para o centro da cena
        Vup=Vetor(0, 1, 0),
        d=2,
        Vres=100,
        Hres=100
    )


    objetos = [toro] 
    renderizar_cena(camera, objetos, luzes, "output_original.ppm")

    #Transformacao afim
    #transformador = TransformacaoAfim()
    #malhaTransformada = transformador.rotacaoX(90, malha)

    #objetos = [malhaTransformada]
    #renderizar_cena(camera, objetos, luzes, "output_transformado.ppm")

if __name__ == "__main__":
    main()
