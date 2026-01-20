from _sprak import Sprak
from _filhandterer import Filhandterer
from _hovedkategori import Hovedkategori

from _dataprosessering import Dataprosessering

class Datasenter:

    def __init__(self):
        self._ordark = Filhandterer.les_json("mine-gloser/ordark.json")

        self._sprak = self.__sett_sprak(self._ordark)
        self._filhandterer = self.__sett_filhandterer(self._ordark)
        self._ordliste = Dataprosessering.hent_ordliste_fra_ordark(self)

        self._kategorier = self.__sett_kategorier(self._ordliste)

    def oppdater_ordark(self):
        Dataprosessering.skriv_ordliste_til_ordark(self)

    def __sett_sprak(self, ordark):
        hovedsprak = ordark["hovedspråk"]
        malsprak = ordark["målspråk"]

        return Sprak(hovedsprak, malsprak)

    def __sett_filhandterer(self, ordark):
        ordliste_ark = ordark["ordliste-ark"]
        excel_specs = ordark["excel"]
        googleark_specs = ordark["googleark"]

        return Filhandterer(ordliste_ark, excel_specs, googleark_specs)

    def __sett_kategorier(self, ordliste):

        kateg = Filhandterer.les_json("mine-gloser/kategorier.json")

        # setter opp hovedkategorier
        kategorier = {}
        for hk_kort,hk in kateg["hovedkategorier"].items():
            kategorier[hk_kort] = Hovedkategori(hk, hk_kort)

        # setter opp underkategorier
        for hk_kort, ukateg in kateg["underkategorier"].items():
            hovedkategori = kategorier[hk_kort]
            for (uk_kort,uk) in ukateg.items():
                hovedkategori.legg_til_underkategori(uk_kort, *uk)

        manglende_kat = set()

        # legger til gloser i kategoriene
        for glose in ordliste._gloser:
            for kat in glose.hent_kategorier():
                hk,uk = kat.split("/")

                if hk not in kategorier:
                    if hk not in manglende_kat:
                        manglende_kat.add(hk)
                        print(f'MERKNAD: Hovedkategorien "{hk}" er ikke spesifisert.')
                    continue

                hovedkategori = kategorier[hk]
                underkategorier = hovedkategori.hent_underkategorier()
                if uk not in underkategorier:
                    if kat not in manglende_kat:
                        manglende_kat.add(kat)
                        print(f'MERKNAD: Kategorien "{kat}" er ikke spesifisert.')
                    continue

                underkategorier[uk].legg_til_glose(glose)

        return kategorier