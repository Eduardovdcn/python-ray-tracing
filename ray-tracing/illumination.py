from vector import Vetor

class Luz:
    def __init__(self, posicao, intensidade):
        self.posicao = posicao
        self.intensidade = intensidade 


def phong(luzes, material, raio, normal, pontoIntersecao):
    IA = (20, 20, 20)  # Intensidade da luz ambiente
    KS = material.ks
    KD = material.kd
    KA = material.ka
    COEF = material.coeficienteRugosidade

    ambiente = Vetor(KA.x * IA[0], KA.y * IA[1], KA.z * IA[2])
    difusao = Vetor(0, 0, 0)
    especular = Vetor(0, 0, 0)

    for luz in luzes:
        N = normal.normalizar()
        L = (luz.posicao.__sub__(pontoIntersecao)).normalizar()
        V = (raio.origem.__sub__(pontoIntersecao)).normalizar()
        OD = material.cor.normalizar()
        IL = luz.intensidade
        cossenoNL = max(N.produto_escalar(L), 0.0)

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

        difusao = difusao.soma(difusaoLuz)
        especular = especular.soma(especularLuz)
    
    iluminacao = ambiente.soma(difusao).soma(especular)
    iluminacao.x = min(iluminacao.x, 255)
    iluminacao.y = min(iluminacao.y, 255)
    iluminacao.z = min(iluminacao.z, 255)
    if iluminacao.x < 10 or iluminacao.y < 10 or iluminacao.z < 10:
        print(f"Iluminação calculada: {iluminacao.x}, {iluminacao.y}, {iluminacao.z}")
    return iluminacao

