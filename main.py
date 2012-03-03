# -*- coding: utf-8 -*-

from grafos import *
from defs import *
from demoucron import *

#import bibliotecas python
import copy

#inicia a geracao dos grafos lendo o arquivo
grafos = leGrafos( raw_input('Digite caminho do arquivo: ') )
#grafos = leGrafos('grafo_100.txt')
saida = open('saida.txt','w')

if len(grafos) > 1:
    grafos[0].escreveArquivoSaida("Foram encontrados %s grafos\n" % (len(grafos)))
else: grafos[0].escreveArquivoSaida("Foi encontrado 1 grafo\n")

for i in grafos:
    #copia o objeto grafo original
    g = copy.deepcopy(i)

    #gera a arvore
    g.lstRaizesConexas = g.gera_arvore()

    if len(g.lstRaizesConexas) > 1:
        g.escreveArquivoSaida("Foram encontradas %s componentes conexas sao elas:\n" % (len(g.lstRaizesConexas)))
    else: g.escreveArquivoSaida("Foi encontrada %s componente conexa:\n" %(len(g.lstRaizesConexas)))

    g.resetVisita()
    for i in g.lstRaizesConexas:
        g.resetVisita()
        g.escreveArvoreArquivo(i)
        g.escreveArquivoSaida("\n")

    #define low_pt, articulacoes e demarcadores
    for raiz in g.lstRaizesConexas:
        g.resetVisita()
        raiz.low_pt()
        g.resetVisita()
        raiz.Articulacao()
        g.resetVisita()
        raiz.Demarcador()

    g.resetVisita()
    g.lstRaizesBiconexas = g.lstRaizesConexas

    #biconexa
    g.resetVisita()
    for raiz in g.lstRaizesConexas:
        g.biconexa(raiz)

    if len(g.lstRaizesBiconexas) > 1:
        g.escreveArquivoSaida("Foram encontradas %s componentes biconexas sao elas:\n" % (len(g.lstRaizesBiconexas)))
    else: g.escreveArquivoSaida("Foi encontrada %s componente biconexa:\n" %(len(g.lstRaizesBiconexas)))

    for i in g.lstRaizesBiconexas:
        g.resetVisita()
        g.escreveArvoreArquivo(i)
        g.escreveArquivoSaida("\n")
    
    for i in g.lstRaizesBiconexas:
        g.resetVisita()
        g.atualizaAdjacencias()
    g.resetVisita()

#    print "\nGrafo"
#    g.resetVisita()
#    g.listaVertices()

    g.simplificar()

#    print "\n\n\nGrafo modificado\n"
#    g.resetVisita()
#    g.listaVertices()
    g.resetVisita()
    g.escreveGrafo()

    listaGrafosBiconexos = []
    for i in g.lstRaizesBiconexas:
        biconexa = Grafo(0)
        g.resetVisita()
        g.retornaBiconexa(i,biconexa)
        listaGrafosBiconexos.append(biconexa)

    for grafo in listaGrafosBiconexos:
        grafo.simplificar2()
        testePlanaridade(grafo)
