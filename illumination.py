import math
from vector import Vetor
from point import Ponto
from objects import Esfera, Plano, Triangulo, MalhaT
from ray import Ray

class Luz:
    def __init__(self, posicao, intensidade):
        self.posicao = posicao
        self.intensidade = intensidade 


def getDifusao(N, L, luz, KD, OD):
    cossenoNL = max(N.produto_escalar(L), 0.0)
    # Otimização: evitar multiplicações desnecessárias quando cossenoNL = 0
    if cossenoNL == 0.0:
        return Vetor(0, 0, 0)
    return Vetor(KD.x * luz.intensidade.x * cossenoNL * OD.x,
                 KD.y * luz.intensidade.y * cossenoNL * OD.y,
                 KD.z * luz.intensidade.z * cossenoNL * OD.z)


def getEspecular(V, R, luz, KS, COEF):
    cossenoRV = max(R.produto_escalar(V), 0.0)
    # Otimização: early exit para especular
    if cossenoRV == 0.0:
        return Vetor(0, 0, 0)
    cossenoRV_pow = cossenoRV ** COEF
    return Vetor(KS.x * luz.intensidade.x * cossenoRV_pow,
                 KS.y * luz.intensidade.y * cossenoRV_pow,
                 KS.z * luz.intensidade.z * cossenoRV_pow)


def getReflexao(N, R, KR, pontoIntersecao, objetos, luzes, profundidade):
    MAX_PROFUNDIDADE = 3
    epsilon = 1e-6
    #se não há componente reflexiva ou excedeu profundidade
    if profundidade >= MAX_PROFUNDIDADE:
        return Vetor(0, 0, 0)
    
    # Verificar se R precisa de normalização
    if R.norma() == 0:
        return Vetor(0, 0, 0)
        
    novoPontoIntersecao = Ponto(
        pontoIntersecao.x + N.x * epsilon,
        pontoIntersecao.y + N.y * epsilon,
        pontoIntersecao.z + N.z * epsilon
    )
    direcaoReflexao = R.normalizar()
    
    # Interseção recursiva
    resultado = intersect(novoPontoIntersecao, direcaoReflexao, objetos)
    if resultado is not None and resultado[0]:
        _, tRefletido, normalRefletido, pontoRefletido, materialRefletido = resultado
        raioReflexao = Ray(novoPontoIntersecao, direcaoReflexao)
        # Calcula iluminação recursiva no ponto de intersecção
        corReflexao = phong(
            luzes, materialRefletido, raioReflexao, normalRefletido, pontoRefletido, objetos, profundidade + 1
        )
        
        return Vetor(
            KR.x * corReflexao.x,
            KR.y * corReflexao.y,
            KR.z * corReflexao.z
        )
    return Vetor(0, 0, 0)


def getRefracao(raio, normal, KT, pontoIntersecao, objetos, luzes, profundidade):
    MAX_PROFUNDIDADE = 3
    epsilon = 1e-6
    
    # Se não há componente refrativa ou excedeu profundidade
    if profundidade >= MAX_PROFUNDIDADE or KT <= 0:
        return Vetor(0, 0, 0)
    
    # Índices de refração (ar = 1.0, vidro ≈ 1.5)
    N1 = 1.0  # meio de origem (ar)
    N2 = 1.5  # meio de destino (material)
    indiceRefracao = N1 / N2

    N = normal.normalizar()
    I = raio.direcao.normalizar()
    cosNI = -N.produto_escalar(I)   # Ângulo de incidência

    # Lei de Snell: sin²(θt) = (n1/n2)² * sin²(θi)
    # sin²(θi) = 1 - cos²(θi)
    sinT2 = (indiceRefracao ** 2) * (1.0 - (cosNI ** 2))

    # Verificar reflexão interna total
    if sinT2 > 1.0:
        return Vetor(0, 0, 0)

    cosT = math.sqrt(1.0 - sinT2)

    # Calcular direção refratada
    # T = η*I + (η*cos_i - cos_t)*N
    fator = (indiceRefracao * cosNI) - cosT
    direcaoRefracao = I.mult_escalar(indiceRefracao).soma(N.mult_escalar(fator))

    if direcaoRefracao.norma() == 0:
        return Vetor(0, 0, 0)
    
    # Gera novo raio refratado (ligeiramente dentro do objeto)
    novoPontoIntersecao = Ponto(
        pontoIntersecao.x - N.x * epsilon,
        pontoIntersecao.y - N.y * epsilon,
        pontoIntersecao.z - N.z * epsilon
    )
    direcaoRefracao = direcaoRefracao.normalizar()
    
    # Interseção recursiva
    resultado = intersect(novoPontoIntersecao, direcaoRefracao, objetos)
    if resultado is not None and resultado[0]:
        _, tRefratado, normalRefratado, pontoRefratado, materialRefratado = resultado
        raioRefracao = Ray(novoPontoIntersecao, direcaoRefracao)

        corRefracao = phong(
            luzes, materialRefratado, raioRefracao, normalRefratado, pontoRefratado, objetos, profundidade + 1
        )
        # Escala pela componente KT do material original
        return Vetor(
            KT * corRefracao.x,
            KT * corRefracao.y,
            KT * corRefracao.z
        )
    return Vetor(0, 0, 0)


