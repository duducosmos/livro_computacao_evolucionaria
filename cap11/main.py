from numpy import load, save
import matplotlib.pyplot as plt

from pygenec.populacao import Populacao
from pygenec.selecao.torneio import Torneio
from pygenec.cruzamento.embaralhamento import Embaralhamento
from pygenec.mutacao.sequenciareversa import SequenciaReversa
from pygenec.evolucao import Evolucao

from gerarlabirinto import GerarLabirinto
from labgrafo import LabGrafo

car_salv = input("Carregar ou Salvar [c/s]: ")
filname = "./labirinto_grap.npy"

if car_salv == "s":
    dimensao = int(input("Qual a dimensão do Labirinto? "))
    lab = GerarLabirinto(dimensao)
    tmp = lab.mapa

    goal = (tmp.shape[0]- 2, tmp.shape[1]-5)
    startpoint = (1, 1)


    tmp[goal] = 150
    tmp[startpoint] = 100

    plt.imshow(tmp)
    plt.show()
