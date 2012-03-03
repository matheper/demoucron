# -*- coding: utf-8 -*-

from grafos import *
import copy


def leGrafos(arquivo):
    """Retorna lista de grafos
    lista = leGrafos(diretorio\arquivo.ext)"""

    G = []
    try:
        arquivo = open(arquivo,'r')

        try:
            grafos = int(arquivo.readline())

            for i in range(grafos):
                nVertices = int(arquivo.readline())
                G.append(Grafo(nVertices))

                for j in range(nVertices):
                    tuplaLine = arquivo.readline() #'3 5 7 16\r\n'
                    tuplaLine = tuplaLine.partition(' ') #('3', ' ', '1 3 12\r\n'), partition(retorna uma tupla())
                    grau = int(tuplaLine[0]) #3
                    vertices = map(int,(tuplaLine[2].rstrip()).split(' ')) #[5,6,16], map(transforma cada elemento da lista em INT)
                    G[i].adicionaVertice(j+1,grau,vertices)

            arquivo.close()
        except:
            print 'Formato do Arquivo invalido!'

    except:
        print 'Arquivo ou diretorio invalido!'
   
    #modifica a lista aresta para uma lista de objetos vertices
    for grafo in G:
        for vertice in grafo.vertices:
            list_arestas = []
            for aresta in vertice.arestas:
                list_arestas.append(grafo.vertices[aresta-1])

            vertice.arestas = list_arestas

    return G
