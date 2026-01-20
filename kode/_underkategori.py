
class Underkategori:

    def __init__(self, sprak2_tittel, sprak1_tittel):
        self._sprak1_tittel = sprak1_tittel
        self._sprak2_tittel = sprak2_tittel
        self._gloser = []

    def legg_til_glose(self, glose):
        self._gloser.append(glose)

    def hent_gloser_som_kortrader(self):
        return [glose.hent_som_kortrad() for glose in self._gloser]