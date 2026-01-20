import copy

import networkx as nx
from networkx.algorithms import threshold

from database.dao import DAO

class Model:
    def __init__ (self) :
        self._G = nx.Graph ()
        self._durate_album = {}

        self._dict_album = {}

    def get_nodes (self, threshold) :
        nodes = []
        album = DAO.read_album (threshold)
        for a in album :
            nodes.append(a)
            self._durate_album [a.id] = a.durata
            self._dict_album [a.id] = a
        return nodes

    def get_edges (self, threshold) :
        edges = []
        connessioni = DAO.read_connessione (threshold)
        for c in connessioni :
            edges.append ((c.album1, c.album2))
        return edges

    def build_graph (self, threshold) :
        self._G.clear()

        nodes = self.get_nodes(threshold)
        for album in nodes:
            self._G.add_node(album.id)

        edges = self.get_edges(threshold)
        self._G.add_edges_from(edges)

    def get_num_nodes (self) :
        num_nodes = self._G.number_of_nodes ()
        return num_nodes

    def get_num_edges (self) :
        num_edges = self._G.number_of_edges ()
        return num_edges

    def get_componenti_connesse (self, nodo) :
        componenti_connesse = nx.node_connected_component(self._G, nodo)
        return len(componenti_connesse)

    def get_durata_vicini (self, nodo) :
        durata = self._durate_album [nodo]
        for n in self._G.neighbors (nodo):
            durata += self._durate_album [n]
        return durata

    def get_set_ideale (self, nodo, durata_massima) :
        self._best_set = []
        self._max_durata = 0

        parziale = []

        self.ricorsione (nodo, parziale, 0, durata_massima)
        return self._best_set, self._max_durata

    def ricorsione (self, nodo, parziale, durata_attuale, durata_massima) :
        if durata_attuale >= self._max_durata :
            self._max_durata = durata_attuale
            self._best_set = list (parziale)


        vicini = list (self._G.neighbors (nodo))
        vicini.append (nodo)
        vicini.sort (key = lambda n: self._durate_album [n])

        for n in vicini :
            album = self._dict_album [n]
            durata = self._durate_album [n]

            if album not in parziale and (durata_attuale + durata) <= float (durata_massima) :
                parziale.append (album)
                self.ricorsione (n, parziale, durata_attuale + durata, durata_massima)
                parziale.pop ()



"""     
        lista_vicini = []

        for n in self._G.neighbors (nodo) :
            lista_vicini.append (n)

        minimo = None
        durata_minima = None

        set_album_parziale = []

        for n in lista_vicini :

            if minimo is None :
                minimo = self._dict_album [nodo]
                durata_minima = self._durate_album [nodo]

            else :
                if self._durate_album [n] < durata_minima :
                    minimo = self._dict_album [n]
                    durata_minima = self._durate_album [n]

        set_album_parziale.append (minimo)

        if minimo in lista_vicini:
            lista_vicini.remove(minimo)

        return set_album_parziale, durata_minima
"""






