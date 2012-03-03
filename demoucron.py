# -*- coding: utf-8 -*-
from grafos import *
from vertice import *
from peca import *

def testePlanaridade(grafo):
    grafo.resetVisita()
    cont = grafo.contaArestas()
    grafo.resetVisita()
    
    if (cont < 9 or len(grafo.vertices) < 5):
        print ("Grafo Planar, arestas= %s, vertices= %s"%(cont,len(grafo.vertices)))
        return grafo.planar
    if (cont > 3*len(grafo.vertices)-6):
        print ("Grafo nao planar, arestas= %s, vertices= %s"%(cont,len(grafo.vertices)))
        grafo.planar = 0
        return grafo.planar
    demoucron(grafo)


def demoucron(grafo):
    faces = []
    
    print "Demoucron"
    grafo.resetVisita()
    condicao = grafo.contaArestas()- len(grafo.vertices) + 2
    grafo.resetVisita()
    #encontra ciclo C em G (1,2,3)
    grafoNovo = montaCiclo(grafo)
    grafoNovo.resetVisita()
    print "Ciclo Inicial"
    grafoNovo.listaVertices(1)
    grafoNovo.resetVisita()
    #cria duas primeiras faces (4)
    faces.append(grafoNovo.encontraCiclo())
    face1 = []
    for face in faces[0]:
        face1.append(face)
    faces.append(face1)
    #(5)
    planar = 1
    sair = 0
    #(6)
    while planar and not sair:

        print "\n\nFACES\n\n"
        i = 0
        for face in faces:
            i += 1
            print "Face %s" %i
            for vertice in face:
                print vertice.cod
        
        #(6.2)
        pecas = encontraPeca(grafo)

##        print "\n\nPECAS"
##        i = 0
        for peca in pecas:
##            i += 1
##            print "Peca %s" %i
##            peca.listaVertices(1)
##            peca.resetVisita()
##            print "Contatos Peca %s"%i
##            for pontoContato in peca.pontosContato:
##                print pontoContato.cod
        #(6.3)
            peca.encontraFaces(faces)

##            print "Possiveis Faces"
##            j = 0
##            for face in peca.faces:
##                j += 1
##                print "Face %s" %j
##                for vertice in face:
##                    print vertice.cod
        
        #(6.4)
        for peca in pecas:
            if not len(peca.faces):
                planar = 0
        if planar == 0:
            print "Grafo nao planar nao ha faces"
        if not len(pecas):
            sair = 1

        #(6.5)
        if planar == 1 and not sair:
            pecaCritica = pecas[0]
            for peca in pecas:
                if len(peca.faces) == 1:
                    pecaCritica = peca

            print "Peca Critica"
            pecaCritica.resetVisita()
            pecaCritica.listaVertices(1)
            for vertice in pecaCritica.caminho:
                print vertice.cod

            print "Contatos Peca"
            for pontoContato in pecaCritica.pontosContato:
                print pontoContato.cod

            print "Possiveis Faces"
            j = 0
            for face in pecaCritica.faces:
                j += 1
                print "Face %s" %j
                for vertice in face:
                    print vertice.cod

            pecaCritica.encontraCaminho()
            print "Caminho"
            for vertice in pecaCritica.caminho:
                print vertice.cod

            grafoNovo.insereCaminho(grafo,pecaCritica,faces)
            print "GrafoNovo"

            grafo.removeVerticeVazio()
            grafoNovo.resetVisita()
            grafoNovo.listaVertices(1)
            print "Grafo"
            grafo.resetVisita()
            grafo.listaVertices(1)


            if len(faces) > condicao:
                planar = 0
            #print "Pressione Enter para continuar"
            #raw_input()
                
    if not planar:
        print "GRAFO NAO PLANAR"
        
    if sair:
        print "GRAFO PLANAR"
    

    print "\n\n\nGRAFO NOVO\n"
    grafoNovo.resetVisita()
    grafoNovo.listaVertices(1)

#    print "\n\nGrafo com arestas removidas"
#    grafo.resetVisita()
#    print "\n\nGRAFO"
#    grafo.listaVertices(1)


def montaCiclo(grafo):
    ciclo = grafo.encontraCiclo()
    
    grafoNovo = Grafo(len(ciclo))

    for vertice in ciclo:
        grafoNovo.adicionaVertice(vertice.cod,0,[])
	# remove primeiro/ultimo vertice *repetido
#    del(grafoNovo.vertices[-1])
#    del(ciclo[-1])
 
    i = 0
    while i < len(grafoNovo.vertices):
        grafoNovo.vertices[i-1].arestas.append(grafoNovo.vertices[i])
        grafoNovo.vertices[i].arestas.append(grafoNovo.vertices[i-1])	
        i += 1

    i = 0
    while i < len(ciclo)-1:
        ciclo[i].arestas.remove(ciclo[i+1])
        ciclo[i].arestas.remove(ciclo[i-1])
        i += 1
    ciclo[len(ciclo)-1].arestas.remove(ciclo[0])
    ciclo[len(ciclo)-1].arestas.remove(ciclo[len(ciclo)-2])
    
    return grafoNovo

def encontraPeca(grafo):
    #encontra primeira condicao
    grafo.resetVisita()
    i = 0
    pecas=[]
    while i<len(grafo.vertices):
        if grafo.vertices[i].presenteCiclo:
            for aresta in grafo.vertices[i].arestas:
                if aresta.presenteCiclo:
                    peca = Peca(2)
                    peca.vertices.append(grafo.vertices[i])
                    peca.vertices.append(aresta)
                    pecas.append(peca)
        i += 1
    #encontra segunda condicao
    grafo.resetVisita()
    #cria uma lista de grafos
    for vertice in grafo.vertices:
        if not vertice.visitado and not vertice.presenteCiclo:
            lst=[]
            encontraComponenteConexa(vertice,lst)
            peca = Peca(len(lst))
            for i in lst:
                peca.vertices.append(i)
            pecas.append(peca)
    i = 0
    for peca in pecas:
        i += 1
        peca.encontraPontosContato()

#    for peca in pecas:
#        peca.resetVisita()
#    for peca in pecas:
#        print "Peca"
#        peca.listaVertices()
    return pecas

def encontraComponenteConexa(vertice,lst):
    vertice.visitado = 1
    if not vertice.presenteCiclo:
        lst.append(vertice)
        for verticeAdj in vertice.arestas:
            if not verticeAdj.visitado:
                encontraComponenteConexa(verticeAdj,lst)
    else:
        presente = 0
        for ponto in lst:
            if vertice.cod == ponto.cod:
                presente = 1
        if presente == 0:
            lst.append(vertice)
