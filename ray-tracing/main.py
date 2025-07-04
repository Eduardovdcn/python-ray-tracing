import numpy as np
from point import Ponto
from vector import Vetor
from camera import Camera
from objects import Esfera, Plano, MalhaT
from obj_reader import ObjReader
from matrix import Matrix

def render_scene(camera, objetos, filename):
    """Renderiza uma cena e salva em um arquivo PPM."""
    imagem = np.zeros((camera.Vres, camera.Hres, 3), dtype=np.uint8)
    
    for i in range(camera.Vres):
        for j in range(camera.Hres):
            ray = camera.get_ray(j, i)
            cor_pixel = Vetor(20, 20, 20)  # Cor de fundo (cinza escuro)
            menor_t = float('inf')
            obj_atingido = None

            for obj in objetos:
                t = obj.intersect(ray.origem, ray.direcao)
                if t is not None and t < menor_t:
                    menor_t = t
                    obj_atingido = obj
            
            if obj_atingido:
                # Converte a cor do objeto (normalizada entre 0-1) para 0-255
                cor = obj_atingido.cor
                if max(cor.x, cor.y, cor.z) <= 1.0:
                     cor_pixel = cor.mult_escalar(255)
                else:
                     cor_pixel = cor
            
            imagem[i, j] = [int(cor_pixel.x), int(cor_pixel.y), int(cor_pixel.z)]

    with open(filename, "w") as f:
        f.write(f"P3\n{camera.Hres} {camera.Vres}\n255\n")
        for row in imagem:
            for pixel in row:
                f.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
            f.write("\n")
    print(f"Imagem renderizada e salva como '{filename}'")


def main():
    obj_path = r"C:\Users\Leo\Documents\GitHub\python-ray-tracing\inputs\icosahedron.obj"
    try:
        reader = ObjReader(obj_path)
    except FileNotFoundError:
        print(f"Erro: Arquivo .obj não encontrado em '{obj_path}'")
        print("Por favor, verifique o caminho e tente novamente.")
        return

    # Calcula o centro do icosaedro a partir dos vértices do .obj
    vertices = reader.get_vertices()
    n = len(vertices)
    centro_x = sum(v.x for v in vertices) / n
    centro_y = sum(v.y for v in vertices) / n
    centro_z = sum(v.z for v in vertices) / n
    centro = Ponto(centro_x, centro_y, centro_z)

    # Configura a câmera centralizada no objeto
    camera = Camera(
        C=Ponto(centro.x, centro.y, centro.z + 10),  # Posição afastada no eixo Z
        M=centro,                                    # Mira para o centro real do icosaedro
        Vup=Vetor(0, 1, 0),
        d=1,
        Vres=400,
        Hres=400
    )

    # --- CENA 1: OBJETO ORIGINAL ---
    print("Renderizando a cena com o objeto original...")
    malha_original = MalhaT(faces=reader.get_faces(), vertices=reader.get_vertices())
    
    objetos_originais = [malha_original]
    render_scene(camera, objetos_originais, "output_original.ppm")

    # --- CENA 2: OBJETO TRANSFORMADO ---
    print("\nRenderizando a cena com o objeto transformado...")
    
    # Cria uma nova malha para a transformação
    malha_transformada = MalhaT(faces=reader.get_faces(), vertices=reader.get_vertices())

    # Cria matrizes de transformação
    matriz_rotacao = Matrix.make_rotation_y(45) * Matrix.make_rotation_x(45)
    matriz_translacao = Matrix.make_translation(1, -0.5, 0)
    
    # Combina as transformações (escala -> rotação -> translação)
    matriz_transformacao_final = matriz_translacao * matriz_rotacao
    
    # Aplica a transformação à malha
    malha_transformada.transform(matriz_transformacao_final)

    objetos_transformados = [malha_transformada]
    render_scene(camera, objetos_transformados, "output_transformada.ppm")


if __name__ == "__main__":
    main()
