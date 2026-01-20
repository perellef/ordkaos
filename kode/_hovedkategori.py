from _underkategori import Underkategori

class Hovedkategori:

    def __init__(self, navn, kortnavn):
        self._kortnavn = kortnavn
        self._navn = navn
        self._underkategorier = {}

    def legg_til_underkategori(self, navn, *underkategori):
        self._underkategorier[navn] = Underkategori(*underkategori)

    def hent_navn(self):
        return self._navn

    def hent_underkategorier(self):
        return self._underkategorier