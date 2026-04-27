
#Importação da biblioteca random para geração de dados aleatórios
import random
#-----------------------------------------------------
#Variáveis constantes do código
#Qualquer alteração ira mudar completamente o código 
totalModulos = 7

tiposEPrefixos = [
    ("Habitacao",      "HAB"),
    ("Energia",        "ENE"),
    ("Laboratorio",    "LAB"),
    ("Logistica",      "LOG"),
    ("Suporte_Medico", "MED"),
]

ventoMax        = 80
chanceTempestade = 0.15

combMinimo      = 15
critEmergencia  = 9

faixaPrioridade  = (1, 5)
faixaCombustivel = (3, 95)
faixaMassa       = (5000, 16000)
faixaCriticidade = (1, 10)
faixaHora        = (6, 20)
chanceSensores   = 0.80
chancePista      = 0.85

faixaAltitude   = (8000, 12000)
faixaVelocidade = (40, 70)
velocidadeRetro = 2
gravidadeMarte  = 3.72
altitudeRetro   = 600
#-----------------------------------------------------
# Etapa Criação de Modulo:
# Criação de Módulo sem repetição de nome:
def proximoNome(prefixo, contadores):
    contadores[prefixo] = contadores.get(prefixo, 0) + 1
    return f"{prefixo}-{contadores[prefixo]:02d}"

# Dicionário de módulo com todos os atributos: 
# Nome, tipo, prioridade etc.
def criarModulo(nome, tipo):
    return {
        "nome"        : nome,
        "tipo"        : tipo,
        "prioridade"  : random.randint(*faixaPrioridade),
        "combustivel" : random.randint(*faixaCombustivel),
        "massaKg"     : random.randint(*faixaMassa),
        "criticidade" : random.randint(*faixaCriticidade),
        "horaChegada" : random.randint(*faixaHora),
        "sensoresOk"  : random.random() < chanceSensores,
        "pistaLivre"  : random.random() < chancePista,
    }

# Monta a fila, essa função garante que pelo menos um módulo de cada tipo exista.
def gerarFila(total):
    fila = []
    contadores = {}

    tipos = list(tiposEPrefixos)
    random.shuffle(tipos)
    #ramdom.shuffle: embaralha cada módulo para cada execução não ter a mesma ordem
    for tipo, prefixo in tipos:
        fila.append(criarModulo(proximoNome(prefixo, contadores), tipo))

    while len(fila) < total:
        tipo, prefixo = random.choice(tiposEPrefixos)
        fila.append(criarModulo(proximoNome(prefixo, contadores), tipo))

    return fila

#-----------------------------------------------------
#Etapa de Busca:
#buscarExtremo: percorre a fila e trás o menor valor ou maior valor encontrado
def buscarExtremo(fila, campo, menor):
    if not fila:
        return None
    resultado = fila[0]
    for m in fila[1:]:
        if (menor and m[campo] < resultado[campo]) or \
           (not menor and m[campo] > resultado[campo]):
            resultado = m
    return resultado


def menorCombustivel(fila):
    return buscarExtremo(fila, "combustivel", menor=True)


def maisUrgente(fila):
    return buscarExtremo(fila, "prioridade", menor=True)

#retorna cada módulo e separa por tipo
def porTipo(fila, tipo):
    return [m for m in fila if m["tipo"] == tipo]

#-----------------------------------------------------
# Etapa de Ordenação:
# cedePosição: caso o item possua maior prioridade ele assume a posição, caso tenha um empate na prioridade assume a posição quem possuer menor combustivel para o pouso
def cedePosicao(esq, dir):
    if esq["prioridade"] != dir["prioridade"]:
        return esq["prioridade"] > dir["prioridade"]
    return esq["combustivel"] > dir["combustivel"]

# OrdenarPorUgencia: aplica o insertion sort e devolve uma lista sem modificar a lista original
def ordenarPorUrgencia(fila):
    lista = list(fila)
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and cedePosicao(lista[j], atual):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista

#-----------------------------------------------------
# Etapa de Autorização de Pouso:
# sortearAtmosfera: define aleatoriamente caso tenha tempestade e a força do vento
def sortearAtmosfera():
    vento = random.randint(10, 110)
    tempestade = random.random() < chanceTempestade
    return vento, tempestade

# atmosferaOk: retorna True se o vento estiver dentro do limite e não houver tempestade
def atmosferaOk(vento, tempestade):
    return vento < ventoMax and not tempestade

