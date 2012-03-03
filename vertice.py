class Vertices(object):
    """Vertice de um grafo"""

    def __init__(self,cod,grau,arestas=[]):
        self.cod = cod
        self.grau = grau
        self.arestas = arestas
        self.visitado = 0
        self.nivel = 0
        self.filhos = []
        self.pai = 0
        self.retornos = []
        self.lowpt = 0
        self.articulacao = 0
        self.demarcador = 0
        self.presenteCiclo = 0


    def low_pt(self):
        """Calcula lowpt de todos os vertices do grafo"""
        self.visitado = 1
        self.lowpt = self
        for filho in self.filhos:
            if not filho.visitado:
                filho.low_pt()
            if filho.lowpt.nivel < self.lowpt.nivel:
                self.lowpt = filho.lowpt
        for retorno in self.retornos:
            if retorno.lowpt.nivel < self.lowpt.nivel:
                self.lowpt = retorno.lowpt


    def Articulacao(self):
        """funcao recebe a raiz e altera articulacao dos vertices"""
        self.visitado = 1
        for filho in self.filhos:
            if not self.pai:
                if len(self.filhos)>1:
                    self.articulacao = 1
            elif filho.lowpt.cod == filho.cod or filho.lowpt.cod == self.cod:
                self.articulacao = 1
            if not filho.visitado:
                filho.Articulacao()


    def Demarcador(self):
        """funcao recebe raiz e altera atributo demarcador dos vertices"""
        self.visitado = 1
        for filho in self.filhos:
            if self.articulacao and filho.lowpt.cod == self.cod:
                filho.demarcador = 1
            if not filho.visitado:
                filho.Demarcador()
