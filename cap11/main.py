from numpy import load, save, where, array, random, hsplit, concatenate

import matplotlib.pyplot as plt

from pygenec.populacao import Populacao
from pygenec.selecao.torneio import Torneio
from pygenec.cruzamento.embaralhamento import Embaralhamento
from pygenec.mutacao.sequenciareversa import SequenciaReversa
from pygenec.evolucao import Evolucao
from pygenec import binarray2int

from gerarlabirinto import GerarLabirinto
from labgrafo import LabGrafo

car_salv = input("Carregar ou Salvar [c/s]: ")
filname = "./labirinto_grap.npy"

if car_salv == "s":
    dimensao = int(input("Qual a dimensão do Labirinto? "))
    lab = GerarLabirinto(dimensao)
    mapa = lab.mapa
    save(filname, mapa)
else:
    mapa = load(filname)


goal = (mapa.shape[0]- 2, mapa.shape[1]-5)
startpoint = (1, 1)


labgrafo = LabGrafo(mapa)


tamanho_populacao = 50
cromossomos = len(labgrafo.nos)
tamanho = int(0.1 * tamanho_populacao) if tamanho_populacao > 10 else 5
bits = 4
genes = bits * cromossomos
pmut = 0.1
pcruz = 0.6
epidemia = 50
elitista = True

def valores(populacao):
    bx = hsplit(populacao, cromossomos)
    const = 2 ** bits - 1
    const = 100 / const
    x = [const * binarray2int(xi) for xi in bx]
    x = concatenate(x).T.astype(int)
    return x

def avaliacao(populacao):
    x = valores(populacao)
    n = len(populacao)

    def steps(k):
        individuo = x[k, :]
        t =  labgrafo.avaliacao(individuo, startpoint, goal, upcaminho=False)
        return t
    peso = array([steps(k) for k in range(n)])
    return peso

populacao = Populacao(avaliacao,
                           genes,
                           tamanho_populacao)

selecao = Torneio(populacao, tamanho=tamanho)
cruzamento = Embaralhamento(tamanho_populacao)
mutacao = SequenciaReversa(pmut=pmut)

evolucao = Evolucao(populacao,
                         selecao,
                         cruzamento,
                         mutacao)

evolucao.nsele = tamanho
evolucao.pcruz = pcruz
evolucao.manter_melhor = elitista
evolucao.epidemia = epidemia

for i in range(200):
    vmin, vmax = evolucao.evoluir()

    print(evolucao.geracao, vmax, vmin)
    if evolucao.geracao % epidemia == 0:
        x = valores(populacao.populacao)
        individuo = x[-1, :]
        print("Gerando Video")
        fnome = "./videos/lab_{}.mp4".format(evolucao.geracao)
        labgrafo.plot(individuo, startpoint, goal, geracao=evolucao.geracao,
                      save_file=fnome)
    if vmax >=  0.002:
        break

x = valores(populacao.populacao)
individuo = x[-1, :]
print("Gerando Video")
fnome = "./videos/lab_{}.mp4".format(evolucao.geracao)
labgrafo.plot(individuo, startpoint, goal, geracao=evolucao.geracao, save_file=fnome)