def intersect(origem, direcao, objetos):
    epsilon = 1e-6
    menor_t = float('inf')
    resultado_mais_proximo = None
    
    for obj in objetos:
        resultado = obj.intersect(origem, direcao)
        if resultado is not None and resultado[0]:
            t = resultado[1]
            if t is not None and t > epsilon:
                if t < menor_t:
                    menor_t = t
                    resultado_mais_proximo = resultado
    return resultado_mais_proximo


def phong(luzes, material, raio, normal, pontoIntersecao, objetos, profundidade):
    # Limite de profundidade para evitar recursão infinita
    MAX_PROFUNDIDADE = 3
    if profundidade > MAX_PROFUNDIDADE:
        return Vetor(0, 0, 0)
    
    # Parâmetros de iluminação
    IA = (30, 30, 30)  # luz ambiente
    KS = material.ks
    KD = material.kd
    KA = material.ka
    COEF = material.coeficienteRugosidade
    KR = material.kr
    KT = material.kt  
    OD = material.cor.normalizar()
    N = normal.normalizar()
    V = (raio.origem.__sub__(pontoIntersecao)).normalizar()
    
    # Componente ambiente
    ambiente = Vetor(KA.x * IA[0] * OD.x,
                     KA.y * IA[1] * OD.y,
                     KA.z * IA[2] * OD.z)
    difusao = Vetor(0, 0, 0)
    especular = Vetor(0, 0, 0)

    # Iluminação direta
    for luz in luzes:
        L = (luz.posicao.__sub__(pontoIntersecao)).normalizar()
        R = N.mult_escalar(2 * N.produto_escalar(L)).__sub__(L)
        
        difusao = difusao.soma(getDifusao(N, L, luz, KD, OD))
        especular = especular.soma(getEspecular(V, R, luz, KS, COEF))
    
    # Componente reflexiva 
    reflexiva = Vetor(0, 0, 0)
    if KR.x > 0 or KR.y > 0 or KR.z > 0:
        I = raio.direcao.normalizar()
        R_reflexao = I.__sub__(N.mult_escalar(2 * I.produto_escalar(N))) #R = I - 2(I·N)N
        reflexiva = getReflexao(N, R_reflexao, KR, pontoIntersecao, objetos, luzes, profundidade)
    
    # Componente refrativa 
    refrativa = Vetor(0, 0, 0)
    # if KT > 0:
    #     refrativa = getRefracao(raio, N, KT, pontoIntersecao, objetos, luzes, profundidade)
    
    # Combinação final
    iluminacao = ambiente.soma(difusao).soma(especular).soma(reflexiva).soma(refrativa)
    
    iluminacao.x = min(max(iluminacao.x, 0), 255)
    iluminacao.y = min(max(iluminacao.y, 0), 255)
    iluminacao.z = min(max(iluminacao.z, 0), 255)
    
    return iluminacao
