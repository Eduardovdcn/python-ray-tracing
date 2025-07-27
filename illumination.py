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
    MAX_PROFUNDIDADE = 5
    epsilon = 1e-6
    
    # Early exit se não há componente reflexiva ou excedeu profundidade
    if profundidade >= MAX_PROFUNDIDADE:
        return Vetor(0, 0, 0)
    
    # Verificar se R precisa de normalização
    if R.norma() == 0:
        return Vetor(0, 0, 0)
        
    # Gera novo raio refletido
    novoPontoIntersecao = Ponto(
        pontoIntersecao.x + N.x * epsilon,
        pontoIntersecao.y + N.y * epsilon,
        pontoIntersecao.z + N.z * epsilon
    )
    direcaoReflexao = R.normalizar()
    
    # Interseção recursiva
    resultado = intersect(novoPontoIntersecao, direcaoReflexao, objetos, profundidade + 1)
    if resultado is not None and resultado[0]:
        _, tRefletido, normalRefletido, pontoRefletido, materialRefletido = resultado
        raioReflexao = Ray(novoPontoIntersecao, direcaoReflexao)
        # Calcula iluminação recursiva no ponto de intersecção
        cor_reflexao = phong(
            luzes, materialRefletido, raioReflexao, normalRefletido, pontoRefletido, objetos, profundidade + 1
        )
        # Escala pela componente KR do material original
        return Vetor(
            KR.x * cor_reflexao.x,
            KR.y * cor_reflexao.y,
            KR.z * cor_reflexao.z
        )
    return Vetor(0, 0, 0)


def getRefracao(raio, normal, KT, pontoIntersecao, objetos, luzes, profundidade):
    MAX_PROFUNDIDADE = 5
    epsilon = 1e-6
    
    # Early exit se não há componente refrativa ou excedeu profundidade
    if profundidade >= MAX_PROFUNDIDADE:
        return Vetor(0, 0, 0)
    
    # Índices de refração (ar = 1.0, vidro ≈ 1.5)
    n1 = 1.0  # meio de origem (ar)
    n2 = 1.5  # meio de destino (material)
    ref_idx = n1 / n2
    
    N = normal.normalizar()
    I = raio.direcao.normalizar()
    
    # Calcular ângulo de incidência
    cos_i = -N.produto_escalar(I)
    
    # Lei de Snell: sin²(t) = (n1/n2)² * (1 - cos²(i))
    ref_idx_sq = ref_idx * ref_idx
    sin_t2 = ref_idx_sq * (1.0 - cos_i * cos_i)
    
    # Verificar reflexão interna total
    if sin_t2 > 1.0:
        return Vetor(0, 0, 0)  # Reflexão interna total
    
    cos_t = math.sqrt(1.0 - sin_t2)
    
    # Calcular direção refratada: T = (n1/n2) * I + ((n1/n2) * cos_i - cos_t) * N
    fator = ref_idx * cos_i - cos_t
    direcaoRefracao = I.mult_escalar(ref_idx).soma(N.mult_escalar(fator))
    
    # Verificar se a direção é válida
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
    resultado = intersect(novoPontoIntersecao, direcaoRefracao, objetos, profundidade + 1)
    if resultado is not None and resultado[0]:
        _, tRefratado, normalRefratado, pontoRefratado, materialRefratado = resultado
        raioRefracao = Ray(novoPontoIntersecao, direcaoRefracao)
        # Calcula iluminação recursiva no ponto de intersecção
        cor_refracao = phong(
            luzes, materialRefratado, raioRefracao, normalRefratado, pontoRefratado, objetos, profundidade + 1
        )
        # Escala pela componente KT do material original
        return Vetor(
            KT * cor_refracao.x,
            KT * cor_refracao.y,
            KT * cor_refracao.z
        )
    return Vetor(0, 0, 0)


def intersect(origem, direcao, objetos, profundidade=0):
    epsilon = 1e-6
    menor_t = float('inf')
    resultado_mais_proximo = None
    
    for obj in objetos:
        resultado = obj.intersect(origem, direcao)
        if resultado is not None and resultado[0]:
            t = resultado[1]
            # Otimização: verificar condições em ordem de probabilidade
            if t is not None and t > epsilon:
                if t < menor_t:
                    menor_t = t
                    resultado_mais_proximo = resultado
    return resultado_mais_proximo


def phong(luzes, material, raio, normal, pontoIntersecao, objetos, profundidade):
    # Limite de profundidade para evitar recursão infinita
    MAX_PROFUNDIDADE = 2
    if profundidade > MAX_PROFUNDIDADE:
        return Vetor(0, 0, 0)
    
    # Parâmetros de iluminação
    IA = (30, 30, 30)  # luz ambiente
    KS = material.ks
    KD = material.kd
    KA = material.ka
    COEF = material.coeficienteRugosidade
    KR = material.kr
    KT = material.kt  # Componente de transmissão/refração
    OD = material.cor.normalizar()
    
    # Pre-calcular vetores que não mudam no loop
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
        # Cache do produto escalar para evitar recálculo
        dot_NL = N.produto_escalar(L)
        R = N.mult_escalar(2 * dot_NL).__sub__(L)
        
        difusao = difusao.soma(getDifusao(N, L, luz, KD, OD))
        especular = especular.soma(getEspecular(V, R, luz, KS, COEF))
    
    # Componente reflexiva (early exit se não há reflexão)
    reflexiva = Vetor(0, 0, 0)
    if KR.x > 0 or KR.y > 0 or KR.z > 0:
        I = raio.direcao.normalizar()
        # Simplificado: R = I - 2(I·N)N
        dot_IN = I.produto_escalar(N)
        R_reflexao = I.__sub__(N.mult_escalar(2 * dot_IN))
        reflexiva = getReflexao(N, R_reflexao, KR, pontoIntersecao, objetos, luzes, profundidade)
    
    # Componente refrativa (early exit se não há refração)
    refrativa = Vetor(0, 0, 0)
    # if KT > 0:
    #     refrativa = getRefracao(raio, N, KT, pontoIntersecao, objetos, luzes, profundidade)
    
    # Combinação final
    iluminacao = ambiente.soma(difusao).soma(especular).soma(reflexiva).soma(refrativa)
    
    # Clamp dos valores para evitar overflow
    iluminacao.x = min(max(iluminacao.x, 0), 255)
    iluminacao.y = min(max(iluminacao.y, 0), 255)
    iluminacao.z = min(max(iluminacao.z, 0), 255)
    
    return iluminacao
