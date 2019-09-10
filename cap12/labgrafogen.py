#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
'''
Estende a classe de representação de labirinto em grafo para adicionar
avaliação de indivíduo vindo do algoritmo genético.
'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from numpy import where
from labgrafo import LabGrafo

class LabGrafoGen(LabGrafo):
    '''
    Estende a classe de representação de labirinto em grafo para adicionar
    avaliação de indivíduo vindo do algoritmo genético.
    '''
    def __init__(self, img):
        super(LabGrafoGen, self).__init__(img)

    def no_correspondente(self, pos):
        tmp = self.nos_ij == pos
        cond = (tmp[:,0] == True) & (tmp[:,1] == True)
        nome_no = self.nos[where(cond)[0][0]]
        return nome_no

    def avaliacao(self, individuo, inicio, meta, upcaminho=True):
        '''
        Dado um indivíduo, verifica se o mesmo representa uma solução
        para o labirinto.
        '''
        partida = self.no_correspondente(inicio)
        fim = self.no_correspondente(meta)
        caminho = [partida]
        atual = partida
        chegou = False
        total = 0
        i0 = 0

        while True:
            possibilidades = {ng for ng in  self.grafo.neighbors(atual)}
            possibilidades = list(possibilidades - set(caminho))
            nposs = len(possibilidades)
            if nposs > 1:
                genes = individuo[i0: i0 + nposs]
                escolhido = possibilidades[where(genes == max(genes))[0][0]]
                i0 += nposs
                caminho.append(escolhido)
                atual = escolhido
            elif nposs == 1:
                caminho += possibilidades
                atual = possibilidades[0]
            else:
                break

            if atual == fim:
                chegou = True
                break

        if chegou is False:
            total += len(caminho) ** 2.0  / 1e11
        else:
            total = 1.0 / len(caminho)

        if upcaminho is True:
            self.caminho = caminho

        return total

    def plot(self, individuo, inicio, meta, geracao=None, save_file=None, interval=100):
        '''
        Gera um vídeo do percurso definido pelos genes de um dado indivíduo.
        '''
        self.avaliacao(individuo, inicio, meta)

        i_fim, j_fim = meta

        fig, ax = plt.subplots()
        img = self._img.copy()

        img[i_fim, j_fim] = 200
        img[img == 0] = 255
        img[img == -1] = 0
        img[inicio] = 0

        im = ax.imshow(img, animated=True, interpolation='none', aspect='auto')

        def updatefig(frame):
            img = self._img.copy()
            img[inicio] = 255
            img[i_fim, j_fim] = 200
            atl = self._nos[self.caminho[frame]]
            img[atl[0], atl[1]] = 100
            if geracao is not None:
                label = "Geração {}".format(geracao)
                ax.set_title(label)
            im.set_array(img)
            return im,

        ani = FuncAnimation(fig,
                            updatefig,
                            frames=len(self.caminho),
                            interval=interval,
                            blit=False)

        if save_file is not None:
            Writer = writers['ffmpeg']
            writer = Writer(fps=29, metadata=dict(artist='Me'), bitrate=1800)
            ani.save(save_file, writer=writer)
        else:
            plt.show()
