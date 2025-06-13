from point import Ponto
from vector import Vetor
from camera import Camera
from objects import Esfera, Plano
import numpy as np

def cor_para_ppm(cor):
    # Garante que os valores estejam entre 0 e 255 e converte para int
    return f"{int(max(0, min(255, cor.x)))} {int(max(0, min(255, cor.y)))} {int(max(0, min(255, cor.z)))}"

def main():
    # Configura a câmera
    camera = Camera(
        C=Ponto(0, 0, 10),      # Posição da câmera
        M=Ponto(0, 0, 0),       # Mira (olhando para a origem)
        Vup=Vetor(0, 1, 0),     # Vetor "para cima"
        d=1,                    # Distância do plano de projeção
        Vres=200,               # Resolução vertical
        Hres=200                # Resolução horizontal
    )

    # Cria objetos
    esfera = Esfera(raio=2, centro=Ponto(0, 0, 0), cor=Vetor(255, 0, 0))
    plano = Plano(ponto=Ponto(0, -3, 0), vetorNormal=Vetor(0, 1, 0), cor=Vetor(200, 200, 200))
    objetos = [esfera, plano]

    # Cria imagem 
    imagem = np.zeros((camera.Vres, camera.Hres, 3), dtype=np.uint8)

    for i in range(camera.Vres):
        for j in range(camera.Hres):
            ray = camera.get_ray(j, i)
            cor_pixel = Vetor(0, 0, 0)  # Cor de fundo padrão
            menor_t = float('inf')
            for obj in objetos:
                t = obj.intersect(ray.origem, ray.direcao)
                if t is not None and t < menor_t:
                    menor_t = t
                    cor_pixel = obj.cor
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
