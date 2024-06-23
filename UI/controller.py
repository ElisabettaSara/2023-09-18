import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        country = self._model.listCountry
        years = self._model.listYears

        for c in country:
            self._view._ddCountry.options.append(ft.dropdown.Option(c))

        for y in years:
            self._view._ddyear.options.append(ft.dropdown.Option(y))

    def handle_graph(self, e):
        if self._view._ddCountry.value == None:
            self._view.create_alert("Inserire un paese")
            return

        if self._view._ddyear.value == None:
            self._view.create_alert("Inserire un anno")
            return
        country = self._view._ddCountry.value
        year = self._view._ddyear.value
        self._model.buildGraph(country, year)
        nN, nE = self._model.getGraphSize()
        self._view.txtOut.clean()
        self._view.txtOut.controls.append(ft.Text(f"Grafo creato con {nN} vertici e {nE} archi"))
        self._view.btn_search.disabled = False
        self._view.update_page()

    def handle_volumi(self, e):
        volumi = self._model.getVolumi()
        self._view.txtOut.clean()
        self._view.txtOut.controls.append(ft.Text(f"Il volume di vendita dei retailers nel grafo è:"))
        for v in volumi:
            self._view.txtOut.controls.append(ft.Text(f"{v[0]} --> {v[1]}"))

        self._view.update_page()

    def handle_search(self, e):
        try:
            nMax = int(self._view._txtIn.value)
        except ValueError:
            self._view.create_alert("Inserire un intero nel campo della lunghezza")
            return

        if nMax < 2:
            self._view.create_alert("Inserire un valore >= a 2")
            return

        bestPath, bestWeight = self._model.getBestPath(nMax)
        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Cammino di peso massimo con esattamente {nMax} archi"))
        self._view.txtOut2.controls.append(ft.Text(f"Peso del cammino: {bestWeight}"))
        for i in range(len(bestPath)-1):
            self._view.txtOut2.controls.append(ft.Text(f"{bestPath[i]} --> {bestPath[i+1]}  Peso={self._model.getPesoArco(bestPath[i], bestPath[i+1])}"))

        self._view.update_page()