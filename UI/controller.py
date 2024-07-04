import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        for n in self._model.getNazioni():
            self._view._ddCountry.options.append(ft.dropdown.Option(n))

        for a in self._model.getAnno():
            self._view._ddyear.options.append(ft.dropdown.Option(a))




    def handle_graph(self, e):
        self._model._grafo.clear()
        nazione = self._view._ddCountry.value
        anno = self._view._ddyear.value
        self._view.txtOut.clean()
        self._model.creaGrafo(nazione, anno)
        self._view.txtOut.controls.append(ft.Text("Grafo creato"))
        numNodi= self._model.getNumNodi()
        numArchi = self._model.getNumArchi()
        self._view.txtOut.controls.append(ft.Text(f"Ci sono {numNodi} vertici"))
        self._view.txtOut.controls.append(ft.Text(f"Ci sono {numArchi} archi"))


        self._view.update_page()








    def handle_volumi(self, e):
        pass

    def handle_search(self, e):
        pass