import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._model._G.clear()
        durata = self._view.txt_durata.value

        self._model.get_nodes (durata)
        self._model.get_edges (durata)
        self._model.build_graph (durata)

        self._view.lista_visualizzazione_1.controls.clear ()
        self._view.lista_visualizzazione_1.controls.append (ft.Text (f"Grafo creato: {self._model.get_num_nodes()} album, "
                                                                     f"{self._model.get_num_edges()} archi."))

        nodes = self._model.get_nodes (durata)

        self._view.dd_album.options.clear()
        for album in nodes:
            self._view.dd_album.options.append (ft.dropdown.Option (key=album.id, text=album.title))

        self._view.page.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO
        album_id = int (self._view.dd_album.value)
        componenti_connesse = self._model.get_componenti_connesse (album_id)

        return album_id, componenti_connesse

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO
        album_id, componenti_connesse = self.get_selected_album (e)
        durata_totale = self._model.get_durata_vicini (album_id)

        self._view.lista_visualizzazione_2.controls.clear ()
        self._view.lista_visualizzazione_2.controls.append (ft.Text (f"Dimensione componente: {componenti_connesse}\n"
                                                                     f"Durata totale: {durata_totale} minuti"))
        self._view.page.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO
        nodo_di_partenza = int (self._view.dd_album.value)
        durata_massima = self._view.txt_durata_totale.value

        set_album, durata = self._model.get_set_ideale (nodo_di_partenza, durata_massima)
        self._view.lista_visualizzazione_3.controls.clear ()

        self._view.lista_visualizzazione_3.controls.append (ft.Text (f"Set trovato ({len (set_album)} album, durata {durata} minuti): "))
        for album in set_album :
            self._view.lista_visualizzazione_3.controls.append (ft.Text (f"{album}"))

        self._view.page.update()