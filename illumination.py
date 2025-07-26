from vector import Vetor
from point import Ponto
from objects import Esfera, Plano, Triangulo, MalhaT
from ray import Ray

class Luz:
    def __init__(self, posicao, intensidade):
        self.posicao = posicao
        self.intensidade = intensidade 


def phong(luzes, material, raio, normal, pontoIntersecao, objetos, recursion_index):
    IA = (30, 30, 30)  # Intensidade da luz ambiente
    KS = material.ks
    KD = material.kd
    KA = material.ka
    COEF = material.coeficienteRugosidade
    NS = material.ns
    NI = material.ni
    KT = 1 - material.ns ##facilitamos o uso de KR e KT
    OD = material.cor.normalizar() ##tem que jogar na ambiente tb
    
    ambiente = Vetor(KA.x * IA[0] * OD.x, KA.y * IA[1] * OD.y, KA.z * IA[2] * OD.z)
    difusao = Vetor(0, 0, 0)
    especular = Vetor(0, 0, 0)
    reflexiva = Vetor(0, 0, 0)
    refrativa = Vetor(0, 0, 0)
    ##necessario importar objetos[] para recursão em refletiva e refrativa
    
    for luz in luzes:
        N = normal.normalizar()
        L = (luz.posicao.__sub__(pontoIntersecao)).normalizar()
        V = (raio.origem.__sub__(pontoIntersecao)).normalizar()
        IL = luz.intensidade
        cossenoNL = max(N.produto_escalar(L), 0.0)
        reflexivaLuz = Vetor(0, 0, 0) ##tem que inicializar fora do if, infelizmente...

        difusaoLuz = Vetor(KD.x * IL.x * cossenoNL * OD.x,
                        KD.y * IL.y * cossenoNL * OD.y,
                        KD.z * IL.z * cossenoNL * OD.z)

        R = N.mult_escalar(2 * N.produto_escalar(L)).__sub__(L)
        if R.norma() != 0:
            R = R.normalizar()
        cossenoRV = max(R.produto_escalar(V), 0.0)

        especularLuz = Vetor(KS.x * IL.x * (cossenoRV ** COEF),
                        KS.y * IL.y * (cossenoRV ** COEF),
                        KS.z * IL.z * (cossenoRV ** COEF))

        #if(material.ns > 0 & recursion_index < 1): ##economizar processamento em não-refletivos ou na terceira recursao
        #  LReflexo = N.mult_escalar(2 * N.produto_escalar(L)).__sub__(L)
        #  if LReflexo.norma() != 0:
        #      pontoInt = Ponto(pontoIntersecao.x, pontoIntersecao.y, pontoIntersecao.z)
        #      raioNovo = Ray(pontoInt, LReflexo) ##ponto interseção tá saindo como vetor???
        #      menor_t = float('inf')
        #      for obj in objetos:
        #          resultado = obj.intersect(raioNovo.origem, raioNovo.direcao)
        #          if resultado is not None and resultado[0] == True:
        #              t = resultado[1]
        #              if t is not None:
        #                  if t < menor_t:
        #                      menor_t = t
        #                      reflexivaLuz = phong(luzes, resultado[4], raioNovo, resultado[2], resultado[3], objetos, recursion_index) # material = resultado[4], normal = resultado[2], pontoIntersecao = resultado[3]
        #                      recursion_index = recursion_index + 1  ##incrementa o índice de recursão
        
        refrativaLuz = Vetor(0,0,0)
        difusao = difusao.soma(difusaoLuz)
        especular = especular.soma(especularLuz)
        if (reflexivaLuz != (0,0,0)):         ##ignora a reflexão do vácuo sem skybox, opcional
          reflexiva = reflexiva.soma(reflexivaLuz)
        ##refrativa = refrativa.soma(refrativaLuz)
        
    
    iluminacao = ambiente.soma(difusao).soma(especular) ##.soma(reflexiva) ##.soma(refrativa)
    iluminacao.x = min(iluminacao.x, 255)
    iluminacao.y = min(iluminacao.y, 255)
    iluminacao.z = min(iluminacao.z, 255)
    if iluminacao.x < 10 or iluminacao.y < 10 or iluminacao.z < 10 and recursion_index < 1: ##não vamos printar todas as recursões...
        print(f"Iluminação calculada: {iluminacao.x}, {iluminacao.y}, {iluminacao.z}")
    return iluminacao