#ehEmergencia: verifica se o módulo pode pousar com combustivel abaixo do mínimo e com a criticidade alta
def ehEmergencia(modulo):
    combCritico = modulo["combustivel"] < combMinimo
    cargaVital  = modulo["criticidade"] >= critEmergencia
    return combCritico and cargaVital

# motivoBloqueio: identifica o primeiro problema encontrado e retorna o motivo do bloqueio
# a ordem importa — atmosfera é verificada antes da pista, pista antes dos sensores etc.
def motivoBloqueio(modulo, atmOk):
    if not atmOk:
        return "Bloqueado - condições atmosferica muito forte"
    if not modulo["pistaLivre"]:
        return "Bloqueado - pista de pouso não está disponível"
    if not modulo["sensoresOk"]:
        return "Bloqueado - sensores com defeito"
    return "Bloqueado - combustivel abaixo do minimo"


# autorizarPouso: decide se o módulo pode pousar ou não
# verifica primeiro as condições normais, depois tenta o pouso de emergência
# retorna uma tupla (autorizado, motivo)
def autorizarPouso(modulo):
    vento, tempestade = sortearAtmosfera()
    atm = atmosferaOk(vento, tempestade)

    print(f"    [Atmosfera] Vento: {vento} km/h  |  Tempestade: {'SIM' if tempestade else 'NAO'}")

    combOk  = modulo["combustivel"] >= combMinimo
    normal  = combOk and modulo["sensoresOk"] and modulo["pistaLivre"] and atm

    if normal:
        return True, "Autorizado - condicoes normais"

    if ehEmergencia(modulo) and modulo["pistaLivre"] and atm:
        return True, "EMERGENCIA - combustivel critico com carga vital"

    return False, motivoBloqueio(modulo, atm)
#-----------------------------------------------------
#Etapa de Descida:
# calcularTRetro: simula a queda segundo a segundo até atingir 600m
# retorna o instante exato em que os retrofoguetes devem ser acionados
def calcularTRetro(h0, v0, g):
    for t in range(1, 10000):
        h = h0 - v0 * t - 0.5 * g * t ** 2
        if h <= altitudeRetro:
            return t
    return None


# parametrosDescida: sorteia altitude e velocidade inicial
def parametrosDescida():
    h0 = random.randint(*faixaAltitude)
    v0 = random.randint(*faixaVelocidade)
    g  = gravidadeMarte
    vf = velocidadeRetro
    tRetro = calcularTRetro(h0, v0, g)
    return {
        "h0"    : h0,
        "v0"    : v0,
        "tRetro": tRetro,
        "vf"    : vf,
        "g"     : g,
    }

# calcularAltitude: retorna a altitude do módulo
def calcularAltitude(t, p):
    h0     = p["h0"]
    v0     = p["v0"]
    g      = p["g"]
    tRetro = p["tRetro"]
    vf     = p["vf"]

    if t <= tRetro:
        h = h0 - v0 * t - 0.5 * g * t ** 2
    else:
        hRetro = h0 - v0 * tRetro - 0.5 * g * tRetro ** 2
        h = hRetro - vf * (t - tRetro)

    return max(0.0, h)


def tempoDePouso(p):
    for t in range(10000):
        if calcularAltitude(t, p) <= 0:
            return t
    return None


def simularDescida(nome):
    p      = parametrosDescida()
    tRetro = p["tRetro"]
    passo  = tRetro // 4

    print(f"\n    --- Descida de [{nome}] ---")
    print(f"    h0={p['h0']}m  v0={p['v0']}m/s  tRetro={tRetro}s  vf={p['vf']}m/s")
    print(f"    {'Tempo(s)':<10} {'Altitude(m)':<13} Fase")
    print(f"    {'-' * 38}")

    instantes = [passo * i for i in range(5)] + [tRetro + passo * i for i in range(1, 4)]
    alertaEmitido = False

    for t in instantes:
        h    = calcularAltitude(t, p)
        fase = "Balistica" if t <= tRetro else "Retrofoguetes"

        if h <= altitudeRetro and not alertaEmitido:
            print(f"    *** ALERTA: altitude <= {altitudeRetro}m — retrofoguetes acionados em t={t}s ***")
            alertaEmitido = True

        print(f"    {t:<10} {h:<13.1f} {fase}")

    tTotal  = tempoDePouso(p)
    hRetro  = calcularAltitude(tRetro, p)

    print(f"    Retrofoguetes em t={tRetro}s (altitude={hRetro:.0f}m)")

    if tTotal:
        print(f"    Pouso estimado em {tTotal}s ({tTotal / 60:.1f} min)")
    else:
        print("    AVISO: simulacao nao possui dados corretos.")

