import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.idMap={}
        self._grafo = nx.Graph()


    def getNazioni(self):
        return DAO.getNazione()

    def getAnno(self):
        return DAO.getAnno()


    def creaGrafo(self, nazione, anno):

        for n in DAO.getNodi(nazione):
            self.idMap[n.Retailer_code] = n
            self._grafo.add_node(n)

        for e in DAO.getArchi(nazione, anno):
            self._grafo.add_edge(self.idMap[e[0]], self.idMap[e[1]], weight=e[2])



    def getNumNodi(self):
        return len(self._grafo.nodes)


    def getNumArchi(self):
        return len(self._grafo.edges)


