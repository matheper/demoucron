from grafos import *
class Peca(Grafo):

    def __init__(self, nVertices):
        super(Peca,self).__init__(nVertices)
        self.pontosContato = []
        self.faces = []
        self.caminho = []
#        self.encontrouCaminho = 0
        

    def encontraPontosContato(self):
        for vertice in self.vertices:
            if vertice.presenteCiclo:
                self.pontosContato.append(vertice)

    def encontraFaces(self,facesX):
        for face in facesX:
            contemPonto = 1
            j = 0
            while contemPonto and j < len(self.pontosContato):
                presente = 0
                i = 0
                while not presente and i < len(face):
                    if self.pontosContato[j].cod == face[i].cod:
                        presente = 1
                    i += 1
                if presente == 0:
                    contemPonto = 0
                j += 1
            if contemPonto == 1:
                self.faces.append(face)

    def encontraCaminho(self):
        if len(self.vertices) > 2:
            #Algoritmo de Tremaux
            # E = -1
            # F = 1
            matriz = {}
            for vertice in self.vertices:
                adjacencias = {}
                matriz[vertice]=adjacencias
                for adjacente in vertice.arestas:
                    presente = 0
                    for presentePeca in self.vertices:
                        if presentePeca == adjacente:
                            presente = 1
                    if presente == 1:
                        adjacencias[adjacente] = 0

            s = self.pontosContato[0]
            t = self.pontosContato[1]
            v = s
            sair = 0
            while not sair:
                #u = passagem nao marcada(v,u)
                u = 0
                for adjacencia in matriz[v]:
                    presente = 0
                    for presentePeca in self.vertices:
                        if presentePeca == adjacencia:
                            presente = 1
                    if presente == 1:
                        if matriz[v][adjacencia] == 0:
                            u = adjacencia
                if u:#passo 2 ha passagens marcadas
                    matriz[v][u] = -1
                    w = 0
                    for adjacencia2 in matriz[u]:
                        if matriz[u][adjacencia2] != 0:
                            w = adjacencia2
                    if w:
                        matriz[u][v] = -1
                    else:
                        matriz[u][v] = 1
                        v = u
                else:#Passo 5, nao ha passagens marcadas
                    u = 0
                    for adjacencia in matriz[v]:
                        presente = 0
                        for presentePeca in self.vertices:
                            if presentePeca == adjacencia:
                                presente = 1
                        if presente == 1:
                            if matriz[v][adjacencia] == 1:
                                u = adjacencia
                    if u:
                        v = u
                    else: sair = 1

##            for vertice in self.vertices:
##                print "vertice %s" %vertice.cod
##                print "Aresta"
##                for adjacencia in vertice.arestas:
##                    presente = 0
##                    for presentePeca in self.vertices:
##                        if presentePeca == adjacencia:
##                            presente = 1
##                    if presente == 1:
##                        print adjacencia.cod
##                        print matriz[vertice][adjacencia]

            self.caminho = []
            v = t
            u = t
            while u != 0:
                u = 0
                for adjacencia in matriz[v]:
                    presente = 0
                    for presentePeca in self.vertices:
                        if presentePeca == adjacencia:
                            presente = 1
                    if presente == 1:
                        if matriz[v][adjacencia] == 1:
                            self.caminho.append(v)
                            u = adjacencia
                if u:
                    v = u
            self.caminho.append(s)
        else:
            self.caminho.append(self.pontosContato[0])
            self.caminho.append(self.pontosContato[1])

        #remove ligacoes dos vertices do ciclo
        i = 0
        while i < len(self.caminho)-1:
            self.caminho[i].presenteCiclo = 1
            self.caminho[i].arestas.remove(self.caminho[i+1])
            self.caminho[i+1].arestas.remove(self.caminho[i])
            i += 1
