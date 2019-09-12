#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
'''
Converte Labiritno em um grafo.
'''
from numpy import array, where
import networkx as nx


class LabGrafo:
    def __init__(self, img):
        self._img = img
        self._nos, self._nome_nos, self._grafo = self._criar_grafo()
        self._caminho = None

    def _criar_grafo(self):
        '''
        Gera grafo a partir da matriz imagem, que representa o labirinto.
        Valores iguais a 0 indicam muro.
        '''
        caminhos = where(self._img != 0)
        nos = list(zip(caminhos[0], caminhos[1]))
        nnos = len(nos)
        nos = array(nos)
        vertices = LabGrafo.encontrar_vertices(nos)
        grafo = nx.Graph()
        nome_nos = list(range(nnos - 1))
        grafo.add_nodes_from(nome_nos)
        grafo.add_edges_from(vertices)
        return nos, nome_nos, grafo

    @property
    def caminho(self):
        return self._caminho

    @property
    def nos(self):
        '''Retorna os nomes dos nós.'''
        return self._nome_nos

    @property
    def nos_ij(self):
        '''
        Retorna o vetor contendo o par que relaciona posição com nó
        na matriz da imagem de entrada.
        '''
        return self._nos

    @property
    def grafo(self):
        '''
        Retorna o grafo que representa os caminhos possíveis no labirinto.
        '''
        return self._grafo

    @staticmethod
    def encontrar_vertices(nos):
        """
        Encontra os vertices nas regiões de movimentos permitidos entre os nós.
        """
        n = nos.shape[0]
        vertices = []
        for i in range(0, n - 1):
            for j in range(i, n):
                if abs(nos[i, 0] - nos[j, 0]) > 1:
                    break
                elif abs(nos[i, 0] - nos[j, 0]) == 1 and \
                     abs(nos[i, 1] - nos[j, 1]) == 0:
                     vertices.append([i, j])
                elif abs(nos[i, 0] - nos[j, 0]) == 0 and \
                     abs(nos[i, 1] - nos[j, 1]) == 1:
                     vertices.append([i, j])
        return array(vertices)
