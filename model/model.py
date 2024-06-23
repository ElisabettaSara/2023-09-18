import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.listCountry = []
        self.listYears = []

        self.grafo = nx.Graph()
        self.nodes = []
        self.edges = []
        self.idMapRetailer = {}
        self.volumi = []

        self._bestPath = []
        self._bestWeight = 0

        self.loadCountry()
        self.loadYears()

    def getBestPath(self, nMax):
        self._bestPath = []
        self._bestWeight = 0

        for n in self.nodes:
            parziale = [n]
            peso = 0
            self._ricorsione(parziale, peso, nMax)

        return self._bestPath, self._bestWeight

    def _ricorsione(self, parziale, peso, nMax):
        if len(parziale) - 1 == nMax:
            if parziale[0] == parziale[-1] and peso >= self._bestWeight:
                self._bestPath = copy.deepcopy(parziale)
                self._bestWeight = peso
                return
            else:
                return

        for v in self.grafo[parziale[-1]]:
            if (len(parziale) == nMax and v== parziale[0]) or (v not in parziale):
                peso += self.grafo[parziale[-1]][v]['weight']
                parziale.append(v)
                self._ricorsione(parziale, peso, nMax)
                peso -= self.grafo[parziale[-2]][parziale[-1]]['weight']
                parziale.pop()


    def loadCountry(self):
        self.listCountry = DAO.getState()

    def loadYears(self):
        self.listYears = DAO.getYears()

    def buildGraph(self, country, year):
        self.grafo.clear()
        self.nodes = DAO.getNode(country)
        self.grafo.add_nodes_from(self.nodes)

        for n in self.nodes:
            self.idMapRetailer[n.Retailer_code] = n

        self.edges = DAO.getEdge(country, year)
        for e in self.edges:
            self.grafo.add_edge(self.idMapRetailer[e[0]], self.idMapRetailer[e[1]], weight=e[2])

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)

    def getVolumi(self):
        for n in self.nodes:
            peso = 0
            for v in self.grafo[n]:
                peso += self.grafo[n][v]['weight']

            self.volumi.append((n, peso))
        self.volumi = sorted(self.volumi, key=lambda x: x[1], reverse=True)
        return self.volumi

    def getPesoArco(self, v0, v1):
        return self.grafo[v0][v1]['weight']