#-----------------------------------------------------
# Função de dados de saída:

def separador(titulo):
    print("\n" + "=" * 62)
    print(f"  {titulo}")
    print("=" * 62)


def exibirModulo(modulo, prefixo="  "):
    print(
        f"{prefixo}[{modulo['nome']}]"
        f"  Tipo: {modulo['tipo']:<15}"
        f"  Prior: {modulo['prioridade']}"
        f"  Comb: {modulo['combustivel']:>3}%"
        f"  Massa: {modulo['massaKg']:>6}kg"
        f"  Crit: {modulo['criticidade']:>2}"
    )


def exibirLista(modulos, prefixo):
    for m in modulos:
        exibirModulo(m, prefixo)

# Simulação da Missão
def etapaFilaInicial(fila):
    separador("Fila Inicial")
    exibirLista(fila, "  >> ")


def etapaBuscas(fila):
    separador("Busca nas Filas:")

    print("\n  Modulo com MENOR combustivel:")
    exibirModulo(menorCombustivel(fila), "  !! ")

    print("\n  Modulo de MAIOR prioridade:")
    exibirModulo(maisUrgente(fila), "  !! ")

    tipo = random.choice([t for t, _ in tiposEPrefixos])
    encontrados = porTipo(fila, tipo)

    print(f"\n  Modulos do tipo '{tipo}' ({len(encontrados)} encontrado(s)):")
    if not encontrados:
        print("  -- Nenhum modulo deste tipo na fila.")
    else:
        exibirLista(encontrados, "  -- ")


def etapaOrdenacao(fila):
    separador("Ordenação da Fila")

    ordenada = ordenarPorUrgencia(fila)

    for i, m in enumerate(ordenada, start=1):
        exibirModulo(m, f"  {i}. ")

    return ordenada


def etapaPousos(fila):
    separador("AUTORIZACAO E DESCIDA DOS MODULOS")

    pousados   = []
    bloqueados = []
    alertas    = []

    while fila:
        modulo = fila.pop(0)

        print(f"\n  Analisando: [{modulo['nome']}]")
        print(f"    Combustivel : {modulo['combustivel']}%")
        print(f"    Sensores OK : {modulo['sensoresOk']}")
        print(f"    Pista Livre : {modulo['pistaLivre']}")
        print(f"    Criticidade : {modulo['criticidade']}")

        autorizado, motivo = autorizarPouso(modulo)

        if autorizado:
            print(f"    Resultado   : OK  {motivo}")
            pousados.append(modulo)
            simularDescida(modulo["nome"])
        else:
            print(f"    Resultado   : XX  {motivo}")
            bloqueados.append(modulo)
            alertas.append(f"ALERTA [{modulo['nome']}]: {motivo}")

    return pousados, bloqueados, alertas


def etapaResultado(pousados, bloqueados):
    separador("Resultado Final")

    print(f"\n  Modulos pousado com sucesso: {len(pousados)}")
    exibirLista(pousados, "  OK ")

    print(f"\n  Modulos Bloqueado: {len(bloqueados)}")
    exibirLista(bloqueados, "  XX ")


def etapaAlertas(alertas):
    separador("Alertas")

    if not alertas:
        print("\n  Nenhum alerta gerado.")
        return

    while alertas:
        print(f"  >> {alertas.pop()}")


def simularMissao():
    separador("MGPEB - Aurora Siger")
    print("  Sistema de Gerenciamento de Pouso")
    print(f"  Simulacao com {totalModulos} modulos gerados aleatoriamente")

    fila = gerarFila(totalModulos)

    etapaFilaInicial(fila)
    etapaBuscas(fila)

    fila = etapaOrdenacao(fila)

    pousados, bloqueados, alertas = etapaPousos(fila)

    etapaResultado(pousados, bloqueados)
    etapaAlertas(alertas)

    separador("Fim da Simulação")
    print()

# Executor Principal para a simulação.
if __name__ == "__main__":
    simularMissao()