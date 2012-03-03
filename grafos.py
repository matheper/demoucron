# -*- coding: utf-8 -*-
import copy
from vertice import *

class Grafo(object):
    """Define o grafo"""

    
    def __init__(self,nVertices):
        self.vertices = []
        self.nVertices = nVertices
        self.lstRaizesConexas = []
        self.lstRaizesBiconexas = []
        self.lstComponentesBiconexas = []
        self.planar = 1


    def ordenaArestas(self):
        for vertice in self.vertices:
            vertice.arestas.sort()


    def resetVisita(self):
        for i in self.vertices:
            i.visitado = 0


    def add_vertice(self,vertice,nivel):
        """Adiciona vertice a arvore, recebendo o object grafo,
        o vertice inicial e o nivel inicial
        Metodo chamado no gera_arvore"""
        vertice.visitado = 1
        vertice.nivel = nivel
        for aresta in vertice.arestas:
            if not aresta.visitado:
                vertice.filhos.append(aresta)
                aresta.pai = vertice
                self.add_vertice(aresta,nivel+1)
            elif vertice.nivel > aresta.nivel:
                vertice.retornos.append(aresta)
        return


    def gera_arvore(self):
        """Gera uma arvore para cada componente do grafo
        Recebe um grafo como parametro
        Retorna uma lista com a raiz de cada arvore do grafo
        Método encontra Componentes Conexas"""
        lstRaiz = []
        for vertice in self.vertices:
            if vertice.visitado == 0:
                self.add_vertice(vertice,0)
                lstRaiz.append(vertice)
            try:
                vertice.retornos.remove(vertice.pai)
            except: pass
        return lstRaiz


    def escreveArvore(vertice):
        vertice.visitado = 1
        print vertice.cod
        for filho in vertice.filhos:
            if not filho.visitado:
                escreveArvore(filho)

    def escreveArvoreAll(self):
        #print lstBiconexa
        for biconexa in self.lstRaizesBiconexa:
            print "Arvore com raiz em %s" % (biconexa.cod)
            self.resetVisita()
            escreveArvore(biconexa)
            print "\n"

    def biconexa(self,vertice):
        """Encontra componentes biconexas do grafo"""
    #    import pdb;pdb.set_trace()
        vertice.visitado = 1
        i = 0
        while i < len(vertice.filhos):
        # for chama biconexa recursivamente ate as folhas
            if not vertice.filhos[i].visitado:
                self.biconexa(vertice.filhos[i])
            if vertice.filhos[i].demarcador:
                vertice.filhos[i].demarcador = 0
                raiz = copy.deepcopy(vertice)
                raiz.filhos = [vertice.filhos[i]]
                raiz.pai = 0
                raiz.retornos = []
                self.atualizaReferencia(raiz,raiz)
                self.lstRaizesBiconexas.append(raiz)
                self.vertices.append(raiz)
                self.nVertices += 1
                vertice.filhos.remove(vertice.filhos[i])
                i-= 1
            i+= 1

    def atualizaReferencia(self,vertice,raiz):
        """Atualiza referencias dos filhos do objeto copiado
        Metodo chamado no biconexa"""
        vertice.visitado = 1
        for filho in vertice.filhos:
            self.atualizaReferencia(filho,raiz)
        for retorno in vertice.retornos:
            if retorno.cod == raiz.cod:
                retorno = raiz
        if vertice.lowpt.cod == raiz.cod:
            vertice.lowpt = raiz
        if vertice.pai:
            if vertice.pai.cod == raiz.cod:
                vertice.pai = raiz

    def verificaRetorno(self,vertice,raiz):
        temRetorno = []
        for filho in vertice.filhos:
            temRetorno += self.verificaRetorno(filho,raiz)
        for retorno in vertice.retornos:
            if retorno.cod == raiz.cod:
                temRetorno.append(vertice)
        return temRetorno

    def atualizaAdjacencias(self):
        """Metodo chamado apos encontradas as componentes biconexas
        Atualiza adjacencias e grau de cada vertice"""
        for vertice in self.vertices:
            retornos = self.verificaRetorno(vertice,vertice)
            if vertice.pai:
                vertice.arestas = [vertice.pai]+vertice.filhos+retornos+vertice.retornos
                vertice.grau = len(vertice.arestas)
            else:
                vertice.arestas = vertice.filhos+retornos
                vertice.grau = len(vertice.arestas)

    def encontraCiclo(self):
        ciclo = []
        vertice = self.vertices[0]
        vertice.visitado = 1
        ciclo.append(vertice)
        filho = vertice.arestas[0]
        anterior = vertice
        vertice = filho
        while not vertice.visitado:
            vertice.visitado = 1
            ciclo.append(vertice)
            if vertice.arestas[0] != anterior:
                filho = vertice.arestas[0]
            else:
                filho = vertice.arestas[1]
            anterior = vertice
            vertice = filho
        while ciclo[0] != vertice:
            ciclo.pop(0)
