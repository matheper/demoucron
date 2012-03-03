# -*- coding: utf-8 -*-

from defs import leGrafos
from grafos import *

#grafos = leGrafos('grafo_100.txt')
grafos = leGrafos('grafo_10.txt')

#plot grafo
#biblioteca http://networkx.lanl.gov/

from pylab import *
import networkx as nx

def plotGrafo(grafos,n=0):
    G = nx.Graph()
    for i in grafos[n].vertices:
        G.add_node(i.cod)

    for i in grafos[n].vertices:
        for j in i.arestas:
            G.add_edge(i.cod,j)
    nx.draw(G)
    show()

plotGrafo(grafos,0)