#        ciclo.append(vertice)
        for verticeCiclo in ciclo:
            verticeCiclo.presenteCiclo = 1
        return ciclo

    def insereCaminho(self,grafo,peca,faces):
        #chamar a partir do grafo novo
        #passar por parametro grafo antigo e caminho a ser adicionado
        if len(peca.vertices)>2:
            caminho = peca.caminho
            tamanhoGrafoIni = len(self.vertices)

            #cria vertices no grafoNovo
            i = 1
            while i < len(caminho)-1:
                self.adicionaVertice(caminho[i].cod,0,[])
                i += 1

            #encontra primeiro ponto de contato e o adiciona ao caminho novo
            i=0
            caminhoNovo = []
            caminhoNovo.append(0)
            while i < len(self.vertices) and not caminhoNovo[0]:
                if self.vertices[i].cod == caminho[0].cod:
                    caminhoNovo[0] = self.vertices[i]
                i += 1
            #adiciona o caminho ao caminho novo
            i = tamanhoGrafoIni
            while i < tamanhoGrafoIni + len(caminho)-2:
                caminhoNovo.append(self.vertices[i])
                i += 1
            #encontra segundo ponto de contato e o adiciona ao caminho novo
            i=0
            caminhoNovo.append(0)
            while i < len(self.vertices) and not caminhoNovo[-1]:
                if self.vertices[i].cod == caminho[-1].cod:
                    caminhoNovo[-1] = self.vertices[i]
                i += 1

            #insere ligacoes
            i = 0
            while i < len(caminhoNovo)-1:
                caminhoNovo[i].arestas.append(caminhoNovo[i+1])
                caminhoNovo[i+1].arestas.append(caminhoNovo[i])	
                i += 1
            
            #marca vertices como ponto de contato
            for vertice in self.vertices:
                vertice.presenteCiclo=1
            
            #atualiza faces
            face1 = peca.faces[0]
            face2 = []
            i = 0
            while face1[i].cod!=caminhoNovo[0].cod:
                i += 1
            j = 0
            while face1[j]!=caminhoNovo[-1]:
                j += 1

            if i > j:
                caminhoAux = []
                for vertice in caminhoNovo:
                    caminhoAux.append(vertice)
                caminhoNovo = caminhoAux[::-1]
                i, j = j, i
            
            face2.append(face1[i])
            k = i + 1
            while k < j:
                face2.append(face1.pop(k))
                j -= 1
            face2.append(face1[j])

            k = len(caminhoNovo)-2
            while k > 0:
                face2.append(caminhoNovo[k])
                k -= 1
            faces.append(face2)

            listaAux = []
            k=j
            while k < len(face1):
                listaAux.append(face1.pop(k))
            
            k = 1

            while k < len(caminhoNovo)-1:
                face1.append(caminhoNovo[k])
                k += 1
            k=0
            while k<len(listaAux):
                face1.append(listaAux[k])
                k += 1

        else:
            caminho = peca.caminho
            tamanhoGrafoIni = len(self.vertices)

            #encontra pontos contato no grafo novo
            vertice1 = 0
            i = 0
            while i < len(self.vertices) and not vertice1:
                if caminho[0].cod == self.vertices[i].cod:
                    vertice1 = self.vertices[i]
                i += 1

            vertice2 = 0
            i = 0
            while i < len(self.vertices) and not vertice2:
                if caminho[1].cod == self.vertices[i].cod:
                    vertice2 = self.vertices[i]
                i += 1
            
            #insere ligacoes
            vertice1.arestas.append(vertice2)
            vertice2.arestas.append(vertice1)
                
            #atualiza faces
            face1 = peca.faces[0]
            face2 = []
            i = 0
            while face1[i].cod!=vertice1.cod:
                i += 1
            j = 0
            while face1[j].cod!=vertice2.cod:
                j += 1

            if i > j:
                i, j = j, i

            face2.append(face1[i])
            k = i + 1
            while k < j:
                face2.append(face1.pop(k))
                j -= 1
            face2.append(face1[j])
            faces.append(face2)



    def contaArestas(self):
        arestas = 0
        for vertice in self.vertices:
            for aresta in vertice.arestas:
                arestas += 1
        return arestas/2


    def removeVerticeVazio(self):
        i = 0
        while i < len(self.vertices):
            if not len(self.vertices[i].arestas):
                self.vertices.remove(self.vertices[i])
            i += 1
    
    def removeCaminho(self,caminho):
        tamanhoGrafoIni = len(self.vertices)

    def simplificar(self):
        flag = 1
        self.resetVisita()
        self.ordenaArestas()
        self.simplificaLoop(flag)
        self.simplificaParalela(flag)
        self.simplificaGrau2(flag)
        self.simplificaGrau2(flag)

    def simplificar2(self):
        i = 0
        while i < len(self.vertices):
            if self.vertices[i].grau == 2:
                self.vertices.remove(self.vertices[i])
            i += 1

    def simplificaGrau2(self,flag):
        i = 0
        while flag > 0:
            flag = 0
            while i < len(self.vertices):
                if self.vertices[i].grau == 2:
                    flag = 1
                    self.escreveArquivoSaida("Grau 2: Aresta (%s,%s) - " % (self.vertices[i].arestas[0].cod, self.vertices[i].cod))
                    self.escreveArquivoSaida("Aresta (%s,%s) removida\n" % (self.vertices[i].cod, self.vertices[i].arestas[1].cod))

                    self.vertices[i].arestas[0].arestas.append(self.vertices[i].arestas[1])
                    self.vertices[i].arestas[1].arestas.append(self.vertices[i].arestas[0])
                    self.removeVertice(self.vertices[i].arestas[0].arestas,self.vertices[i])
                    self.removeVertice(self.vertices[i].arestas[1].arestas,self.vertices[i])
                    self.vertices.remove(self.vertices[i])
                    i-= 1
                    self.simplificaLoop(flag)
                    self.simplificaParalela(flag)
                i+= 1

    def simplificaLoop(self,flag):
        for vertice in self.vertices:
            i = 0
            while i < len(vertice.arestas):
                if vertice.cod == vertice.arestas[i].cod:
                    flag = 1
                    self.escreveArquivoSaida("Loop: Aresta (%s,%s) removida\n" % (vertice.cod, vertice.cod))
                    vertice.arestas.remove(vertice.arestas[i])
                    vertice.grau -= 1
                    i-= 1
                i+= 1

    def simplificaParalela(self,flag):
        self.ordenaArestas()
        for vertice in self.vertices:
            i = 0
            while i < len(vertice.arestas)-1:
                if vertice.arestas[i].cod == vertice.arestas[i+1].cod:
                    flag = 1
                    vertice.arestas.remove(vertice.arestas[i+1])
                    vertice.arestas[i].arestas.remove(vertice)
                    self.escreveArquivoSaida("Paralela: Aresta (%s,%s) removida\n" % (vertice.cod, vertice.arestas[i].cod))
                    vertice.grau -= 1
                    vertice.arestas[i].grau -= 1
                    i-= 1
                i+= 1

    def escreveArquivoSaida(self,descricao):
        argSaida = open('saida.txt','a')
        argSaida.writelines(descricao)
        argSaida.close()


    def escreveArvoreArquivo(self,vertice):
        vertice.visitado = 1 
        self.escreveArquivoSaida(" %s " % (vertice.cod))
        for filho in vertice.filhos: 
            if not filho.visitado:
                self.escreveArvoreArquivo(filho)

    def retornaBiconexa(self,vertice,grafo):
        #utilizado em geraBiconexa
        vertice.visitado = 1
        grafo.vertices.append(vertice)
        for adjacente in vertice.arestas: 
            if not adjacente.visitado:
                self.retornaBiconexa(adjacente, grafo)


    def escreveGrafo(self):
        self.escreveArquivoSaida("\nGrafo Simplificado\n")
        for vertice in self.vertices:
            self.escreveArquivoSaida(\
                "Cod = %s, Grau = %s, Adjacencias = %s\n"\
                %(vertice.cod,
                vertice.grau,
                [aresta.cod for aresta in vertice.arestas]))

    def adicionaVertice(self,cod, grau, arestas=[]):
        self.vertices.append(Vertices(cod,grau,arestas))

    def removeVertice(self,lista,vertice):
        i = 0
        while i < len(lista):
            if lista[i].cod == vertice.cod:
                lista.remove(lista[i])
                i -= 1
            i += 1
		
			
    def listaVertices(self,flag = 0):
        for vertice in self.vertices:
            print\
                "Cod = %s, Grau = %s, Arestas = %s, PontoContato = %s"\
                %(vertice.cod,
                vertice.grau,
                [aresta.cod for aresta in vertice.arestas],
                vertice.presenteCiclo)
            try: pai = vertice.pai.cod
            except: pai = 0
            if not flag:
                print\
                    "Nivel = %s, Pai = %s, Filhos = %s, Lowpt = %s, Visitado = %s, Retornos = %s\n, Articulacao = %s\n, Demarcador = %s\n"%(
                    vertice.nivel,
                    pai,
                    [aresta.cod for aresta in vertice.filhos],
                    vertice.lowpt.cod,
                    vertice.visitado,
                    [aresta.cod for aresta in vertice.retornos],
                    vertice.articulacao,
                    vertice.demarcador
                    )

